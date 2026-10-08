#!/usr/bin/env python3
"""Audit every English lesson (Grade 1-3) and say what each one needs.

Scans <ENG>/GRADE*/Q*/WEEK*/DAY*/INTERACTIVE/index.html and checks the things
that broke the old lessons: pictures that do not exist, faded pictures used as
content, broken or macOS-junk audio paths, pop-ups, phonetic spellings, long
adult sentences, too few slides, no rebuild yet. It also pulls out the words,
titles and story lines it can find so the agent rewriting the lesson has the
old content in one place.

  export SPT_ENG_ROOT="/Volumes/SPT Externa/ALL MODULES/ENG"   # or leave unset for repo SPT/ENG
  python3 tools/audit.py                # writes AUDIT_REPORT.md + AUDIT_REPORT.json at the repo root
  python3 tools/audit.py GRADE1/Q1      # only part of the tree
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENG = os.environ.get("SPT_ENG_ROOT") or os.path.join(ROOT, "SPT", "ENG")

try:
    from PIL import Image, ImageStat
except ImportError:          # the audit still runs, it just cannot spot faded pictures
    Image = None

MEDIA_RE = re.compile(r"""(?:\.\./)*(?:[\w-]+/)*media/[\w.\-/]+\.(?:png|jpe?g|webp)""", re.I)
AUDIO_RE = re.compile(r"""speech/[^"'`\s)]+\.(?:mp3|wav)""", re.I)
TEXT_RE = re.compile(r"""(?:word|title|label|caption|text|mean|meaning|desc|sub|line|prompt|model|ask)\s*["']?\s*:\s*["']([^"'\n]{2,200})["']""")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def faded(path):
    """True for washed-out background art (low saturation and low contrast)."""
    if not Image:
        return False
    try:
        import warnings
        warnings.filterwarnings("ignore")
        im = Image.open(path).convert("RGB")
        im.thumbnail((200, 200))
        hsv = im.convert("HSV")
        sat = ImageStat.Stat(hsv).mean[1] / 255
        con = ImageStat.Stat(im.convert("L")).stddev[0] / 255
        return sat < 0.16 and con < 0.17
    except Exception:
        return False


def audit_day(day_dir):
    rel = os.path.relpath(day_dir, ENG)
    inter = os.path.join(day_dir, "INTERACTIVE")
    html_path = os.path.join(inter, "index.html")
    r = {"lesson": rel, "issues": [], "content": {}}
    if not os.path.exists(html_path):
        r["status"] = "MISSING"
        r["issues"].append("no INTERACTIVE/index.html")
        return r
    html = open(html_path, encoding="utf-8", errors="replace").read()
    t = re.search(r"<title>([^<]*)", html)
    r["title"] = t.group(1).strip() if t else ""
    r["size_kb"] = round(len(html) / 1024)
    rebuilt = "GENERATED FILE: edit tools/lessons" in html
    r["slides"] = len(re.findall(r"""["']?type["']?\s*:\s*["'][a-z_\-]+["']""", html))

    imgs = sorted(set(MEDIA_RE.findall(html)))
    missing = [i for i in imgs if not os.path.exists(os.path.normpath(os.path.join(inter, i)))]
    fade = [i for i in imgs if i not in missing and faded(os.path.normpath(os.path.join(inter, i)))]
    audios = sorted(set(AUDIO_RE.findall(html)))
    junk = [a for a in audios if "/._" in a or a.startswith("speech/._")]
    amiss = [a for a in audios if a not in junk and not os.path.exists(os.path.join(inter, a))]
    texts = [m.strip() for m in TEXT_RE.findall(html)]
    long_t = [x for x in texts if len(x.split()) > 14]

    if missing:
        r["issues"].append("%d pictures do not exist: %s" % (len(missing), ", ".join(missing[:8])))
    if fade:
        r["issues"].append("%d faded/washed-out pictures (fine as background only): %s" % (len(fade), ", ".join(fade[:6])))
    if junk:
        r["issues"].append("audio points at macOS junk files: %s" % ", ".join(junk[:4]))
    if amiss and not rebuilt:
        r["issues"].append("%d audio files missing" % len(amiss))
    if "alert(" in html:
        r["issues"].append("uses alert() pop-ups")
    if re.search(r"\[\s*[A-Za-z]+(?:-[A-Za-z]+)+\s*\]", html):
        r["issues"].append("phonetic spellings like [dih-SKUH-ver-ee]")
    if EMOJI_RE.search(html):
        r["issues"].append("emoji in the lesson")
    if long_t:
        r["issues"].append("%d on-screen texts longer than 14 words, e.g. %r" % (len(long_t), long_t[0][:90]))
    if r["slides"] < 10:
        r["issues"].append("only %d slides (one-screen stub or too short)" % r["slides"])
    if not rebuilt:
        r["issues"].append("not rebuilt with tools/build.py yet")

    if rel.replace(os.sep, "/") == "GRADE1/Q1/WEEK1/DAY1":
        r["status"] = "KEEP (gold standard)"
        r["issues"] = []
        return r
    r["status"] = "REBUILT" if rebuilt and len(r["issues"]) == 0 else ("REBUILT-CHECK" if rebuilt else "REBUILD")
    r["content"] = {
        "texts": list(dict.fromkeys(texts))[:120],
        "pictures_used": imgs,
        "pictures_in_folder": sorted(f for f in os.listdir(os.path.join(inter, "media"))
                                     if not f.startswith("._")) if os.path.isdir(os.path.join(inter, "media")) else [],
        "verse_png": sorted(f for f in os.listdir(os.path.dirname(day_dir)) if f.lower().endswith(".png")
                            and not f.startswith("._")),
    }
    return r


def main():
    sub = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = os.path.join(ENG, sub[0]) if sub else ENG
    days = []
    for d, dirs, _ in os.walk(base):
        dirs[:] = sorted(x for x in dirs if not x.startswith("._") and x not in ("POSES", "styles", "js", "KID-PLAYER", "scratch", "_FIXED"))
        if re.search(r"GRADE\d/Q\d/WEEK\d+/DAY\d$", d.replace(os.sep, "/")):
            days.append(d)
            dirs[:] = []

    def key(p):
        return [int(x) for x in re.findall(r"\d+", os.path.relpath(p, ENG))]
    days.sort(key=key)
    results = [audit_day(d) for d in days]
    with open(os.path.join(ROOT, "AUDIT_REPORT.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, ensure_ascii=False)
    count = {}
    for r in results:
        count[r["status"]] = count.get(r["status"], 0) + 1
    out = ["# English lessons audit", "", "Folder: `%s`" % ENG, "",
           "Totals: " + ", ".join("%s %d" % kv for kv in sorted(count.items())), "",
           "REBUILD = write `tools/lessons/<code>.py` for it (see ANTIGRAVITY_GUIDE.md).  "
           "Old content per lesson is in AUDIT_REPORT.json → content.", "",
           "| Lesson | Title | Slides | KB | Status | Issues |", "|---|---|---|---|---|---|"]
    for r in results:
        out.append("| %s | %s | %s | %s | %s | %s |" % (r["lesson"], r.get("title", "").replace("|", "/"), r.get("slides", ""),
                   r.get("size_kb", ""), r["status"], "<br>".join(i.replace("|", "/") for i in r["issues"])))
    with open(os.path.join(ROOT, "AUDIT_REPORT.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Audited %d lessons: %s" % (len(results), count))
    print("Wrote AUDIT_REPORT.md and AUDIT_REPORT.json")


if __name__ == "__main__":
    main()
