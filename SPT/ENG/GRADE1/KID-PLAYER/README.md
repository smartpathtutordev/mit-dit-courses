# Easy (KID) player

This is the 6-year-old version of the English modules.

- Original lessons are **not** changed. Open `index.html` in a day folder for the original.
- Easy lessons live in a **`KID`** subfolder inside each day: `GRADE …/DAY 1/KID/index.html`
- Shared look and code: this `KID-PLAYER` folder.

How a child uses it:

1. This is a **short** version: about 10 pages, one sentence each.
2. Teacher Sage says that one sentence. Listen pages move on by themselves.
3. Story pictures stay open. Sage stands, steps aside, or leaves if she would cover the picture.
4. Speech is **only** prebuilt clips. The name on screen is Teacher Sage (said “Sage”).

Rebuild after changing a lesson:

```
python3 kid_logic.py
python3 record_kid_speech.py "GRADE 1"
```

Change backgrounds or recenter Sage: open `kid-builder.html` (double-click `start-kid-builder.command`).

Open the easy hub: `KID-PLAYER/index.html`

Teacher path for each day: `KID/SCRIPT.md`. Full notes: `KID-LESSON.md`.
