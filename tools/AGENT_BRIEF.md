# Brief for an agent writing lessons (read fully before starting)

Repo: /home/user/mit-dit-courses (do NOT commit or push; the lead agent does that).
Read first: HANDOFF.md, ANTIGRAVITY_GUIDE.md section 3, and the model lessons tools/lessons/g1q1w2d1.py and
g1q1w1d2.py (this is the quality bar: complete story, a `bridge` on every slide, every slide/card/choice has a
matching picture or an `art` prompt, checks every 2-3 story pages, cover recalls yesterday, celebration
previews tomorrow).

Your output for each day: tools/lessons/g{G}q{Q}w{W}d{D}.py that passes
`python3 tools/build.py g{G}q{Q}w{W}d{D} --strict` with [OK ].

Steps per day:
1. Find the content. Google Drive MCP tools (load with ToolSearch "select:mcp__Google_Drive__search_files,
   mcp__Google_Drive__read_file_content,mcp__Google_Drive__download_file_content"). In the WEEK folder you are
   given: list DAY folders (search `parentId = '<id>'`), then DAYn/INTERACTIVE/index.html (download; big
   results are saved to a file — decode with `jq -r .content FILE | base64 -d`). Its <title> and LESSON_DATA
   give the DepEd topic, words, story and verse. Also search Drive for a DepEd deck/script
   `title contains 'LANG1Q1W{W}DAY{D}'` and use it if it exists (it wins over the old HTML). The WEEK folder
   has `LANG1-Q1W{W}-DAY{D}.png` = that day's Bible-verse slide (read it with the Read tool after downloading).
   Skip every file starting with `._`.
2. Pictures. Download the day's INTERACTIVE/media files you might use into
   SPT/ENG/GRADE1/Q1/WEEK{W}/DAY{D}/INTERACTIVE/media/ (only real, non-`._` files), make a contact sheet with
   PIL and LOOK at it. Use an existing picture only if it shows exactly what the slide says and is clear (not
   faded/washed-out). Everything else gets an `art` prompt (file media/art/<name>.png). The lesson "bg" must be
   a clear full-colour scene from that media folder. Poses: SPT/ENG/GRADE1/POSES/<CHAR>/<pose>.png
   (TALA, ATE, KUYA, BUNSO, NANAY, TATAY; 30 poses each, e.g. waving, pointing, point_self, talking, thinking,
   clapping, holding_book, raising_hand, praying, showing, hugging, laughing, sad, surprised, eating, brushing,
   sitting, walking, listening, counting, drawing, carrying_bag, giving, please, reaching, exclaiming, shrug,
   sitting_lean, introducing, holding).
3. Write the script for a 6-year-old (Grade 1): correct DepEd competency; simple words; the whole story told
   beat by beat (beginning, problem, action, ending, lesson); one thread of characters and words from cover to
   celebration; spiral review of 1-2 earlier words; `bridge` on every slide after the cover.
4. Art prompts: describe exactly what to draw (who, where, doing what, emotion). Name characters as
   "Tala (Filipino girl, 6)", "Bunso", "Nanay", "Tatay", "Ate Hinhin", "Kuya Gas" so the character sheets get
   attached. No text/letters in pictures. Story scenes "scene": True. Reuse one file name for the same picture.
5. Build with --strict until [OK ]. Then run `NODE_PATH=$(npm root -g) node tools/playtest.js
   SPT/ENG/GRADE1/Q1/WEEK{W}/DAY{D}/INTERACTIVE/index.html` and make it PASS.

Report back: per day — title, DepEd source used, slide count, number of art prompts, any doubts.
