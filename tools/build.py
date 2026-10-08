#!/usr/bin/env python3
"""Build SmartPath Grade 1 English lessons.

Each lesson is written once in tools/lessons/<code>.py as plain content
(what Tala says, the pictures, the games). This script turns it into:

  SPT/ENG/GRADE1/Q?/WEEK?/DAY?/INTERACTIVE/index.html   the playable lesson
  .../INTERACTIVE/speech/_lines.json                     every line for TTS
  .../SCRIPT.md                                          readable teacher script

and checks the lesson against the "6-year-old rules" below. A lesson that
breaks a rule is reported; with --strict the build fails.

Usage:  python3 tools/build.py [lesson-code ...] [--strict]
"""
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
ENG = os.path.join(ROOT, "SPT", "ENG")

CHARS = {
    "TALA": "Tala", "ATE": "Ate Hinhin", "KUYA": "Kuya Gas",
    "BUNSO": "Bunso", "NANAY": "Nanay", "TATAY": "Tatay",
}

# Shared short feedback lines. Kept tiny and warm; never "wrong".
FX = {
    "good": ["Great job!", "Yes! You did it!", "Wonderful!", "Very good!"],
    "try": ["Almost! Try again.", "Look again. You can do it!"],
    "cheer": ["Hi! You are doing so well!", "I am happy to learn with you!"],
    "still": ["Good listening! Simon did not say it."],
    "oops": ["Oops! Simon did not say it. Stay still next time!"],
    "doit": ["Simon said it! Let us do it!"],
}

PASSIVE = {"cover", "story", "verse", "celebrate"}

# One look for every generated picture, matching the Tala character sheets.
ART_STYLE_CARD = (
    "Children's picture-book illustration for Filipino Grade 1 learners (age 6). Soft 2D cartoon style "
    "matching the Tala character sheet: rounded shapes, clean dark-brown outlines, warm pastel colours, "
    "gentle shading. ONE clear subject, centered, filling about 70% of the frame, on a plain soft cream "
    "background (#FFF8EC). No text, no letters, no numbers, no watermark, no extra objects. "
    "Square 1024x1024 PNG.")
ART_STYLE_SCENE = (
    "Wide storybook scene, 16:9, 1600x900, same soft 2D cartoon style as the Tala character sheet. "
    "Bright, clear and fully coloured (not faded), warm Filipino setting, the main characters large and "
    "easy to see in the middle third, simple uncluttered background. No text, no letters, no watermark.")
CHARACTERS_NOTE = (
    "Characters: Tala = Filipino girl, 6, dark brown pigtails, yellow T-shirt, blue denim overalls, white "
    "sneakers. Bunso = her little brother, 5, short dark hair, light-blue shirt, denim overalls. Kuya Gas = "
    "older brother, 11. Ate Hinhin = older sister, 10. Nanay = mother with glasses and yellow sweater. "
    "Tatay = father with glasses and navy shirt. Use the SHEET-*.png files in GRADE1/POSES as reference.")
CHECKS = {"pick", "order"}


