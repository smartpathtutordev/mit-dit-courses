# SmartPath English — Guide for Google Antigravity (local Mac)

**Status when Claude stopped (out of usage):** 11 lessons are fully written by Claude (Grade 1 Q1: W1 D2–D4,
W2 D1–D3, W4 D1, W7 D1–D2, W8 D1–D2) plus the original W1 D1. Their pictures and voices are ready to generate
(sections 1–4). **All other lessons still need writing** — section 7 tells Antigravity how, using the same
system and rules, so the quality matches.

**Who does what**
- **Claude (cloud)** writes everything: every lesson script, every voice line, every picture prompt, and the exact
  file name and folder for each. These are in the GitHub repo.
- **Antigravity (your Mac)** only: (1) gets the repo, (2) connects to **Google Vertex AI** and generates the
  pictures and the Leda voices, (3) saves them in the right folders on the external drive, (4) checks, (5) uploads
  to Google Drive. **Antigravity does not write or change lesson content.**

---

## 1. One-time setup on the Mac

Plug in the external drive and check the path (it must list GRADE1, GRADE2, GRADE3):
```bash
ls "/Volumes/SPT Externa/ALL MODULES/ENG"
```
If the drive name is different, use your path everywhere below.

```bash
# get Claude's work
cd ~
git clone -b claude/sweet-faraday-n5v9he https://github.com/smartpathtutordev/mit-dit-courses.git
cd mit-dit-courses

# tell the tools where the lessons live
echo 'export SPT_ENG_ROOT="/Volumes/SPT Externa/ALL MODULES/ENG"' >> ~/.zshrc
echo 'export GOOGLE_CLOUD_PROJECT="YOUR-VERTEX-PROJECT-ID"' >> ~/.zshrc
source ~/.zshrc

# Google Cloud login + APIs (Vertex AI for pictures, Text-to-Speech for Leda voices)
gcloud auth login
gcloud auth application-default login
gcloud config set project "$GOOGLE_CLOUD_PROJECT"
gcloud services enable aiplatform.googleapis.com texttospeech.googleapis.com

# helpers
pip3 install pillow
npm i -g playwright && npx playwright install chromium     # only for the automatic check

# back up the drive's ENG folder once
cp -R "$SPT_ENG_ROOT" "${SPT_ENG_ROOT}_BACKUP_$(date +%Y%m%d)"
```

---

## 2. Every time Claude pushes new lessons

```bash
cd ~/mit-dit-courses
git pull                                             # get the newest lessons and prompts

# copy the pictures/folders Claude prepared (never overwrites your generated files)
rsync -av --ignore-existing --exclude '._*' --exclude 'POSES' --exclude 'KID-PLAYER' --exclude 'styles' \
  SPT/ENG/ "$SPT_ENG_ROOT/"

python3 tools/build.py                               # writes the lessons onto the drive + the prompt lists
python3 tools/generate_vertex.py --dry-run           # shows what will be generated
python3 tools/generate_vertex.py                     # GENERATES pictures + voices and saves them in place
python3 tools/build.py                               # lessons switch to the new pictures
```

