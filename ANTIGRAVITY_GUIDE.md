# SmartPath English — Full Guide for Google Antigravity (local Mac)

This guide is for **you** and for the **Antigravity agent** on your Mac.
The Claude cloud session built the lesson system and 5 sample lessons, then stopped because of usage.
Everything below is done **locally**: audit all Grade 1–3 lessons, rewrite them, generate the pictures and
the Leda voices, put every file in the right folder, check, and upload to Google Drive.

---

## 0. The big picture (read once)

```
GitHub repo  smartpathtutordev/mit-dit-courses   branch  claude/sweet-faraday-n5v9he
│
├── tools/                    ← the lesson SYSTEM (code). Never put pictures/voices here.
│   ├── lessons/g1q1w1d2.py   ← ONE FILE PER LESSON: the script, games, pictures (content only)
│   ├── engine/               ← the player (look and feel = Week 1 Day 1)
│   ├── build.py              ← turns lessons/*.py into playable index.html + checks the rules
│   ├── audit.py              ← audits every Grade 1–3 lesson → AUDIT_REPORT.md
│   ├── tts_gemini.py         ← makes the voices (Gemini preview TTS, voice Leda)
│   └── playtest.js           ← plays every lesson in a browser and reports problems
├── HANDOFF.md                ← rules + what each lesson must do
├── ANTIGRAVITY_GUIDE.md      ← this file
├── IMAGE_PROMPTS_ALL.md/.json← every picture still to generate (prompt + exact save path)
└── SPT/ENG/GRADE1/...        ← a COPY of the Drive lessons (only Q1 W1–W2 + poses)

Your Mac ENG folder (the real lessons, all grades), e.g.
/Volumes/SPT Externa/ALL MODULES/ENG/GRADE1/Q1/WEEK1/DAY2/
├── SCRIPT.md                 ← readable teacher script (generated)
├── IMAGE_PROMPTS.md          ← pictures still needed for this lesson (generated)
└── INTERACTIVE/
    ├── index.html            ← the playable lesson (generated — never edit by hand)
    ├── media/                ← pictures. New generated pictures go in media/art/
    │   └── art/<name>.png
    └── speech/               ← voices: <name>.mp3, plus _lines.json (the text of every clip)
```

**Golden rule:** edit only `tools/lessons/*.py`, then run `python3 tools/build.py`. Pictures go in
`INTERACTIVE/media/art/`, voices go in `INTERACTIVE/speech/`. The build picks them up automatically.

---

## 1. Get the cloud work onto your Mac (one time)

Open **Terminal** on the Mac (or ask the Antigravity agent to run these):

```bash
cd ~
git clone -b claude/sweet-faraday-n5v9he https://github.com/smartpathtutordev/mit-dit-courses.git
cd mit-dit-courses
```
(No git? Open the repo on github.com → branch `claude/sweet-faraday-n5v9he` → **Code → Download ZIP**, unzip
to `~/mit-dit-courses`.)

Tell the tools where your real ENG folder is. It is on your **external drive**; your old scripts used
`/Volumes/SPT Externa/ALL MODULES/ENG`. Check the exact name first (plug the drive in):
```bash
ls /Volumes/                                  # shows the drive name, e.g. "SPT Externa"
ls "/Volumes/SPT Externa/ALL MODULES/ENG"     # must show GRADE1  GRADE2  GRADE3 ...
```
If the name is different, use your path in the two lines below. The drive must be plugged in whenever you
build, audit, generate or play.

```bash
export SPT_ENG_ROOT="/Volumes/SPT Externa/ALL MODULES/ENG"
echo 'export SPT_ENG_ROOT="/Volumes/SPT Externa/ALL MODULES/ENG"' >> ~/.zshrc   # remember it
```

**Back up first** (once):
```bash
cp -R "$SPT_ENG_ROOT" "${SPT_ENG_ROOT}_BACKUP_$(date +%Y%m%d)"
```

