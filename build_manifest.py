#!/usr/bin/env python3
"""Builds the portal's file index from Google Drive.

Writes:
  <out>/tree.json                      grade/quarter/week/day navigation for every language
  <out>/m/<LANG>/<dayKey>.json         every file and folder inside one DAY folder

Usage: build_manifest.py <config.js> <out_dir> [referer]
"""
import json, os, re, socket, sys, time, urllib.parse, urllib.request

# Cloud Shell has no working IPv6 route; force IPv4 so requests don't hang.
_gai = socket.getaddrinfo
socket.getaddrinfo = lambda host, port, family=0, *a, **k: _gai(host, port, socket.AF_INET, *a, **k)
from concurrent.futures import ThreadPoolExecutor

cfg_text = open(sys.argv[1], encoding="utf-8").read()
OUT = sys.argv[2]
REFERER = sys.argv[3] if len(sys.argv) > 3 else "https://smartpath-math-review.web.app/"
API_KEY = re.search(r'apiKey:\s*"([^"]*)"', cfg_text).group(1)
API_BASE = re.search(r'apiBase:\s*"([^"]*)"', cfg_text).group(1)
LANGS = re.findall(r'\{\s*code:\s*"([^"]+)",\s*label:\s*"([^"]+)",\s*folderId:\s*"([^"]+)"', cfg_text)
FOLDER = "application/vnd.google-apps.folder"
pool = ThreadPoolExecutor(32)


def natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def day_key(segs):
    return "__".join(re.sub(r"[^A-Za-z0-9]+", "_", s) for s in segs)


def ls(folder_id):
    files, token = {}, ""
    while True:
        q = {"q": f"'{folder_id}' in parents and trashed=false",
             "fields": "nextPageToken,files(id,name,mimeType,size,modifiedTime)",
             "pageSize": "1000", "supportsAllDrives": "true", "includeItemsFromAllDrives": "true", "key": API_KEY}
        if token:
            q["pageToken"] = token
        req = urllib.request.Request(API_BASE + "?" + urllib.parse.urlencode(q), headers={"Referer": REFERER})
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=25) as r:
                    j = json.load(r)
                break
            except Exception as e:  # rate limits / transient errors
                if attempt == 5:
                    raise
                time.sleep(1.5 * (attempt + 1))
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


def main():
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
        with ThreadPoolExecutor(8) as dp:
            counts = list(dp.map(do_day, days_todo))
        total_days += len(days_todo)
        total_files += sum(counts)
        print(f"{code}: {len(days_todo)} days, {sum(counts)} files, {time.time() - t0:.0f}s", flush=True)
    with open(os.path.join(OUT, "tree.json"), "w", encoding="utf-8") as fh:
        json.dump(tree, fh, separators=(",", ":"))
    print(f"TOTAL {total_days} days, {total_files} files")


if __name__ == "__main__":
    main()
