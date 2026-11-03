/* Password vault helpers shared by the page and the service worker.
   Secret files (Drive key, lesson list, file index) are stored AES-GCM encrypted;
   the key is derived from the portal password with PBKDF2-SHA256. */
self.SPTVault = (() => {
  const b64d = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
  const b64e = u8 => btoa(String.fromCharCode(...u8));
  async function derive(password, salt, iter) {
    const base = await crypto.subtle.importKey("raw", new TextEncoder().encode(password), "PBKDF2", false, ["deriveBits"]);
    const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", salt: b64d(salt), iterations: iter, hash: "SHA-256" }, base, 256);
    return new Uint8Array(bits);
  }
  async function decrypt(rawKey, box) {
    const k = await crypto.subtle.importKey("raw", rawKey, "AES-GCM", false, ["decrypt"]);
    const pt = await crypto.subtle.decrypt({ name: "AES-GCM", iv: b64d(box.iv) }, k, b64d(box.d));
    return new TextDecoder().decode(pt);
  }
  const isBox = o => o && typeof o === "object" && o.v === 1 && typeof o.iv === "string" && typeof o.d === "string";
  // Reads JSON that may be an encrypted box.
  async function openJson(rawKey, obj) {
    return isBox(obj) ? JSON.parse(await decrypt(rawKey, obj)) : obj;
  }
  return { b64d, b64e, derive, decrypt, isBox, openJson };
})();

/* Paths a lesson page refers to by relative path (shared by the page's upload check). */
self.SPTRefs = (() => {
  const RE = /["'`(=]\s*((?:\.{1,2}\/)?[^"'`()\s<>{}$]+?\.(?:png|jpe?g|gif|webp|svg|mp3|wav|m4a|ogg|mp4|webm|vtt|json|css|js))(?=["'`)?#\s])/gi;
  function referenced(html, dir) {
    const out = new Set();
    for (const m of html.matchAll(RE)) {
      const ref = m[1];
      if (/^(https?:|data:|blob:|\/\/)/i.test(ref)) continue;
      const parts = dir ? dir.split("/") : [];
      for (const seg of ref.split("/")) {
        if (seg === "..") parts.pop(); else if (seg !== "." && seg !== "") parts.push(seg);
      }
      out.add(parts.join("/"));
    }
    return out;
  }
  return { referenced };
})();