Copy the 5 rebuilt sample lessons (and the placeholder crops they use) from the repo into the real folder:
```bash
rsync -av --exclude '._*' --exclude 'POSES' --exclude 'KID-PLAYER' --exclude 'styles' \
  SPT/ENG/GRADE1/Q1/ "$SPT_ENG_ROOT/GRADE1/Q1/"
python3 tools/build.py          # rebuilds straight into $SPT_ENG_ROOT
```

Install the checker once: `npm i -g playwright && npx playwright install chromium` and `pip3 install pillow`.

---

## 2. Audit ALL lessons (Grade 1 → 3)

```bash
python3 tools/audit.py
open AUDIT_REPORT.md
```
`AUDIT_REPORT.md` lists every lesson (≈384) with its status:
- **KEEP (gold standard)** — Grade 1 Q1 W1 D1 only.
- **REBUILT** — already done with the new system (passes the rules).
- **REBUILD** — must be rewritten; the issues column says why (pictures that don't exist, faded pictures used
  as content, broken audio like `speech/._age-talk.mp3`, pop-ups, phonetic spellings, long adult sentences,
  one-screen stubs…).

`AUDIT_REPORT.json` → `content` holds each old lesson's words, titles, story lines, the pictures it uses and the
pictures in its folder, so the agent can rewrite it without opening the old HTML.

**Order of work:** Grade 1 Q1 (W2 D3 → W8 D4) → Grade 1 Q2 → Q3 → Q4 → Grade 2 → Grade 3.
Do one **week** at a time, check it, then continue.

---

## 3. Rewrite a lesson (the script) — what "good" means

The owner's feedback: *"the script isn't good, it's not interconnected and there is no good transition
between slides; images don't support the lesson; stories aren't complete."* Every lesson must:

### 3.1 Be a correct DepEd lesson
- Follow the DepEd source for that day. Search Google Drive for the lesson deck / narration script:
  `LANG{grade}Q{q}W{w}DAY{d}` (e.g. `LANG1Q1W2DAY3LESSON`, `LANG1Q1W1DAY2NARRATIONSCRIPT`). Google Docs/Slides
  are only shortcuts on the Mac — open them in the browser or export as .txt/.pdf into
  `<ENG>/GRADE?/Q?/WEEK?/DAY?/source/`. The verse picture `LANG1-Q1Wx-DAYy.png` in each WEEK folder gives the
  day's Bible verse. If no DepEd source exists, use the old lesson's topic from `AUDIT_REPORT.json`.
- Grade level: Grade 1 = age 6, Grade 2 = age 7, Grade 3 = age 8. Grades 2–3 may use slightly longer sentences
  (change the limits in `build.py` → `check()` per grade if needed) but the same design.

### 3.2 Be interconnected (one flowing lesson, not separate slides)
- **Cover** recalls yesterday and says today's 2–3 goals ("Yesterday we… Today we…").
- **Every slide has a `bridge`** — one short line that links it to the slide before
  ("You know the five words! Now let us move our bodies."). The build FAILS without it.
- **One thread** runs through the lesson: the same characters and setting from start to end; the words taught
  first are the words used in the story, the games, and the child's own sentence.
- **Stories are complete**: beginning → problem → what they do → ending → lesson, one picture per beat,
  a quick check (`pick`) every 2–3 story pages.
- **Spiral review**: reuse 1–2 words from earlier days in each new lesson.
- **Celebration** recaps the 3 goals and previews tomorrow ("Tomorrow we will…"); the verse connects to the
  story's value.

### 3.3 Be easy and fun for a child (enforced by build.py)
10–20 slides · 2–3 goals ≤7 words · teacher sentences ≤14 words, ≤75 words per slide · card words ≤4 words ·
≥6 hands-on slides · ≥2 checks (`pick`/`order`) · never >3 listen-only slides in a row · no phonetic
spellings, no pop-ups, no "wrong" · listen first, then "Your turn!".

### 3.4 Every part has a picture that supports it
Cover, every story page, every word card, every answer choice, talk slide and verse need a picture that shows
exactly what is said. Use an existing picture **only if it truly matches** (check the contact sheet). Otherwise
add an `art` entry with a prompt. Backgrounds (`"bg"`) must be a clear, full-colour room/scene — never a faded one.