def load(code):
    path = os.path.join(TOOLS, "lessons", code + ".py")
    spec = importlib.util.spec_from_file_location(code, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LESSON


def words(t):
    return len(re.findall(r"[A-Za-z0-9'’-]+", re.sub(r"\(pause(?:\s*\d+)?\)", " ", t or "")))


def sentences(t):
    t = re.sub(r"\(pause(?:\s*\d+)?\)", ".", t or "")
    return [s.strip() for s in re.split(r"[.!?]+", t) if s.strip()]


class Builder:
    def __init__(self, L, code):
        self.L = L
        self.code = code
        self.lines = {}          # file -> text
        self.problems = []
        g, q, w, d = L["grade"], L["quarter"], L["week"], L["day"]
        self.rel = os.path.join("GRADE%d" % g, "Q%d" % q, "WEEK%d" % w, "DAY%d" % d)
        self.out_dir = os.path.join(ENG, self.rel, "INTERACTIVE")
        self.grade_dir = os.path.join(ENG, "GRADE%d" % g)

    # ---------- helpers ----------
    def clip(self, name, text):
        name = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")
        if name in self.lines and self.lines[name] != text:
            raise SystemExit("%s: two different lines share the audio name %s" % (self.code, name))
        self.lines[name] = text
        return {"a": "speech/" + name, "t": text}

    def who(self, s):
        char = s.get("char", self.L.get("teacher", "TALA"))
        return {"char": char, "pose": s.get("pose", "waving.png"), "name": s.get("name", CHARS.get(char, char.title()))}

    def warn(self, where, msg):
        self.problems.append("%s: %s" % (where, msg))

    # ---------- build ----------
    def build(self):
        L = self.L
        slides = []
        self.art = []
        for i, src in enumerate(L["slides"]):
            s = dict(src)
            self.resolve_art(s, i + 1)
            sid = s.get("id") or "s%02d" % (i + 1)
            s["id"] = sid
            s["who"] = self.who(s)
            for k in ("char", "pose", "name"):
                s.pop(k, None)
            s["passive"] = s["type"] in PASSIVE
            if s.get("say"):
                s["narration"] = self.clip(sid, s.pop("say"))
            t = s["type"]
            if t in ("cards", "langs"):
                for j, it in enumerate(s["items"]):
                    it["clip"] = self.clip("%s-%d" % (sid, j + 1), it.pop("say", it.get("word")))
            elif t == "word":
                s["clip"] = self.clip(sid + "-word", s.pop("wordSay", s["word"]))
            elif t == "sentence":
                for j, o in enumerate(s["options"]):
                    full = "%s %s%s" % (s["pre"], o["word"], s.get("post", ""))
                    o["clip"] = self.clip("%s-%d" % (sid, j + 1), o.pop("say", full.strip()))
            elif t == "pick":
                for r, rd in enumerate(s["rounds"]):
                    rd["clip"] = self.clip("%s-q%d" % (sid, r + 1), rd.pop("askSay", rd["ask"]))
                    if rd.get("yesSay"):
                        rd["yesClip"] = self.clip("%s-q%d-yes" % (sid, r + 1), rd.pop("yesSay"))
                    if rd.get("hintSay"):
                        rd["hintClip"] = self.clip("%s-q%d-hint" % (sid, r + 1), rd.pop("hintSay"))
            elif t == "order":
                for j, it in enumerate(s["items"]):
                    it["clip"] = self.clip("%s-%d" % (sid, j + 1), it.pop("say", it["word"]))
                s["askClips"] = [self.clip("%s-ask%d" % (sid, j + 1), a) for j, a in enumerate(s["ask"])]
                if s.get("yesSay"):
                    s["yesClip"] = self.clip(sid + "-yes", s.pop("yesSay"))
            elif t == "act":
                for j, c in enumerate(s["cmds"]):
                    default = ("Simon says, " + c["word"]) if (s.get("simon") and c.get("simon")) else c["word"]
                    c["clip"] = self.clip("%s-%d" % (sid, j + 1), c.pop("say", default))
            elif t == "chant":
                for j, ln in enumerate(s["lines"]):
                    ln["clip"] = self.clip("%s-%d" % (sid, j + 1), ln.pop("say", ln["text"]))
            elif t == "talk":
                if s.get("example"):
                    ex = s["example"]
                    ex["clip"] = self.clip(sid + "-example", ex.pop("say", ex["text"]))
            elif t == "verse":
                s["verseClip"] = self.clip(sid + "-verse", s.pop("verseSay", "%s (pause) %s." % (s["verse"], s["ref"])))
            slides.append(s)

        fx = {}
        for kind, texts in FX.items():
            fx[kind] = [self.clip("fx-%s-%d" % (kind, n + 1), t) for n, t in enumerate(texts)]

        g, q, w, d = L["grade"], L["quarter"], L["week"], L["day"]
        label = "Quarter %d • Week %d • Day %d" % (q, w, d)
        runtime = {
            "code": self.code,
            "title": L["title"],
            "label": label,
            "bg": L["bg"],
            "posesRoot": "../../../../POSES",
            "nextHref": L.get("next"),
            "slides": slides,
            "fx": fx,
        }
        self.check(runtime)
        self.write(runtime, label)
        return runtime

    # ---------- pictures still to be generated ----------
    def resolve_art(self, s, n):
        """An "art" entry names a picture to generate. If the file is there, use it;
        otherwise keep the placeholder picture and list the prompt in IMAGE_PROMPTS.md."""
        objs = [s]
        for key in ("items", "options", "cmds"):
            objs += s.get(key, [])
        for rd in s.get("rounds", []):
            objs += rd["choices"]
        for o in objs:
            art = o.pop("art", None)
            if not art:
                continue
            f = art["file"]
            ready = os.path.exists(os.path.join(self.out_dir, f))
            if ready:
                o["img"] = f
                o.pop("pose", None)
            label = o.get("word") or o.get("title") or s.get("title", "")
            if not any(a["file"] == f for a in self.art):
                self.art.append({"file": f, "prompt": art["prompt"], "scene": art.get("scene", False),
                                 "slide": n, "label": label, "ready": ready})

    def write_prompts(self):
        path = os.path.join(ENG, self.rel, "IMAGE_PROMPTS.md")
        if not self.art:
            if os.path.exists(path):
                os.remove(path)
            return
        todo = [a for a in self.art if not a["ready"]]
        out = ["# Pictures to generate — %s" % self.L["title"], "",
               "%d of %d still needed. Save each picture with the exact file name below "
               "(inside `INTERACTIVE/`), then run `python3 tools/build.py`; the lesson picks it up "
               "automatically. Until then a placeholder is shown." % (len(todo), len(self.art)), "",
               "**Characters.** " + CHARACTERS_NOTE.replace("Characters: ", ""), ""]
        for a in self.art:
            style = ART_STYLE_SCENE if a["scene"] else ART_STYLE_CARD
            out += ["## %s `%s`" % ("DONE" if a["ready"] else "NEEDED", a["file"]),
                    "Slide %d — %s" % (a["slide"], a["label"]), "",
                    "```", a["prompt"].strip() + " " + style, "```", ""]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out))

    # ---------- the 6-year-old rules ----------
    def check(self, R):
        sl = R["slides"]
        types = [s["type"] for s in sl]
        if types[0] != "cover":
            self.warn("structure", "first slide must be the cover")
        if types[-1] != "celebrate" or types[-2] != "verse":
            self.warn("structure", "lesson must end with verse then celebrate")
        goals = sl[0].get("goals", [])
        if not 2 <= len(goals) <= 3:
            self.warn("cover", "2 or 3 goals only (found %d)" % len(goals))
        for g in goals:
            if words(g) > 7:
                self.warn("cover", "goal too long for a child: %r" % g)
        if not 10 <= len(sl) <= 18:
            self.warn("structure", "aim for 10-18 slides (found %d)" % len(sl))
        interactive = [t for t in types if t not in PASSIVE]
        if len(interactive) < 6:
            self.warn("structure", "needs at least 6 hands-on slides (found %d)" % len(interactive))
        if sum(1 for t in types if t in CHECKS) < 2:
            self.warn("structure", "needs at least 2 understanding checks (pick/order)")
        run = 0
        for i, t in enumerate(types[1:-2], 1):
            run = run + 1 if t in PASSIVE else 0
            if run > 3:
                self.warn("slide %d" % (i + 1), "more than 3 listen-only slides in a row; add a tap game")
        covered = set()
        for i, s in enumerate(sl):
            where = "slide %d (%s)" % (i + 1, s["id"])
            if s.get("goal"):
                covered.add(s["goal"])
            nar = s.get("narration", {}).get("t", "")
            if not nar:
                self.warn(where, "no narration")
            if words(nar) > 75:
                self.warn(where, "narration %d words; keep under 75 (about 30 seconds)" % words(nar))
            for sen in sentences(nar):
                if words(sen) > 14:
                    self.warn(where, "long sentence (%d words): %r" % (words(sen), sen))
            screen = []
            if s.get("title"):
                screen.append(("title", s["title"], 8))
            for it in s.get("items", []) + s.get("options", []) + s.get("cmds", []):
                screen.append(("word", it.get("word", ""), 6 if s["type"] in ("sentence", "order") else 4))
                if it.get("sub"):
                    screen.append(("sub", it["sub"], 6))
            for ln in s.get("lines", []):
                screen.append(("line", ln if isinstance(ln, str) else ln["text"], 12))
            if s.get("mean"):
                screen.append(("meaning", s["mean"], 10))
            for rd in s.get("rounds", []):
                screen.append(("question", rd["ask"], 9))
                for c in rd["choices"]:
                    screen.append(("choice", c["word"], 4))
            for kind, text, cap in screen:
                if words(text) > cap:
                    self.warn(where, "%s too long (%d words, max %d): %r" % (kind, words(text), cap, text))
                if "[" in text or "alert(" in text:
                    self.warn(where, "no phonetic spellings or pop-ups: %r" % text)
            for img in self.images(s):
                p = os.path.normpath(os.path.join(self.out_dir, img))
                if not os.path.exists(p):
                    self.warn(where, "missing picture %s" % img)
            pose = os.path.join(self.grade_dir, "POSES", s["who"]["char"], s["who"]["pose"])
            if not os.path.exists(pose):
                self.warn(where, "missing pose %s/%s" % (s["who"]["char"], s["who"]["pose"]))
        for n in range(1, len(goals) + 1):
            if n not in covered:
                self.warn("goals", "goal %d is not practised by any slide (tag slides with goal=%d)" % (n, n))
        bg = os.path.normpath(os.path.join(self.out_dir, R["bg"]))
        if not os.path.exists(bg):
            self.warn("lesson", "missing background %s" % R["bg"])

    def images(self, s):
        out = []
        for k in ("img", "bg"):
            if s.get(k):
                out.append(s[k])
        lists = s.get("items", []) + s.get("options", []) + s.get("cmds", [])
        for rd in s.get("rounds", []):
            lists += rd["choices"]
        for it in lists:
            if it.get("img"):
                out.append(it["img"])
            if it.get("pose"):
                out.append("../../../../POSES/" + it["pose"])
        return out

    # ---------- output ----------
    def write(self, R, label):
        os.makedirs(os.path.join(self.out_dir, "speech"), exist_ok=True)
        engine = os.path.join(TOOLS, "engine")
        css = open(os.path.join(engine, "base.css"), encoding="utf-8").read() + "\n" + \
            open(os.path.join(engine, "extra.css"), encoding="utf-8").read()
        js = open(os.path.join(engine, "player.js"), encoding="utf-8").read()
        shell = open(os.path.join(engine, "shell.html"), encoding="utf-8").read()
        first = R["slides"][0]["who"]
        html = (shell
                .replace("{{TITLE}}", "Grade 1 English • %s" % R["title"])
                .replace("{{TITLE_SHORT}}", R["title"])
                .replace("{{LABEL}}", label)
                .replace("{{SOURCE}}", self.code + ".py")
                .replace("{{START_POSE}}", "../../../../POSES/%s/%s" % (first["char"], first["pose"]))
                .replace("{{CSS}}", css)
                .replace("{{LESSON_JSON}}", json.dumps(R, ensure_ascii=False, indent=1).replace("</", "<\\/"))
                .replace("{{PLAYER_JS}}", js))
        with open(os.path.join(self.out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        with open(os.path.join(self.out_dir, "speech", "_lines.json"), "w", encoding="utf-8") as f:
            json.dump(self.lines, f, ensure_ascii=False, indent=1)
        self.write_script(R, label)
        self.write_prompts()

    def write_script(self, R, label):
        L = self.L
        out = ["# %s" % R["title"], "", "Grade 1 English · %s · `%s`" % (label, self.code), ""]
        out += ["## Objectives (the child will...)", ""]
        out += ["%d. %s" % (i + 1, g) for i, g in enumerate(R["slides"][0]["goals"])]
        if L.get("source"):
            out += ["", "Source: %s" % L["source"]]
        out += ["", "## Slides", ""]
        for i, s in enumerate(R["slides"]):
            out.append("### %d. %s — %s (%s)" % (i + 1, s.get("title", s["type"]), s["type"],
                                                s["who"]["name"]))
            if s.get("narration"):
                out.append("> %s" % s["narration"]["t"])
            for key in ("items", "options", "cmds", "lines"):
                for it in s.get(key, []):
                    if isinstance(it, dict) and it.get("clip"):
                        out.append("- tap **%s** → \"%s\"" % (it.get("word") or it.get("text"), it["clip"]["t"]))
            for rd in s.get("rounds", []):
                ok = [c["word"] for c in rd["choices"] if c.get("ok")]
                out.append("- check: %s → **%s**" % (rd["ask"], ", ".join(ok)))
            out.append("")
        with open(os.path.join(ENG, self.rel, "SCRIPT.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(out))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    codes = args or sorted(f[:-3] for f in os.listdir(os.path.join(TOOLS, "lessons"))
                           if f.endswith(".py") and not f.startswith("_"))
    bad = 0
    for code in codes:
        b = Builder(load(code), code)
        R = b.build()
        status = "OK " if not b.problems else "FIX"
        need = sum(1 for a in b.art if not a["ready"])
        print("[%s] %s  %d slides, %d voice lines, %d pictures to generate -> %s"
              % (status, code, len(R["slides"]), len(b.lines), need, b.rel))
        for p in b.problems:
            print("      - " + p)
        bad += bool(b.problems)
    write_menu()
    if strict and bad:
        sys.exit(1)


def write_menu():
    """PLAY-LESSONS.html at the repo root: one big button per lesson."""
    rows = []
    for code in sorted(f[:-3] for f in os.listdir(os.path.join(TOOLS, "lessons"))
                       if f.endswith(".py") and not f.startswith("_")):
        L = load(code)
        rel = "SPT/ENG/GRADE%d/Q%d/WEEK%d/DAY%d/INTERACTIVE/index.html" % (L["grade"], L["quarter"], L["week"], L["day"])
        rows.append((L["week"], L["day"], L["title"], rel, "SPT/ENG/GRADE%d/Q%d/WEEK%d/DAY%d/SCRIPT.md" %
                     (L["grade"], L["quarter"], L["week"], L["day"])))
    if os.path.exists(os.path.join(ENG, "GRADE1/Q1/WEEK1/DAY1/INTERACTIVE/index.html")):
        rows.append((1, 1, "Myself and My Family (original)", "SPT/ENG/GRADE1/Q1/WEEK1/DAY1/INTERACTIVE/index.html", None))
    rows.sort()
    cards = "\n".join(
        '<div><a class="card" href="%s"><span class="tag">Week %d · Day %d</span><span class="t">%s</span></a>%s</div>'
        % (rel, w, d, title, ('<a class="script" href="%s">teacher script</a>' % sc) if sc else "")
        for w, d, title, rel, sc in rows)
    html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grade 1 English Lessons</title>
<style>
body{margin:0;font-family:'Fredoka','Nunito',system-ui,sans-serif;background:#FFF4E4;color:#1E1B18;padding:32px 16px}
h1{text-align:center;color:#92400E;font-size:40px;margin:0 0 6px}
p.sub{text-align:center;color:#6B7280;font-size:18px;margin:0 0 28px}
.grid{max-width:900px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}
.card{display:flex;flex-direction:column;gap:6px;background:#fff;border:4px solid #FDE68A;border-radius:24px;padding:20px 22px;
text-decoration:none;color:inherit;box-shadow:0 8px 18px rgba(0,0,0,.08)}
.card:hover{border-color:#F59E0B;transform:translateY(-3px)}
.tag{font-size:15px;font-weight:800;color:#B45309;letter-spacing:.5px;text-transform:uppercase}
.t{font-size:24px;font-weight:800}
.script{display:inline-block;font-size:14px;color:#0F766E;margin:8px 0 0 22px}
</style></head><body>
<h1>Grade 1 English · Quarter 1</h1>
<p class="sub">Tap a lesson to play. Use Chrome or Safari. Sound on!</p>
<div class="grid">
%s
</div></body></html>
""" % cards
    with open(os.path.join(ROOT, "PLAY-LESSONS.html"), "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main()
