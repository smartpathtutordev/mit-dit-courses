/* Service worker: serves  <scope>/v/<languageRootId>/<GRADE>/<QUARTER>/<WEEK>/<DAY>/<path>
   from Google Drive so each module's index.html can load assets/, speech/ and videos/
   by the same relative paths it uses on disk.

   Speed:
   - a prebuilt per-day index (m/<LANG>/<dayKey>.json) maps every path to its Drive file id,
     so no folder-by-folder lookups are needed;
   - when a module opens, every file it references is downloaded in the background
     into a local cache, so later slides, narration and videos play instantly;
   - the day's folders are re-checked in the background so edits made in Drive show up. */
importScripts("config.js", "vault.js");
const CFG = self.PORTAL_CONFIG;
const SCOPE = self.registration.scope;
const VPREFIX = new URL("v/", SCOPE).pathname;
const LANG_BY_ROOT = new Map(CFG.languages.map(l => [l.folderId, l]));
const MEDIA_CACHE = "spt-media-v2";
const FOLDER = "application/vnd.google-apps.folder";
const MAX_ENTRIES = 1200;
const PREFETCH_CONCURRENCY = 6;

const days = new Map();      // `${root}|${dayKey}` -> {id, f:{path:[id,size,mtime]}, d:{path:id}, checked}
const inflight = new Map();  // fileId@mtime -> Promise<Blob>
const prefetched = new Set();

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil((async () => {
  for (const k of await caches.keys()) if (k.startsWith("spt-media-") && k !== MEDIA_CACHE) await caches.delete(k);
  await self.clients.claim();
})()));
/* ---------------- Password vault ---------------- */
const VAULT = self.PORTAL_VAULT || null;
const META_CACHE = "spt-meta-v1";
const META_KEY = "https://meta.local/vault";
let vaultKey = null;
async function ensureUnlocked() {
  if (!VAULT || vaultKey) return true;
  try {
    const r = await (await caches.open(META_CACHE)).match(META_KEY);
    if (!r) return false;
    const v = await r.json();
    const key = SPTVault.b64d(v.key);
    if ((await SPTVault.decrypt(key, VAULT.check)) !== "smartpath-ok") return false;
    vaultKey = key;
    CFG.apiKey = await SPTVault.decrypt(key, VAULT.apiKey);
    return true;
  } catch (e) { return false; }
}
async function lockAll() {
  vaultKey = null; days.clear(); prefetched.clear();
  await caches.delete(META_CACHE);
  await caches.delete(MEDIA_CACHE);
}

self.addEventListener("message", e => {
  const d = e.data || {};
  const reply = msg => { if (e.ports && e.ports[0]) e.ports[0].postMessage(msg); };
  if (d === "flush" || d.type === "flush") { days.clear(); prefetched.clear(); reply("ok"); return; }
  if (d.type === "unlock") {
    e.waitUntil((async () => {
      try {
        const key = SPTVault.b64d(d.key);
        if (!VAULT || (await SPTVault.decrypt(key, VAULT.check)) !== "smartpath-ok") throw new Error("bad key");
        vaultKey = key;
        CFG.apiKey = await SPTVault.decrypt(key, VAULT.apiKey);
        await (await caches.open(META_CACHE)).put(META_KEY, new Response(JSON.stringify({ key: d.key })));
        reply("ok");
      } catch (err) { reply("bad"); }
    })());
    return;
  }
  if (d.type === "lock") { e.waitUntil(lockAll().then(() => reply("ok"))); }
});
function locked() {
  return new Response(`<!DOCTYPE html><meta charset="utf-8"><body style="font-family:system-ui;padding:40px;color:#334">
<h2 style="margin:0 0 8px">Locked</h2><p>Open the review portal and enter the password first.</p></body>`,
    { status: 401, headers: { "content-type": "text/html; charset=utf-8" } });
}