That is all. `generate_vertex.py`:
- **Pictures**: reads `IMAGE_PROMPTS_ALL.json` (written by Claude's build). For each picture it calls Vertex AI
  (`gemini-2.5-flash-image`), attaches the character sheets `GRADE1/POSES/SHEET-*.png` whenever the prompt names
  Tala, Bunso, Nanay, Tatay, Ate or Kuya (so they always look the same), and saves a PNG to
  `$SPT_ENG_ROOT/<save_to>` — e.g. `GRADE1/Q1/WEEK1/DAY3/INTERACTIVE/media/art/pina-kitchen.png`
  (16:9 → 1600×900, square → 1024×1024).
- **Voices**: reads every `INTERACTIVE/speech/_lines.json` and makes `INTERACTIVE/speech/<clip>.mp3` with
  Cloud Text-to-Speech, model **gemini-2.5-flash-preview-tts**, voice **Leda** (never Chirp3), warm slow
  teacher style; `(pause)` becomes a real pause.
- Skips anything already made, so you can stop and run it again any time. Useful options:
  `--images`, `--voices`, `--only GRADE1/Q1/WEEK3`, `--force` (remake), `--dry-run`.
- If the picture model name changes in your Vertex project:
  `export SPT_IMAGE_MODEL=gemini-2.5-flash-image` (or another image model you have), `SPT_IMAGE_LOCATION=global`.

### Where every file goes (the script does this — this table is for checking)

| What | Saved to (inside the ENG folder on the drive) |
|---|---|
| Lesson page | `GRADE?/Q?/WEEK?/DAY?/INTERACTIVE/index.html` (made by build.py) |
| Generated picture | `GRADE?/Q?/WEEK?/DAY?/INTERACTIVE/media/art/<name>.png` |
| Existing picture | `GRADE?/Q?/WEEK?/DAY?/INTERACTIVE/media/<name>.jpg/png` |
| Voice clip | `GRADE?/Q?/WEEK?/DAY?/INTERACTIVE/speech/<clip>.mp3` |
| Voice text list | `GRADE?/Q?/WEEK?/DAY?/INTERACTIVE/speech/_lines.json` |
| Teacher script / picture list | `GRADE?/Q?/WEEK?/DAY?/SCRIPT.md`, `IMAGE_PROMPTS.md` |
| Characters | `GRADE1/POSES/<CHAR>/<pose>.png`, sheets `GRADE1/POSES/SHEET-<CHAR>.png` |

---

## 3. Check the result

```bash
NODE_PATH=$(npm root -g) node tools/playtest.js --shots ~/Desktop/lesson-shots   # plays every lesson
open PLAY-LESSONS.html                                                            # play them yourself
```
Look at the screenshots: if a generated picture is wrong (wrong character, text in the picture, does not
show what the slide says), delete that PNG and run `python3 tools/generate_vertex.py --images` again (it is
remade). Tell Claude if a prompt itself must change.

---

## 4. Upload to Google Drive

Upload the changed lesson folders into Drive `SPT/ENG/GRADE?/Q?/WEEK?/DAY?/` (same structure): `SCRIPT.md`,
`IMAGE_PROMPTS.md` and the whole `INTERACTIVE/` folder. Remove macOS junk first:
```bash
find "$SPT_ENG_ROOT" -name '._*' -delete
```
(If the ENG folder is inside Google Drive for desktop, it syncs automatically.)

---

## 5. Copy-paste prompt for Antigravity

> Go to `~/mit-dit-courses` and read `ANTIGRAVITY_GUIDE.md`. Do NOT change any lesson content or prompts.
> Run section 2: `git pull`, the rsync copy, `python3 tools/build.py`, then
> `python3 tools/generate_vertex.py` to generate all missing pictures (Vertex AI) and Leda voices
> (Cloud TTS, gemini-2.5-flash-preview-tts) into `$SPT_ENG_ROOT`. Then `python3 tools/build.py` again and run
> the check in section 3. Report: how many pictures and voices were made, any that failed, and show me
> 5 random generated pictures. If a call fails because of login/project/API, fix the setup from section 1.

---

## 7. Writing the remaining lessons (Antigravity takes over Claude's part)

Claude can no longer write lessons, so Antigravity must, exactly the way Claude did:
1. Read `HANDOFF.md` (rules + per-lesson plan) and `tools/AGENT_BRIEF.md` (step-by-step for one lesson).
   Study the finished lessons in `tools/lessons/` (best models: `g1q1w2d1.py`, `g1q1w1d2.py`).
2. Run `python3 tools/audit.py` → `AUDIT_REPORT.md` lists every lesson (all grades) and what is wrong;
   `AUDIT_REPORT.json` has each old lesson's words, story lines and pictures.
3. For each lesson, in order (Grade 1 Q1 first, one week at a time): get the DepEd source (Drive search
   `LANG{grade}Q{q}W{w}DAY{d}`, or the old lesson from the audit), write
   `tools/lessons/g{G}q{Q}w{W}d{D}.py` (complete story, a `bridge` on every slide, cover recalls yesterday,
   celebration previews tomorrow, every slide/card/choice has a matching picture or an `art` prompt), then
   `python3 tools/build.py g{G}q{Q}w{W}d{D} --strict` until `[OK ]`.
   Unfinished drafts from Claude's helpers, if any, are `tools/lessons/_draft_*.py` (not built; finish or delete).
4. After each week: run sections 2–4 (generate pictures + voices, check, upload) and
   `git add tools/ HANDOFF.md && git commit -m "G? Q? Week ?" && git push`.

Copy-paste prompt for that:
> Read `ANTIGRAVITY_GUIDE.md`, `HANDOFF.md` and `tools/AGENT_BRIEF.md` in `~/mit-dit-courses`. Run
> `python3 tools/audit.py`. Then write the next missing week of lessons (start Grade 1 Q1 Week 2 Day 4) as
> `tools/lessons/*.py` exactly like the finished ones, until `python3 tools/build.py <code> --strict` prints
> `[OK ]` for each. Then generate pictures and voices with `python3 tools/generate_vertex.py --only <that week>`,
> rebuild, run the play-test, and show me the week before continuing.

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| `No Google Cloud login` | `gcloud auth application-default login` |
| `HTTP 403 ... API not enabled` | `gcloud services enable aiplatform.googleapis.com texttospeech.googleapis.com` |
| `HTTP 404` model not found | set `SPT_IMAGE_MODEL` to an image model your project has (Vertex AI Studio → Model Garden) |
| `no image returned (safety)` | run again; if it repeats, tell Claude the file name so the prompt is reworded |
| `HTTP 429` busy | quota; the script waits and retries. Run per week with `--only GRADE1/Q1/WEEK3` |
| Lesson still shows robot voice | that clip's `.mp3` is missing → `python3 tools/generate_vertex.py --voices` |
| Lesson shows plain background instead of a picture | picture not generated yet → `--images`, then `build.py` |
| No sound at all | press the green **Start!** button (browsers need one tap) |