### 3.5 How to write the file
Copy a finished lesson (e.g. `tools/lessons/g1q1w2d1.py`) to `tools/lessons/g{G}q{Q}w{W}d{D}.py` and replace the
content. Slide types: `cover, cards, word, sentence, story, pick, order, act (simon=True), chant, talk, langs,
verse, celebrate`. A picture to generate looks like:

```python
"art": {"file": "media/art/pina-kitchen.png",
        "prompt": "Inside a cosy nipa-hut kitchen: Pina pouting... (what to draw, who, where, doing what)",
        "scene": True}      # True = 16:9 story scene, omit = square card picture
```
Reuse the same `file` name for the same picture (one picture, many slides). For pictures shared across
lessons, point at the other lesson's file: `"../../DAY4/INTERACTIVE/media/art/body-feet.png"`.

Then:
```bash
python3 tools/build.py g1q1w2d3 --strict      # must print [OK ]
```

---

## 4. Generate the PICTURES

After writing lessons, run `python3 tools/build.py`. It writes:
- `IMAGE_PROMPTS_ALL.json` (repo root) — machine list: `save_to`, `shape`, full `prompt`.
- `IMAGE_PROMPTS_ALL.md` — the same as a table for people.
- `<lesson>/IMAGE_PROMPTS.md` — the list for one lesson.

For each item in `IMAGE_PROMPTS_ALL.json → images`:
1. Generate the picture in Antigravity (Gemini image / Nano Banana) with the **full `prompt`** text.
   **Attach the character sheets** as reference so Tala, Bunso, Nanay… always look the same:
   `$SPT_ENG_ROOT/GRADE1/POSES/SHEET-TALA.png` (and SHEET-BUNSO / NANAY / TATAY / ATE / KUYA). If the sheets are
   not in your ENG folder, they are in Drive `SPT/ENG/GRADE1/POSES/`.
2. Size: square → 1024×1024; scene (16:9) → 1600×900. PNG.
3. Save to **`$SPT_ENG_ROOT/` + `save_to`**, exactly that path and file name
   (e.g. `GRADE1/Q1/WEEK1/DAY3/INTERACTIVE/media/art/pina-kitchen.png`). Create `media/art/` if needed.
4. Look at it: does a 6-year-old instantly see what the slide says? Right character? No text/letters in the
   picture? If not, regenerate.
5. Run `python3 tools/build.py` — the item disappears from the "to generate" list and the lesson uses it.

---

## 5. Generate the VOICES (Gemini preview TTS, voice **Leda** — not Chirp3)

Every lesson has `INTERACTIVE/speech/_lines.json` = `{ "clip-name": "text to say", ... }`.
The lesson plays `INTERACTIVE/speech/<clip-name>.mp3` (or `.wav`).

**Option A (recommended, automatic):**
```bash
export GEMINI_API_KEY=...            # from https://aistudio.google.com/apikey
brew install ffmpeg                  # optional: makes small .mp3 instead of .wav
python3 tools/tts_gemini.py                      # all lessons; skips clips that already exist
python3 tools/tts_gemini.py GRADE1/Q1/WEEK2      # just one week
```
It uses model `gemini-2.5-flash-preview-tts`, voice `Leda`, warm slow teacher style, and turns `(pause)` into
real pauses. Add `--force` to remake clips after editing a lesson's words.

**Option B (generate inside Antigravity by hand):** for every key in `_lines.json`, generate speech with the
**Gemini preview TTS model, voice Leda**, style: *"You are Tala, a kind Filipino teacher talking to one
six-year-old child. Speak slowly, warmly and clearly."* Replace `(pause)` with a short pause. Save as
`INTERACTIVE/speech/<key>.mp3` (or `.wav`, 24 kHz mono). File names must match the keys exactly.

**When a lesson's text changes**, `build.py` rewrites `_lines.json`; re-make only the changed clips
(delete their old .mp3 first, or run with `--force` for that lesson folder).

Until a clip exists the lesson uses the browser voice, so lessons are always playable.

---

## 6. Check everything