/* ---------------- Drive helpers ---------------- */
function apiUrl(path, params) {
  const u = new URL(CFG.apiBase + path);
  for (const [k, v] of Object.entries(params || {})) u.searchParams.set(k, v);
  u.searchParams.set("key", CFG.apiKey);
  return u.toString();
}
async function listFolder(id) {
  const out = new Map();
  let pageToken = "";
  do {
    const p = { q: `'${id}' in parents and trashed=false`, fields: "nextPageToken,files(id,name,mimeType,size,modifiedTime)",
      pageSize: "1000", supportsAllDrives: "true", includeItemsFromAllDrives: "true" };
    if (pageToken) p.pageToken = pageToken;
    const r = await fetch(apiUrl("", p));
    if (!r.ok) throw new Error(`Drive list failed (${r.status})`);
    const j = await r.json();
    for (const f of j.files || []) {
      if (f.name.startsWith("._") || f.name === ".DS_Store") continue;
      const prev = out.get(f.name);
      if (!prev || prev.modifiedTime < f.modifiedTime) out.set(f.name, f);
    }
    pageToken = j.nextPageToken || "";
  } while (pageToken);
  return out;
}
const dayKey = segs => segs.map(s => s.replace(/[^A-Za-z0-9]+/g, "_")).join("__");

/* ---------------- Day index ---------------- */
async function crawlDay(dayId) {
  const day = { id: dayId, f: {}, d: { "": dayId } };
  let frontier = [["", dayId]];
  while (frontier.length) {
    const lists = await Promise.all(frontier.map(async ([pre, id]) => [pre, await listFolder(id)]));
    frontier = [];
    for (const [pre, files] of lists) for (const f of files.values()) {
      const rel = pre ? `${pre}/${f.name}` : f.name;
      if (f.mimeType === FOLDER) { day.d[rel] = f.id; frontier.push([rel, f.id]); }
      else day.f[rel] = [f.id, Number(f.size || 0), f.modifiedTime || ""];
    }
  }
  return day;
}

// Re-reads every folder of the day in one parallel round and merges changes.
async function revalidate(day) {
  const entries = Object.entries(day.d);
  const lists = await Promise.all(entries.map(async ([pre, id]) => {
    try { return [pre, await listFolder(id)]; } catch (e) { return [pre, null]; }
  }));
  for (const [pre, files] of lists) {
    if (!files) continue;
    const seen = new Set();
    for (const f of files.values()) {
      const rel = pre ? `${pre}/${f.name}` : f.name;
      seen.add(rel);
      if (f.mimeType === FOLDER) {
        if (!day.d[rel]) { const sub = await crawlDay(f.id); for (const [k, v] of Object.entries(sub.f)) day.f[`${rel}/${k}`] = v; for (const [k, v] of Object.entries(sub.d)) if (k) day.d[`${rel}/${k}`] = v; day.d[rel] = f.id; }
      } else day.f[rel] = [f.id, Number(f.size || 0), f.modifiedTime || ""];
    }
    for (const rel of Object.keys(day.f)) {
      const parent = rel.includes("/") ? rel.slice(0, rel.lastIndexOf("/")) : "";
      if (parent === pre && !seen.has(rel)) delete day.f[rel];
    }
  }
  day.checked = Date.now();
  return day;
}

async function liveDayId(root, segs) {
  let id = root;
  for (const s of segs) {
    const m = await listFolder(id);
    const hit = m.get(s) || [...m.values()].find(f => f.name.toLowerCase() === s.toLowerCase());
    if (!hit) return null;
    id = hit.id;
  }
  return id;
}

async function getDay(root, segs, { fresh = false } = {}) {
  const lang = LANG_BY_ROOT.get(root);
  const key = `${root}|${dayKey(segs)}`;
  let day = days.get(key);
  if (day && !fresh) return day;
  if (!day) {
    try {
      const r = await fetch(new URL(`m/${lang.code}/${dayKey(segs)}.json`, SCOPE), { cache: "no-cache" });
      if (r.ok) day = await SPTVault.openJson(vaultKey, await r.json());
    } catch (e) {}
    if (!day) {
      const id = await liveDayId(root, segs);
      if (!id) return null;
      day = await crawlDay(id);
      day.checked = Date.now();
    }
    days.set(key, day);
  }
  if (fresh) await revalidate(day);
  return day;
}

/* ---------------- Cache + download ---------------- */
const cacheKey = f => `https://cache.local/${f[0]}@${f[2]}`;
const TYPES = {
  html: "text/html; charset=utf-8", htm: "text/html; charset=utf-8", css: "text/css", js: "text/javascript",
  mjs: "text/javascript", json: "application/json", png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg",
  gif: "image/gif", webp: "image/webp", svg: "image/svg+xml", mp3: "audio/mpeg", wav: "audio/wav", m4a: "audio/mp4",
  ogg: "audio/ogg", mp4: "video/mp4", webm: "video/webm", woff: "font/woff", woff2: "font/woff2", ttf: "font/ttf",
  txt: "text/plain; charset=utf-8", vtt: "text/vtt"
};
const typeFor = name => TYPES[(name.split(".").pop() || "").toLowerCase()] || "application/octet-stream";

