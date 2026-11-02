/* Service worker: serves  <scope>/v/<rootFolderId>/<path inside Drive>
   by resolving the path to a Drive file and streaming it from the Drive API.
   This lets each module's index.html load its assets/, speech/ and videos/
   by the same relative paths it uses on disk. */
importScripts("config.js");
const CFG = self.PORTAL_CONFIG;
const VPREFIX = new URL("v/", self.registration.scope).pathname;
const ROOTS = new Set(CFG.languages.map(l => l.folderId));
const MEDIA_CACHE = "spt-media-v1";
const CACHEABLE_MAX = 15 * 1024 * 1024;

const listCache = new Map(); // folderId -> {t, p}

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("message", e => {
  if (e.data === "flush") { listCache.clear(); caches.delete(MEDIA_CACHE); }
});

function apiUrl(path, params) {
  const u = new URL(CFG.apiBase + path);
  for (const [k, v] of Object.entries(params || {})) u.searchParams.set(k, v);
  u.searchParams.set("key", CFG.apiKey);
  return u.toString();
}

function listFolder(id) {
  const hit = listCache.get(id);
  if (hit && Date.now() - hit.t < (CFG.listTtl || 300) * 1000) return hit.p;
  const p = (async () => {
    const byName = new Map();
    let pageToken = "";
    do {
      const params = {
        q: `'${id}' in parents and trashed=false`,
        fields: "nextPageToken,files(id,name,mimeType,size,modifiedTime)",
        pageSize: "1000",
        supportsAllDrives: "true",
        includeItemsFromAllDrives: "true"
      };
      if (pageToken) params.pageToken = pageToken;
      const r = await fetch(apiUrl("", params));
      if (!r.ok) throw new Error(`Drive list failed (${r.status}): ${(await r.text()).slice(0, 300)}`);
      const j = await r.json();
      for (const f of j.files || []) {
        if (f.name.startsWith("._") || f.name === ".DS_Store") continue;
        const prev = byName.get(f.name);
        if (!prev || prev.modifiedTime < f.modifiedTime) byName.set(f.name, f);
      }
      pageToken = j.nextPageToken || "";
    } while (pageToken);
    return byName;
  })();
  listCache.set(id, { t: Date.now(), p });
  p.catch(() => listCache.delete(id));
  return p;
}

async function findChild(folderId, name) {
  const m = await listFolder(folderId);
  if (m.has(name)) return m.get(name);
  const lower = name.toLowerCase();
  for (const [k, v] of m) if (k.toLowerCase() === lower) return v;
  return null;
}

async function resolve(rootId, segs) {
  let cur = { id: rootId, mimeType: "application/vnd.google-apps.folder" };
  for (const s of segs) {
    if (cur.mimeType !== "application/vnd.google-apps.folder") return null;
    cur = await findChild(cur.id, s);
    if (!cur) return null;
  }
  return cur;
}

const TYPES = {
  html: "text/html; charset=utf-8", htm: "text/html; charset=utf-8", css: "text/css",
  js: "text/javascript", mjs: "text/javascript", json: "application/json",
  png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif",
  webp: "image/webp", svg: "image/svg+xml", mp3: "audio/mpeg", wav: "audio/wav",
  m4a: "audio/mp4", ogg: "audio/ogg", mp4: "video/mp4", webm: "video/webm",
  woff: "font/woff", woff2: "font/woff2", ttf: "font/ttf", txt: "text/plain; charset=utf-8",
  vtt: "text/vtt"
};
function typeFor(name, fallback) {
  const ext = (name.split(".").pop() || "").toLowerCase();
  return TYPES[ext] || fallback || "application/octet-stream";
}

function notFound(path, extra) {
  const body = `<!DOCTYPE html><meta charset="utf-8"><body style="font-family:system-ui;padding:40px;color:#334">
<h2 style="margin:0 0 8px">Not found in Drive</h2><p>${path.replace(/</g, "&lt;")}</p>
${extra ? `<pre style="white-space:pre-wrap;color:#a33">${String(extra).replace(/</g, "&lt;")}</pre>` : ""}</body>`;
  return new Response(body, { status: 404, headers: { "content-type": "text/html; charset=utf-8" } });
}

async function serve(request, url) {
  let rest = url.pathname.slice(VPREFIX.length);
  const segs = rest.split("/").map(s => decodeURIComponent(s));
  const rootId = segs.shift();
  if (!ROOTS.has(rootId)) return notFound(rest, "Unknown root folder");
  if (segs.length === 0 || segs[segs.length - 1] === "") {
    if (segs.length) segs.pop();
    segs.push("index.html");
  }
  const clean = segs.filter(s => s && s !== ".");
  let file;
  try { file = await resolve(rootId, clean); }
  catch (err) { return notFound(clean.join("/"), err.message); }
  if (!file) return notFound(clean.join("/"));
  if (file.mimeType === "application/vnd.google-apps.folder") {
    return Response.redirect(url.href.replace(/\/?$/, "/") + "index.html", 302);
  }

  const range = request.headers.get("range");
  const size = Number(file.size || 0);
  const cacheKey = `https://cache.local/${file.id}/${file.modifiedTime}`;
  const isHtml = /\.html?$/i.test(file.name);
  const cacheable = !isHtml && size > 0 && size <= CACHEABLE_MAX;

  if (cacheable && (!range || /^bytes=0-$/.test(range))) {
    const cache = await caches.open(MEDIA_CACHE);
    const hit = await cache.match(cacheKey);
    if (hit) return hit;
    if (!range) {
      const r = await fetch(apiUrl(`/${file.id}`, { alt: "media", supportsAllDrives: "true" }));
      if (!r.ok) return notFound(clean.join("/"), `Drive download failed (${r.status})`);
      const blob = await r.blob();
      const resp = new Response(blob, { status: 200, headers: {
        "content-type": typeFor(file.name, file.mimeType), "content-length": String(blob.size),
        "accept-ranges": "bytes", "cache-control": "no-store" } });
      cache.put(cacheKey, resp.clone()).catch(() => {});
      return resp;
    }
  }

  const headers = {};
  if (range) headers["Range"] = range;
  const r = await fetch(apiUrl(`/${file.id}`, { alt: "media", supportsAllDrives: "true" }), { headers });
  if (!r.ok && r.status !== 206) {
    return notFound(clean.join("/"), `Drive download failed (${r.status}): ${(await r.text()).slice(0, 300)}`);
  }
  const out = new Headers({ "content-type": typeFor(file.name, file.mimeType), "accept-ranges": "bytes", "cache-control": "no-store" });
  for (const h of ["content-length", "content-range"]) { const v = r.headers.get(h); if (v) out.set(h, v); }
  if (!out.has("content-length") && size && r.status === 200) out.set("content-length", String(size));
  if (r.status === 206 && !out.has("content-range") && size) {
    const m = /bytes=(\d+)-(\d*)/.exec(range || "");
    if (m) out.set("content-range", `bytes ${m[1]}-${m[2] || size - 1}/${size}`);
  }
  return new Response(r.body, { status: r.status, headers: out });
}

self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin || !url.pathname.startsWith(VPREFIX)) return;
  if (event.request.method !== "GET" && event.request.method !== "HEAD") return;
  event.respondWith(serve(event.request, url).catch(err => notFound(url.pathname, err && err.message)));
});
