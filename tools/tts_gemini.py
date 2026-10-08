#!/usr/bin/env python3
"""Make every voice clip with Gemini preview TTS, voice "Leda".

Reads speech/_lines.json in each lesson (written by tools/build.py) and
writes speech/<name>.mp3 next to it. Clips that already exist are skipped,
so you can stop and re-run any time. If ffmpeg is not installed the clip is
saved as .wav instead (the lesson player plays either).

Needs a Gemini API key:   export GEMINI_API_KEY=...   (aistudio.google.com/apikey)

Usage:
  python3 tools/tts_gemini.py                      # every lesson
  python3 tools/tts_gemini.py GRADE1/Q1/WEEK1      # one folder
  python3 tools/tts_gemini.py --force              # re-make all clips
  python3 tools/tts_gemini.py --model gemini-2.5-pro-preview-tts
"""
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENG = os.path.join(ROOT, "SPT", "ENG")
VOICE = "Leda"
MODEL = "gemini-2.5-flash-preview-tts"

STYLE_LONG = ("You are Tala, a kind Filipino teacher talking to one six-year-old child. "
              "Speak slowly, warmly and clearly, with a gentle smile in your voice. "
              "Where you see '...' take a short breath and pause. Read exactly this:\n")
STYLE_SHORT = ("Say this slowly, clearly and cheerfully to a six-year-old child, "
               "exactly as written:\n")


def prep(text):
    t = re.sub(r"\(pause\s*\d+\)", " ... ... ", text)
    t = re.sub(r"\(pause\)", " ... ", t)
    return re.sub(r"\s+", " ", t).strip()


def synth(text, key, model):
    body = {
        "contents": [{"parts": [{"text": (STYLE_LONG if len(text.split()) > 6 else STYLE_SHORT) + prep(text)}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}},
        },
    }
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % model
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read())
            part = data["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(part["data"])
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:300]
            if e.code in (429, 500, 503) and attempt < 5:
                wait = 20 * (attempt + 1)
                print("      busy (%d), waiting %ds..." % (e.code, wait))
                time.sleep(wait)
                continue
            raise SystemExit("Gemini TTS error %d: %s" % (e.code, msg))
        except (KeyError, IndexError):
            if attempt < 5:
                time.sleep(5)
                continue
            raise SystemExit("Gemini returned no audio for: %r" % text)


def save(pcm, base):
    wav = base + ".wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(pcm)
    if shutil.which("ffmpeg"):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav,
                        "-af", "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                               "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                               "apad=pad_dur=0.25",
                        "-ac", "1", "-b:a", "64k", base + ".mp3"], check=True)
        os.remove(wav)
        return base + ".mp3"
    return wav


def main():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise SystemExit("Set GEMINI_API_KEY first (get one at https://aistudio.google.com/apikey).")
    args = sys.argv[1:]
    force = "--force" in args
    model = MODEL
    if "--model" in args:
        model = args[args.index("--model") + 1]
    paths = [a for a in args if not a.startswith("--") and a != model]
    roots = [os.path.join(ENG, p) for p in paths] or [ENG]
    manifests = []
    for r in roots:
        for d, _, files in os.walk(r):
            if "_lines.json" in files and d.endswith("speech"):
                manifests.append(os.path.join(d, "_lines.json"))
    total = made = 0
    for m in sorted(manifests):
        lines = json.load(open(m, encoding="utf-8"))
        d = os.path.dirname(m)
        print("%s  (%d clips)" % (os.path.relpath(d, ENG), len(lines)))
        for name, text in lines.items():
            total += 1
            base = os.path.join(d, name)
            if not force and (os.path.exists(base + ".mp3") or os.path.exists(base + ".wav")):
                continue
            pcm = synth(text, key, model)
            out = save(pcm, base)
            made += 1
            print("   + %s" % os.path.basename(out))
    print("Done: %d new clips, %d total." % (made, total))


if __name__ == "__main__":
    main()