async function cached(f) {
  const c = await caches.open(MEDIA_CACHE);
  const r = await c.match(cacheKey(f));
  return r ? r.blob() : null;
}

function download(f) {
  const k = cacheKey(f);
  if (inflight.has(k)) return inflight.get(k);
  const p = (async () => {
    let lastErr;
    for (let i = 0; i < 3; i++) {
      try {
        const r = await fetch(apiUrl(`/${f[0]}`, { alt: "media", supportsAllDrives: "true" }));
        if (!r.ok) throw new Error(`Drive download failed (${r.status})`);
        const blob = await r.blob();
        const c = await caches.open(MEDIA_CACHE);
        await c.put(k, new Response(blob)).catch(() => {});
        trim();
        return blob;
      } catch (e) { lastErr = e; await new Promise(z => setTimeout(z, 600 * (i + 1))); }
    }
    throw lastErr;
  })();
  inflight.set(k, p);
  p.finally(() => inflight.delete(k));
  return p;
}

let trimming = false;
async function trim() {
  if (trimming) return;
  trimming = true;
  try {
    const c = await caches.open(MEDIA_CACHE);
    const keys = await c.keys();
    if (keys.length > MAX_ENTRIES) for (const k of keys.slice(0, keys.length - MAX_ENTRIES + 200)) await c.delete(k);
  } finally { trimming = false; }
}

function respondBlob(blob, name, range) {
  const size = blob.size;
  const base = { "content-type": typeFor(name), "accept-ranges": "bytes", "cache-control": "no-store" };
  const m = range && /bytes=(\d*)-(\d*)/.exec(range);
  if (m && (m[1] !== "" || m[2] !== "")) {
    let start, end;
    if (m[1] === "") { start = Math.max(0, size - Number(m[2])); end = size - 1; }
    else { start = Number(m[1]); end = m[2] ? Math.min(Number(m[2]), size - 1) : size - 1; }
    if (start >= size) return new Response(null, { status: 416, headers: { "content-range": `bytes */${size}` } });
    return new Response(blob.slice(start, end + 1), { status: 206, headers: {
      ...base, "content-range": `bytes ${start}-${end}/${size}`, "content-length": String(end - start + 1) } });
  }
  return new Response(blob, { status: 200, headers: { ...base, "content-length": String(size) } });
}

async function passthrough(f, name, range) {
  const headers = range ? { Range: range } : {};
  const r = await fetch(apiUrl(`/${f[0]}`, { alt: "media", supportsAllDrives: "true" }), { headers });
  if (!r.ok && r.status !== 206) throw new Error(`Drive download failed (${r.status})`);
  const out = new Headers({ "content-type": typeFor(name), "accept-ranges": "bytes", "cache-control": "no-store" });
  for (const h of ["content-length", "content-range"]) { const v = r.headers.get(h); if (v) out.set(h, v); }
  return new Response(r.body, { status: r.status, headers: out });
}