```bash
python3 tools/build.py --strict                                  # rules: every lesson [OK ]
NODE_PATH=$(npm root -g) node tools/playtest.js --shots ~/Desktop/lesson-shots   # plays every lesson
python3 tools/audit.py                                            # statuses move to REBUILT
open PLAY-LESSONS.html                                            # play them yourself (Chrome/Safari, sound on)
```
Look through `~/Desktop/lesson-shots` (one screenshot per slide) for any picture that does not match.

---

## 7. Upload to Google Drive

- If `SPT_ENG_ROOT` **is** your Google Drive for desktop folder, it syncs by itself — done.
- If it is the external drive, upload the changed lesson folders into Drive `SPT/ENG/GRADE?/Q?/WEEK?/DAY?/`
  (keep the same structure). Only upload `SCRIPT.md`, `IMAGE_PROMPTS.md` and the `INTERACTIVE/` folder
  (`index.html`, `media/`, `speech/`). Never upload `._*` files: `find "$SPT_ENG_ROOT" -name '._*' -delete`.

## 8. Save the work back to GitHub (so any AI can continue)

```bash
cd ~/mit-dit-courses
git add tools/ HANDOFF.md ANTIGRAVITY_GUIDE.md AUDIT_REPORT.md AUDIT_REPORT.json IMAGE_PROMPTS_ALL.*
git commit -m "Rebuild Grade 1 Q1 Week N lessons"
git push
```
Pictures and voices live in the ENG folder / Drive (too big for git). Update the **Status** table in
`HANDOFF.md` after each finished week.

---

## 9. Copy-paste prompt for the Antigravity agent

> You are continuing the SmartPath English lesson rebuild. Repo: `~/mit-dit-courses` (branch
> `claude/sweet-faraday-n5v9he`). Lessons folder: `$SPT_ENG_ROOT` (= `/Volumes/SPT Externa/ALL MODULES/ENG`).
> Read `HANDOFF.md` and `ANTIGRAVITY_GUIDE.md` fully first. Then:
> 1. Run `python3 tools/audit.py` and read `AUDIT_REPORT.md`.
> 2. Take the next week marked REBUILD (start Grade 1 Q1 Week 2 Day 3). For each day: find the DepEd source,
>    contact-sheet the day's `INTERACTIVE/media`, write `tools/lessons/g{G}q{Q}w{W}d{D}.py` following section 3
>    (correct DepEd content, cover recalls yesterday, a `bridge` on every slide, complete story with a picture
>    per beat, checks every 2–3 pages, every slide/card/choice has a matching picture or an `art` prompt,
>    celebration previews tomorrow). Run `python3 tools/build.py <code> --strict` until `[OK ]`.
> 3. Generate every picture in `IMAGE_PROMPTS_ALL.json` (section 4), attaching the POSES/SHEET-*.png character
>    sheets, and save each to `$SPT_ENG_ROOT/<save_to>`.
> 4. Generate the voices with Gemini preview TTS voice Leda (section 5).
> 5. Run the checks (section 6), fix anything reported, update the Status table in HANDOFF.md, commit and push
>    (section 8). Show me the week's lessons (PLAY-LESSONS.html) before starting the next week.
> Never hand-edit a generated index.html. Never use Chirp3. Never use a faded picture as content.

---

## 10. Troubleshooting

| Problem | Fix |
|---|---|
| `build.py` says `missing picture media/...` | The file is not in that lesson's `INTERACTIVE/media/`; copy it there or use an `art` prompt. |
| A generated picture does not show | File name/path must match `save_to` exactly (lower-case, `.png`), then re-run `build.py`. |
| No voice, only robot voice | The `.mp3` for that clip is missing; run `tts_gemini.py` for that folder. |
| `tts_gemini.py` says busy (429) | Free-tier limit; it waits and retries. Leave it running or run one week at a time. |
| Lesson opens but no sound at all | Press the green **Start!** button (browsers need one tap before sound). |
| Menu links broken | Re-run `python3 tools/build.py` after setting `SPT_ENG_ROOT`. |
| `._something` files everywhere | macOS junk from the external drive: `find "$SPT_ENG_ROOT" -name '._*' -delete`. |
