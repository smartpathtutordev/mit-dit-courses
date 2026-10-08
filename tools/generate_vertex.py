#!/usr/bin/env python3
"""Generate every picture and voice clip with Google Vertex AI and save each
one exactly where the lessons expect it. Nothing to decide: all prompts and
lines are already written (IMAGE_PROMPTS_ALL.json and speech/_lines.json,
produced by tools/build.py).

Pictures: Vertex AI Gemini image model (default gemini-2.5-flash-image), with
          the character sheets attached so Tala & family always look the same.
Voices:   Cloud Text-to-Speech, Gemini preview TTS model, voice "Leda".

Setup (once):
  gcloud auth login && gcloud auth application-default login
  gcloud config set project YOUR_PROJECT_ID
  gcloud services enable aiplatform.googleapis.com texttospeech.googleapis.com
  export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
  export SPT_ENG_ROOT="/Volumes/SPT Externa/ALL MODULES/ENG"
  pip3 install pillow           # optional: exact picture sizes

Run:
  python3 tools/generate_vertex.py                 # pictures + voices, everything missing
  python3 tools/generate_vertex.py --images        # only pictures
  python3 tools/generate_vertex.py --voices        # only voices
  python3 tools/generate_vertex.py --only GRADE1/Q1/WEEK3   # one part of the tree
  python3 tools/generate_vertex.py --dry-run       # list what would be made
  python3 tools/generate_vertex.py --force         # remake even if the file exists
Then:  python3 tools/build.py   (lessons switch to the new pictures automatically)
"""
import base64
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENG = os.environ.get("SPT_ENG_ROOT") or os.path.join(ROOT, "SPT", "ENG")
PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
IMAGE_MODEL = os.environ.get("SPT_IMAGE_MODEL", "gemini-2.5-flash-image")
IMAGE_LOCATION = os.environ.get("SPT_IMAGE_LOCATION", "global")
TTS_MODEL = os.environ.get("SPT_TTS_MODEL", "gemini-2.5-flash-preview-tts")
VOICE = "Leda"
TTS_STYLE = ("You are Tala, a kind Filipino teacher talking to one young child (age 6 to 8). "
             "Speak slowly, warmly and clearly, with a smile in your voice. Pause where you see '...'.")
SHEETS = {"Tala": "TALA", "Bunso": "BUNSO", "Nanay": "NANAY", "Tatay": "TATAY", "Ate": "ATE", "Kuya": "KUYA"}

_token = {"v": None, "t": 0}


def token():
    if _token["v"] and time.time() - _token["t"] < 2400:
        return _token["v"]
    for cmd in (["gcloud", "auth", "application-default", "print-access-token"], ["gcloud", "auth", "print-access-token"]):
        try:
            v = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
            if v:
                _token.update(v=v, t=time.time())
                return v
        except Exception:
            continue
    raise SystemExit("No Google Cloud login. Run: gcloud auth application-default login")


def post(url, body):
    for attempt in range(6):
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers={
            "Authorization": "Bearer " + token(), "Content-Type": "application/json", "x-goog-user-project": PROJECT})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:400]
            if e.code == 401:
                _token["v"] = None
            if e.code in (401, 429, 500, 503) and attempt < 5:
                wait = 15 * (attempt + 1)
                print("      busy (%d), retry in %ds" % (e.code, wait))
                time.sleep(wait)
                continue
            raise RuntimeError("HTTP %d: %s" % (e.code, msg))
    raise RuntimeError("gave up after retries")


# ---------------------------------------------------------------- pictures
def sheet_parts(prompt):
    parts = []
    for name, folder in SHEETS.items():
        if re.search(r"\b%s\b" % name, prompt):
            for base in (os.path.join(ENG, "GRADE1", "POSES"), os.path.join(ROOT, "SPT", "ENG", "GRADE1", "POSES")):
                p = os.path.join(base, "SHEET-%s.png" % folder)
                if os.path.exists(p):
                    parts.append({"inlineData": {"mimeType": "image/png", "data": base64.b64encode(open(p, "rb").read()).decode()}})
                    break
    return parts[:3]