/* ---------------- Prefetch: everything a page references ---------------- */
const REF_RE = /["'`(=]\s*((?:\.{1,2}\/)?[^"'`()\s<>{}$]+?\.(?:png|jpe?g|gif|webp|svg|mp3|wav|m4a|ogg|mp4|webm|vtt|json|css|js))(?=["'`)?#\s])/gi;
function referencedPaths(html, dir) {
  const out = new Set();
  for (const m of html.matchAll(REF_RE)) {
    const ref = m[1];
    if (/^(https?:|data:|blob:|\/\/)/i.test(ref)) continue;
    const parts = (dir ? dir.split("/") : []);
    for (const seg of ref.split("/")) {
      if (seg === "..") parts.pop(); else if (seg !== "." && seg !== "") parts.push(seg);
    }
    out.add(parts.join("/"));
  }
  return out;
}

async function prefetch(day, htmlRel, html) {
  const tag = `${day.id}|${htmlRel}`;
  if (prefetched.has(tag)) return;
  prefetched.add(tag);
  const dir = htmlRel.includes("/") ? htmlRel.slice(0, htmlRel.lastIndexOf("/")) : "";
  const wanted = [...referencedPaths(html, dir)].filter(p => day.f[p]);
  // small files first so pictures and narration are ready before the big videos
  // videos come last, in the order the page first mentions them (title, intro, ... outro)
  const firstMention = new Map();
  for (const m of html.matchAll(REF_RE)) if (!firstMention.has(m[1])) firstMention.set(m[1], m.index);
  const isVid = p => /\.(mp4|webm)$/i.test(p);
  const pos = p => firstMention.get(dir ? p.slice(dir.length + 1) : p) ?? 1e9;
  const list = wanted.map(p => [p, day.f[p]]).sort((a, b) => {
    const va = isVid(a[0]), vb = isVid(b[0]);
    if (va !== vb) return va ? 1 : -1;
    return va ? pos(a[0]) - pos(b[0]) : a[1][1] - b[1][1];
  });
  let i = 0;
  const worker = async () => {
    while (i < list.length) {
      const [, f] = list[i++];
      try { if (!(await caches.open(MEDIA_CACHE).then(c => c.match(cacheKey(f))))) await download(f); } catch (e) {}
    }
  };
  await Promise.all(Array.from({ length: PREFETCH_CONCURRENCY }, worker));
}

/* ---------------- Request handling ---------------- */
function notFound(path, extra) {
  const body = `<!DOCTYPE html><meta charset="utf-8"><body style="font-family:system-ui;padding:40px;color:#334">
<h2 style="margin:0 0 8px">Not found in Drive</h2><p>${path.replace(/</g, "&lt;")}</p>
${extra ? `<pre style="white-space:pre-wrap;color:#a33">${String(extra).replace(/</g, "&lt;")}</pre>` : ""}</body>`;
  return new Response(body, { status: 404, headers: { "content-type": "text/html; charset=utf-8" } });
}

async function serve(event, url) {
  const request = event.request;
  if (!(await ensureUnlocked())) return locked();
  const segs = url.pathname.slice(VPREFIX.length).split("/").map(decodeURIComponent);
  const root = segs.shift();
  if (!LANG_BY_ROOT.has(root)) return notFound(segs.join("/"), "Unknown language folder");
  if (segs.length < 5) return notFound(segs.join("/"));
  const daySegs = segs.slice(0, 4);
  let rel = segs.slice(4).filter(s => s && s !== ".").join("/");
  if (!rel || url.pathname.endsWith("/")) rel = (rel ? rel + "/" : "") + "index.html";
  const isHtml = /\.html?$/i.test(rel);
  const isNav = request.mode === "navigate" || request.destination === "iframe" || request.destination === "document";
  const refresh = url.searchParams.has("r");

  let day = await getDay(root, daySegs, { fresh: refresh });
  if (!day) return notFound(segs.join("/"));
  let f = day.f[rel];
  if (!f && !day.checked) { await revalidate(day); f = day.f[rel]; }
  if (!f && day.d[rel]) return Response.redirect(url.origin + url.pathname.replace(/\/?$/, "/") + "index.html", 302);
  if (!f) return notFound(segs.join("/"));
  const name = rel.split("/").pop();
  const range = request.headers.get("range");

  if (isHtml) {
    // pages: always the newest copy (fast: html files are small)
    if (!day.checked && !refresh) event.waitUntil(revalidate(day).catch(() => {}));
    let blob;
    try { blob = await download(f); }
    catch (e) { await revalidate(day); f = day.f[rel]; if (!f) return notFound(segs.join("/")); blob = await download(f); }
    if (isNav) {
      const text = await blob.text();
      event.waitUntil(prefetch(day, rel, text).catch(() => {}));
      return new Response(text, { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
    }
    return respondBlob(blob, name, null);
  }

  const hit = await cached(f);
  if (hit) return respondBlob(hit, name, range);
  const k = cacheKey(f);
  const big = f[1] > 8 * 1024 * 1024;
  if (inflight.has(k) && (!range || !big)) {
    try { return respondBlob(await inflight.get(k), name, range); } catch (e) {}
  }
  if (range && big) {
    // stream the requested part now; the full file keeps downloading in the background
    event.waitUntil(download(f).catch(() => {}));
    try { return await passthrough(f, name, range); }
    catch (e) { await revalidate(day); f = day.f[rel]; if (!f) return notFound(segs.join("/")); return passthrough(f, name, range); }
  }
  try { return respondBlob(await download(f), name, range); }
  catch (e) {
    await revalidate(day); f = day.f[rel];
    if (!f) return notFound(segs.join("/"));
    return respondBlob(await download(f), name, range);
  }
}

self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin || !url.pathname.startsWith(VPREFIX)) return;
  if (event.request.method !== "GET" && event.request.method !== "HEAD") return;
  event.respondWith(serve(event, url).catch(err => notFound(url.pathname, err && err.message)));
});
