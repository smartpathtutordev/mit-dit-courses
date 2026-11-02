#!/usr/bin/env python3
"""Builds the portal's file index from Google Drive.

Writes:
  <out>/tree.json                      grade/quarter/week/day navigation for every language
  <out>/m/<LANG>/<dayKey>.json         every file and folder inside one DAY folder

Usage: build_manifest.py <config.js> <out_dir> [referer]
"""
import json, os, re, socket, sys, threading, time, urllib.error, urllib.parse, urllib.request

# Cloud Shell's DNS is slow: resolve each host once (IPv4) and reuse the answer.
_gai = socket.getaddrinfo
_dns = {}
def _cached_gai(host, port, family=0, *a, **k):
    key = (host, port)
    if key not in _dns:
        _dns[key] = _gai(host, port, socket.AF_INET, *a, **k)
    return _dns[key]
socket.getaddrinfo = _cached_gai
from concurrent.futures import ThreadPoolExecutor

cfg_text = open(sys.argv[1], encoding="utf-8").read()
OUT = sys.argv[2]
REFERER = sys.argv[3] if len(sys.argv) > 3 else "https://smartpath-math-review.web.app/"
API_KEY = re.search(r'apiKey:\s*"([^"]*)"', cfg_text).group(1)
API_BASE = re.search(r'apiBase:\s*"([^"]*)"', cfg_text).group(1)
LANGS = re.findall(r'\{\s*code:\s*"([^"]+)",\s*label:\s*"([^"]+)",\s*folderId:\s*"([^"]+)"', cfg_text)
FOLDER = "application/vnd.google-apps.folder"
pool = ThreadPoolExecutor(16)


def natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def day_key(segs):
    return "__".join(re.sub(r"[^A-Za-z0-9]+", "_", s) for s in segs)


_local = threading.local()
STATS = {"calls": 0, "retries": 0, "last_error": ""}


def _session():
    sess = getattr(_local, "s", None)
    if sess is None:
        import requests  # keep-alive connections: no DNS/TLS setup per call
        sess = _local.s = requests.Session()
        sess.headers["Referer"] = REFERER
    return sess


def _get_json(params):
    try:
        r = _session().get(API_BASE, params=params, timeout=30)
        return r.status_code, (r.json() if r.content else {})
    except ImportError:
        req = urllib.request.Request(API_BASE + "?" + urllib.parse.urlencode(params), headers={"Referer": REFERER})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.load(r)
        except urllib.error.HTTPError as e:
            return e.code, {"error": {"message": e.read().decode()[:200]}}


def ls(folder_id):
    files, token = {}, ""
    while True:
        q = {"q": f"'{folder_id}' in parents and trashed=false",
             "fields": "nextPageToken,files(id,name,mimeType,size,modifiedTime)",
             "pageSize": "1000", "supportsAllDrives": "true", "includeItemsFromAllDrives": "true", "key": API_KEY}
        if token:
            q["pageToken"] = token
        for attempt in range(8):
            STATS["calls"] += 1
            try:
                status, j = _get_json(q)
            except Exception as e:
                status, j = 0, {"error": {"message": str(e)}}
            if status == 200:
                break
            STATS["retries"] += 1
            STATS["last_error"] = f"{status} {str(j.get('error', {}).get('message', ''))[:120]}"
            if attempt == 7:
                raise RuntimeError(STATS["last_error"])
            time.sleep(min(20, 1.0 * 2 ** attempt))
        for f in j.get("files", []):
            n = f["name"]
            if n.startswith("._") or n == ".DS_Store":
                continue
            prev = files.get(n)
            if not prev or prev.get("modifiedTime", "") < f.get("modifiedTime", ""):
                files[n] = f
        token = j.get("nextPageToken")
        if not token:
            return files


def subdirs(files):
    return sorted([f for f in files.values() if f["mimeType"] == FOLDER], key=lambda f: natkey(f["name"]))


def crawl_day(day_id):
    """Lists everything under a DAY folder, one level at a time in parallel."""
    out_files, out_dirs = {}, {"": day_id}
    frontier = [("", day_id)]
    while frontier:
        results = list(pool.map(lambda pf: (pf[0], ls(pf[1])), frontier))
        frontier = []
        for prefix, files in results:
            for f in files.values():
                rel = f"{prefix}/{f['name']}" if prefix else f["name"]
                if f["mimeType"] == FOLDER:
                    out_dirs[rel] = f["id"]
                    frontier.append((rel, f["id"]))
                else:
                    out_files[rel] = [f["id"], int(f.get("size") or 0), f.get("modifiedTime", "")]
    return out_files, out_dirs


def _ticker():
    t0 = time.time()
    while True:
        time.sleep(15)
        print(f"  ...{time.time() - t0:.0f}s, {STATS['calls']} Drive calls, {STATS['retries']} retries {STATS['last_error']}", flush=True)


def main():
    threading.Thread(target=_ticker, daemon=True).start()
    os.makedirs(OUT, exist_ok=True)
    tree = {"built": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "languages": {}}
    total_days = total_files = 0
    for code, label, root in LANGS:
        t0 = time.time()
        grades = []
        days_todo = []
        for g in subdirs(ls(root)):
            qs = list(pool.map(lambda q: (q, ls(q["id"])), subdirs(ls(g["id"]))))
            gnode = {"name": g["name"], "quarters": []}
            for q, qfiles in qs:
                weeks = list(pool.map(lambda w: (w, ls(w["id"])), subdirs(qfiles)))
                qnode = {"name": q["name"], "weeks": []}
                for w, wfiles in weeks:
                    wnode = {"name": w["name"], "days": []}
                    for d in subdirs(wfiles):
                        wnode["days"].append(d["name"])
                        days_todo.append(([g["name"], q["name"], w["name"], d["name"]], d["id"]))
                    qnode["weeks"].append(wnode)
                gnode["quarters"].append(qnode)
            grades.append(gnode)
        tree["languages"][code] = {"folderId": root, "grades": grades}
        print(f"{code}: navigation read ({len(days_todo)} days, {time.time() - t0:.0f}s); indexing files...", flush=True)
        os.makedirs(os.path.join(OUT, "m", code), exist_ok=True)

        def do_day(item):
            segs, did = item
            files, dirs = crawl_day(did)
            with open(os.path.join(OUT, "m", code, day_key(segs) + ".json"), "w", encoding="utf-8") as fh:
                json.dump({"id": did, "f": files, "d": dirs}, fh, separators=(",", ":"))
            return len(files)

        # day crawls run several at a time; each one fans out internally
        with ThreadPoolExecutor(6) as dp:
            counts = list(dp.map(do_day, days_todo))
        total_days += len(days_todo)
        total_files += sum(counts)
        print(f"{code}: {len(days_todo)} days, {sum(counts)} files, {time.time() - t0:.0f}s", flush=True)
    with open(os.path.join(OUT, "tree.json"), "w", encoding="utf-8") as fh:
        json.dump(tree, fh, separators=(",", ":"))
    print(f"TOTAL {total_days} days, {total_files} files")


if __name__ == "__main__":
    main()