def make_image(item, out):
    wide = item["shape"].startswith("16:9")
    refs = sheet_parts(item["prompt"])
    text = item["prompt"]
    if refs:
        text = ("Use the attached character sheet(s) only as the reference for how the characters look "
                "(same face, hair, clothes, art style). Do not copy the sheet layout. ") + text
    body = {"contents": [{"role": "user", "parts": refs + [{"text": text}]}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": "16:9" if wide else "1:1"}}}
    url = ("https://aiplatform.googleapis.com/v1/projects/%s/locations/%s/publishers/google/models/%s:generateContent"
           % (PROJECT, IMAGE_LOCATION, IMAGE_MODEL))
    data = post(url, body)
    for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            raw = base64.b64decode(part["inlineData"]["data"])
            os.makedirs(os.path.dirname(out), exist_ok=True)
            try:
                from PIL import Image
                im = Image.open(io.BytesIO(raw)).convert("RGB")
                size = (1600, 900) if wide else (1024, 1024)
                im = im.resize(size, Image.LANCZOS)
                im.save(out, "PNG")
            except ImportError:
                open(out, "wb").write(raw)
            return True
    raise RuntimeError("no image returned (maybe blocked by safety filter): %s" % str(data)[:300])


def images(only, force, dry):
    path = os.path.join(ROOT, "IMAGE_PROMPTS_ALL.json")
    if not os.path.exists(path):
        raise SystemExit("IMAGE_PROMPTS_ALL.json missing: run python3 tools/build.py first")
    items = json.load(open(path, encoding="utf-8"))["images"]
    done = made = failed = 0
    for it in items:
        rel = it["save_to"]
        if only and not rel.startswith(only):
            continue
        out = os.path.normpath(os.path.join(ENG, rel))
        if os.path.exists(out) and not force:
            done += 1
            continue
        print("  picture  %s" % rel)
        if dry:
            continue
        try:
            make_image(it, out)
            made += 1
        except Exception as e:
            failed += 1
            print("      FAILED: %s" % e)
    print("Pictures: %d made, %d already there, %d failed" % (made, done, failed))


# ---------------------------------------------------------------- voices
def prep(text):
    t = re.sub(r"\(pause\s*\d+\)", " ... ... ", text)
    t = re.sub(r"\(pause\)", " ... ", t)
    return re.sub(r"\s+", " ", t).strip()


def make_voice(text, out):
    body = {"input": {"prompt": TTS_STYLE, "text": prep(text)},
            "voice": {"languageCode": "en-US", "name": VOICE, "modelName": TTS_MODEL},
            "audioConfig": {"audioEncoding": "MP3", "speakingRate": 0.95}}
    data = post("https://texttospeech.googleapis.com/v1/text:synthesize", body)
    open(out, "wb").write(base64.b64decode(data["audioContent"]))


def voices(only, force, dry):
    made = done = failed = 0
    for d, _, files in os.walk(ENG):
        if "_lines.json" not in files or not d.endswith("speech"):
            continue
        rel = os.path.relpath(d, ENG).replace(os.sep, "/")
        if only and not rel.startswith(only):
            continue
        lines = json.load(open(os.path.join(d, "_lines.json"), encoding="utf-8"))
        print("  voices   %s (%d clips)" % (rel, len(lines)))
        for name, text in lines.items():
            out = os.path.join(d, name + ".mp3")
            if os.path.exists(out) and not force:
                done += 1
                continue
            if dry:
                continue
            try:
                make_voice(text, out)
                made += 1
            except Exception as e:
                failed += 1
                print("      FAILED %s: %s" % (name, e))
    print("Voices: %d made, %d already there, %d failed" % (made, done, failed))


def main():
    a = sys.argv[1:]
    only = a[a.index("--only") + 1].strip("/") if "--only" in a else ""
    force, dry = "--force" in a, "--dry-run" in a
    want_img = "--voices" not in a
    want_voice = "--images" not in a
    if not PROJECT and not dry:
        raise SystemExit("Set GOOGLE_CLOUD_PROJECT first (your Vertex AI project id).")
    print("ENG folder: %s" % ENG)
    if want_img:
        images(only, force, dry)
    if want_voice:
        voices(only, force, dry)
    print("Now run: python3 tools/build.py")


if __name__ == "__main__":
    main()
