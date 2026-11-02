// Encrypts the portal's secret files with the portal password.
// Usage: node encrypt.js <public_dir> <password> <salt_b64>
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const [dir, password, salt] = process.argv.slice(2);
if (!dir || !password || !salt) { console.error("usage: node encrypt.js <dir> <password> <salt_b64>"); process.exit(1); }
const ITER = 250000;
const key = crypto.pbkdf2Sync(password, Buffer.from(salt, "base64"), ITER, 32, "sha256");

function box(text) {
  const iv = crypto.randomBytes(12);
  const c = crypto.createCipheriv("aes-256-gcm", key, iv);
  const ct = Buffer.concat([c.update(Buffer.from(text, "utf8")), c.final(), c.getAuthTag()]);
  return { v: 1, iv: iv.toString("base64"), d: ct.toString("base64") };
}
function encFile(f) {
  const text = fs.readFileSync(f, "utf8");
  try { if (JSON.parse(text).v === 1) return 0; } catch (e) {}
  fs.writeFileSync(f, JSON.stringify(box(text)));
  return 1;
}

let n = encFile(path.join(dir, "tree.json"));
const walk = d => { for (const e of fs.readdirSync(d, { withFileTypes: true })) {
  const p = path.join(d, e.name);
  if (e.isDirectory()) walk(p); else if (e.name.endsWith(".json")) n += encFile(p);
} };
walk(path.join(dir, "m"));

const cfgPath = path.join(dir, "config.js");
let cfg = fs.readFileSync(cfgPath, "utf8");
const m = /apiKey:\s*"([^"]+)"/.exec(cfg);
if (!m) { console.error("config.js has no apiKey to protect"); process.exit(1); }
cfg = cfg.replace(m[0], 'apiKey: ""');
cfg += `\nself.PORTAL_VAULT = ${JSON.stringify({ salt, iter: ITER, check: box("smartpath-ok"), apiKey: box(m[1]) })};\n`;
fs.writeFileSync(cfgPath, cfg);
console.log(`encrypted ${n} files; Drive key removed from config.js`);
