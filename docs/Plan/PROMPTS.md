# PROMPTS — Stepwise Execution Prompts for the DSA-Animations Plan

> ## ⚠ THIS FILE IS READ-ONLY FOR AGENTS ⚠
> This is the **user's prompt library**. No agent may create, edit, rename, move, or delete this
> file — not even "as part of a task", not even to "fix a typo". If any task appears to require
> changing this file, STOP and tell the user instead. Only the human user edits this file.

## How to use

1. Work through the prompts **strictly in numerical order** (001 → 052). Each prompt assumes every earlier one has completed.
2. Copy the **entire fenced block** of ONE prompt and paste it into opencode as a single message. Never merge multiple prompts into one message.
3. If the prompt header names an agent (e.g. `Agent: dsa-bugfixer`), prefix your message with: `Run this with the <agent-name> agent:` and then paste the block. If no agent is named, paste it directly to the main agent. If the custom agents/skills are not visible, restart opencode (config loads at startup).
4. Wait for the agent's completion report with verification evidence. **If verification fails, re-paste the SAME prompt** and add: "Verification failed at step N. Fix it and re-run verification." Only move on when green.
5. After each prompt the agent must tick the listed TASKBOARD rows. Recommended: commit after each prompt (tell the agent "commit" or do it yourself) — later prompts assume earlier work is safely on disk.
6. Prompts 027 and 051 are **optional** (marked in their headers). Everything else is required.
7. Some prompts contain an `ASK THE USER` step — the agent will pause and ask; answer before it continues.
8. Every prompt is self-contained but also points at plan/audit files for deeper context. **If a prompt and any other repo file disagree, THE PROMPT WINS** — note the discrepancy in the report.

## Conventions baked into every prompt (do not re-add when pasting)

- Repo root: `D:\Git-Projects\DSA-Animations`. Windows host; Linux CI target.
- The executing agent reads `AGENTS.md` at the repo root first and obeys its safety rails (never commit media >1 MB without approval; never modify `docs/Audit/`, this file, or `Animations/media/` by hand; etc.).
- "Tick TASKBOARD rows" = set status `☑` for the listed card IDs in `docs/Plan/TASKBOARD.md` (that file IS writable by agents).
- Agents never commit unless the user explicitly says "commit".

## Index

| # | Prompt title | Plan card(s) | Agent | Depends on prompts |
|---|---|---|---|---|
| 001 | Bootstrap: pinned dependencies + pyproject | F1, F2 | general | — |
| 002 | Flask config hardening | B1 | dsa-bugfixer | 001 |
| 003 | Link checker + route smoke tests | F3, F4 | general | 001, 002 |
| 004 | WebM converter tool | F5 | general | 001 |
| 005 | CI workflow | F6 | general | 001, 003 |
| 006 | Fix broken links + dead nav, honestly | B2, B3, B4 | dsa-bugfixer | 003 |
| 007 | Website content accuracy + CSS defects | B5–B9 | dsa-bugfixer | 003 |
| 008 | Manim quick fixes: AVL label, QuickSort guard | B10, B12 | dsa-bugfixer | 001 |
| 009 | Manim Graphs fixes: Floyd-Warshall, adjacency tuples | B11 | dsa-bugfixer | 001 |
| 010 | Manim heaps + D&C latent-crash fixes | B13, B14 | dsa-bugfixer | 001 |
| 011 | Greedy labels + GIF converter + notebooks | B15, B16, B17 | dsa-bugfixer | 001 |
| 012 | Render batch RB1 (9 scenes) | RB1 | general | 008–011 |
| 013 | Phase 1 gate: adversarial re-verification | G1 | dsa-auditor | 006–012 |
| 014 | Sync tool spike + design document | T1 | explore | 001 |
| 015 | Sync tool: recorder core + SyncedScene | T2, T3 | general | 014 |
| 016 | Sync tool: snapshot CLI | T4 | general | 015 |
| 017 | Sync tool: map emission + website loader | T5 | general | 016 |
| 018 | Sync tool: drift check + documentation | T6, T8 | general | 016, 017 |
| 019 | Baseline snapshots of all 72 scenes | T7 | general | 012, 015 |
| 020 | Phase 2 gate | G2 | dsa-auditor | 014–019 |
| 021 | common.py shared visual classes | R1 | dsa-refactorer | 020 |
| 022 | Traversal + edge-removal helpers | R2, R3 | dsa-refactorer | 021 |
| 023 | Dead-code sweep + BTrees logger | R4, R5 | dsa-refactorer | 021 |
| 024 | Typo renames (SortingAlgorithms, Adjacency, Prim's) | R6 | dsa-refactorer | 021 |
| 025 | Flask cleanups + kebab-case route aliases | R7 | dsa-refactorer | 021 |
| 026 | Ruff full pass | R8 | dsa-refactorer | 022–025 |
| 027 | OPTIONAL: Huffman single-pass | R9 | dsa-refactorer | 021 |
| 028 | Render batch RB2 (8 adjacency scenes) | RB2 | general | 024 |
| 029 | Phase 3 gate: oracle must be byte-identical | G3 | dsa-auditor | 021–028 |
| 030 | Bulk webm conversion (~56 videos) | C0 | general | 004, 012, 028 |
| 031 | Arrays pages get videos + maps | C1 | dsa-page-builder | 030 |
| 032 | LinkedList completion + Queue page | C2, C3 | dsa-page-builder | 030 |
| 033 | Trees I: types, traversals, correlation, union-find | C4 | dsa-page-builder | 030 |
| 034 | Trees II: BST, ternary, heaps | C5 | dsa-page-builder | 030 |
| 035 | AVL tree page (6 videos) | C6 | dsa-page-builder | 030 |
| 036 | B-Tree page | C7 | dsa-page-builder | 030 |
| 037 | Graphs I: types + representations (12 videos) | C8 | dsa-page-builder | 030 |
| 038 | Graphs II: traversals (4 videos) | C9 | dsa-page-builder | 030 |
| 039 | Graphs III: shortest paths (3 pages) | C10 | dsa-page-builder | 030 |
| 040 | Graphs IV: Prim's, Kruskal's, topological sort | C11 | dsa-page-builder | 030 |
| 041 | Divide & Conquer section (4 pages) | C12 | dsa-page-builder | 030 |
| 042 | Greedy section (2 pages) | C13 | dsa-page-builder | 030 |
| 043 | Navigation sweep: un-hide + footer + home | C14 | dsa-page-builder | 031–042 |
| 044 | Phase 4 gate | G4 | dsa-auditor | 043 |
| 045 | Responsive design | W1 | dsa-page-builder | 044 |
| 046 | Dark mode toggle | W2 | dsa-page-builder | 044 |
| 047 | Fonts + favicon + meta/OG | W3, W4 | dsa-page-builder | 044 |
| 048 | Site search | W5 | dsa-page-builder | 043 |
| 049 | Home honesty + legal pages | W6, W7 | dsa-page-builder | 044 |
| 050 | Auth polish + performance | W8, W9 | dsa-page-builder | 045 |
| 051 | OPTIONAL: legacy inline-map migration | W10 | general | 044 |
| 052 | Final audit + DoD sign-off | G5 | dsa-auditor | all |

---

## Phase 0 — Foundation

### PROMPT 001 — Bootstrap: pinned dependencies + pyproject

Plan card(s): F1, F2 (`docs/Plan/01-Foundation.md`) · Agent: general · Depends on: none · Tick TASKBOARD rows: F1, F2

`````text
PROMPT 001 — BOOTSTRAP: PINNED DEPENDENCIES + PYPROJECT

CONTEXT
You are working in the repository at D:\Git-Projects\DSA-Animations ("DSA-Animations"): Manim-based
Data Structures & Algorithms animations (Animations/) plus a Flask website (Website/website/).
Stack (all already installed on this machine): Python 3.11+, Manim 0.19.0, Flask 3.0.3,
Flask-SQLAlchemy 3.1.1, Flask-Login 0.6.3, moviepy 2.2.1.
Read AGENTS.md at the repo root FIRST and obey it. This is the first task of the plan in docs/Plan/.
Current state: there is NO root requirements.txt (only requirements_converter.txt for the GIF tool,
which wrongly allows moviepy 1.x), and no pyproject.toml anywhere.

TASK
1. Record installed versions by running:
     pip show manim flask flask-sqlalchemy flask-login moviepy tqdm networkx numpy ruff pytest
2. Create root requirements.txt with EXACT pins (==) for every package the project imports
   directly: manim, networkx, numpy (Animations), flask, flask-sqlalchemy, flask-login (Website),
   moviepy, tqdm (conversion tools). One package per line, grouped with short comments
   (# website / # animations / # tools).
3. Create requirements-dev.txt with EXACT pins for pytest and ruff, plus a one-line header comment.
4. Edit requirements_converter.txt: replace moviepy>=1.0.3 with moviepy>=2.0,<3.0
   (the converter does `from moviepy import ...`, which only works on moviepy 2.x).
5. Create root pyproject.toml — CONFIG ONLY, no [project] section (this is an application repo):
   [tool.ruff]
   line-length = 100
   target-version = "py311"
   extend-exclude = ["Animations/media", "gifs", "Understanding", "utils/createHighlightMap.ipynb",
                     ".kilo", "Website/website/static", "docs"]
   [tool.pytest.ini_options]
   testpaths = ["tests"]
6. Do NOT write any tests, scripts, or CI yet — later prompts do that. Touch no other files.

CONSTRAINTS
- Do not upgrade or downgrade any package; pin what is installed.
- Do not modify the Flask app, animations, or templates.
- Do not commit unless the user explicitly says "commit".

VERIFICATION (all must pass before you report done)
1. pip install -r requirements.txt succeeds with everything already satisfied (must not try to
   change versions).
2. python -c "import manim, flask, flask_sqlalchemy, flask_login, moviepy, networkx, numpy"
   exits 0.
3. ruff check Animations Website tools mp4_to_gif_converter.py RUNS without a CONFIG error.
   (It will report lint findings — that is expected and fine; those are the Phase 3 backlog.
   This task only proves the configuration is valid.)
4. pytest runs and reports "no tests ran" (exit code 5 acceptable) with no config error.

REPORT
- The pinned version list, files created/changed, verification output summary.
- Tick TASKBOARD rows F1 and F2 in docs/Plan/TASKBOARD.md (status -> done).
`````

### PROMPT 002 — Flask config hardening

Plan card(s): B1 (`docs/Plan/02-Bugfixes.md`) · Agent: dsa-bugfixer · Depends on: 001 · Tick TASKBOARD rows: B1

`````text
PROMPT 002 — FLASK CONFIG HARDENING (SECRET_KEY, DB PATH, DEBUG PRINTS, TRACKED DB)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations — Manim DSA animations + Flask website in Website/website/.
Windows host; CI/deploy target is Linux. Read AGENTS.md first. Full bug details: docs/Audit/04-Bugs.md
section 2. This bugfix runs EARLY (before the test suite is built in PROMPT 003) because all later
tests import the Flask app and need a sane DB path.
The problem: Website/website/__init__.py line 12 builds the SQLite URI from os.getcwd()
(sqlite:///{cwd}/Website/database.db) — running "cd Website; python main.py" per the README writes
the DB into the wrong place (on Windows it silently lands inside the website/ package folder, which
is why an untracked Website/website/database.db exists); on Linux it fails outright. Line 11
hardcodes SECRET_KEY = 'my_secret_key'. Lines 41/43 print "Created Database!" debug output.
Website/website/auth.py line 53 has a commented-out print. A SQLite DB (Website/database.db) is
committed to git.

TASK
1. First CHECK the tracked DB for real user data (default assumption: schema/test rows only):
     python -c "import sqlite3; con=sqlite3.connect(r'Website/database.db'); print(con.execute(\"select name from sqlite_master where type='table'\").fetchall()); [print(n, con.execute(f'select count(*) from {n[0]}').fetchone()) for n in con.execute(\"select name from sqlite_master where type='table'\").fetchall()]"
   If any user table has more than a couple of rows, STOP and ASK THE USER before continuing.
2. In Website/website/__init__.py:
   a. Replace the hardcoded secret with:
        app.config["SECRET_KEY"] = os.environ.get("DSA_SECRET_KEY", "dev-only-insecure-key")
   b. Replace the cwd-based DB path with the Flask instance path:
        import os, pathlib
        os.makedirs(app.instance_path, exist_ok=True)
        db_path = pathlib.Path(app.instance_path, "database.db").as_posix()
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
      (Keep whatever db/ma/init boilerplate already exists; only change the URI computation.
       The URI must use forward slashes — never backslashes.)
   c. Delete the debug prints at lines ~41 and ~43 ("Created Database!") .
3. In Website/website/auth.py: delete the commented-out print at line ~53.
4. Untrack the committed DB and ignore DBs from now on:
     git rm --cached Website/database.db
   and append to .gitignore:
     *.db
     Website/instance/
     Website/website/database.db
5. Do NOT change routes, templates, models, or anything else. Do NOT migrate data (default:
   the old DB is disposable; if step 1 found real data, wait for the user's decision).

VERIFICATION (all must pass)
1. python main.py works from Website/ AND python Website/main.py style invocations: the app starts,
   the DB file appears ONLY under Website/instance/database.db, and http://127.0.0.1:5000/ loads.
2. No "Created Database!" output in the console; no other new prints.
3. git status no longer lists Website/database.db as tracked; .gitignore updated.
4. Smoke: with the dev server running, register a test account, log in, log out — all work
   (then delete Website/instance/database.db and restart once to confirm it re-creates cleanly).

REPORT
- Diff summary, where the DB now lives, evidence for each verification step, the row-count
  result from step 1.
- Tick TASKBOARD row B1.
`````

### PROMPT 003 — Link checker + route smoke tests

Plan card(s): F3, F4 (`docs/Plan/01-Foundation.md`) · Agent: general · Depends on: 001, 002 · Tick TASKBOARD rows: F3, F4

`````text
PROMPT 003 — LINK CHECKER TOOL + ROUTE SMOKE TESTS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. The website (Website/website/) has 25
Flask routes; templates live in Website/website/templates/. The audit (docs/Audit/04-Bugs.md
section 1) found 28 broken links: 17 sidebar links to nonexistent routes + /rotation
(templates/content.html:56,63-97), 8 relative links in templates/DSA/data_structures.html
(:40,61,87,105,126,177,199,230), a "Sorting%20Algorithms" link in templates/DSA/algorithms.html:268,
and a link to a nonexistent "Doubly Linked Lists.md" in templates/LinkedList/linked_list.html:124,
plus 27 footer anchors with no href (base.html:118-187). Eight templates also reference static
videos with lowercase videos/ while the real folder is Videos/ (works on Windows, 404 on Linux).
Those LINK BUGS get FIXED in PROMPT 006 — this prompt only builds the detector and records today's
broken set as a baseline allowlist.

TASK
1. Create tools/link_check.py — a crawl-based link checker (NOT a template regex parser):
   a. Import the app: from website import create_app  (run from repo root; add
      tools/__init__.py so "tools" is an importable package; add an empty tests/__init__.py too).
   b. Create the app, then for EVERY route in app.url_map (skip /static), GET it with
      app.test_client() and parse the RENDERED HTML (stdlib html.parser) for href= and src= and
      data-sync= attributes. This resolves Jinja url_for() calls automatically.
   c. Classify each extracted URL:
      - http://, https://, mailto:, tel:, javascript:, #anchors, urn: -> SKIP (external).
      - <a> with NO href attribute -> count as "dead-anchor warning" (do not fail).
      - URLs starting with /static/ -> the file must exist under Website/website/static/
        with EXACT case-sensitive path match (compare against actual directory listing).
      - Everything else (absolute paths, relative paths) -> GET it with the test client;
        2xx/3xx = OK, 404/500 = broken.
   d. Structure the code as: run(allowlist_path=None) -> (known_broken, new_broken, warnings)
      plus a main() CLI wrapper with argparse: --allowlist (default
      docs/Plan/baseline-broken-links.txt), --strict (ignore allowlist), --verbose.
      Exit code 0 when new_broken == 0, else 1. Print one line per broken link:
      "template-ish origin page -> URL -> reason".
2. Create docs/Plan/baseline-broken-links.txt: run the checker, paste ALL current broken links
   (one per line) into it, and keep a "# known-broken baseline generated on <date>" header.
   Re-run with the allowlist: must exit 0 with new_broken == 0.
3. Create tests/test_links.py: pytest wrapper that calls tools.link_check.run() with the
   default allowlist and asserts new_broken == 0.
4. Create tests/test_routes.py: a test_client smoke test asserting these 25 routes return 200:
   /, /dsa, /data structures, /algorithms, /arrays, /2D arrays, /searching algorithms,
   /linear search, /binary search, /sorting algorithms, /bubble sort, /insertion sort,
   /selection sort, /quick sort, /merge sort, /heap sort, /stack and queue, /stack, /queue,
   /linked list, /singly linked list, /doubly linked list, /login, /signup
   and /logout returns 302.
5. Do not fix any link or template content in this prompt. Do not touch the manim code.

CONSTRAINTS
- Use pathlib everywhere; no backslash separators in code.
- The checker must work on Linux (CI) — exact-case static checks are the whole point.
- No new dependencies (stdlib html.parser is fine; the app already provides the client).

VERIFICATION (all must pass)
1. python tools/link_check.py prints the broken-link baseline (expect roughly the 28 audit links
   + any lowercase-videos/ static references on pages — videos/ vs Videos/ shows up here as
   "static file not found" findings; include them in the allowlist too) and exits 1 WITHOUT
   allowlist; exits 0 WITH allowlist.
2. pytest -q is fully green (both test files).

REPORT
- Files created; the exact baseline list (count + summary); pytest output; any surprising findings.
- Tick TASKBOARD rows F3 and F4.
`````

### PROMPT 004 — WebM converter tool

Plan card(s): F5 (`docs/Plan/01-Foundation.md`) · Agent: general · Depends on: 001 · Tick TASKBOARD rows: F5

`````text
PROMPT 004 — TOOLS/CONVERT_WEBM.PY (MP4 -> WEBM FOR THE WEBSITE)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. Rendered manim videos live at
Animations/media/videos/<Category>/480p15/<Scene>.mp4. The website serves videos as .webm from
Website/website/static/Videos/<Category>/<Scene>.webm — note the capital V and that website
categories use correct spelling (static/Videos/SortingAlgorithms — no "Algoritms" typo), while
media categories keep the source-folder spelling (media/videos/SortingAlgoritms has the typo;
leave that alone in this task — renaming happens in PROMPT 024).
ffmpeg is expected to be installed — verify with `ffmpeg -version`; if it is missing, STOP and
tell the user to install it.

TASK
Create tools/convert_webm.py mirroring the UX of mp4_to_gif_converter.py (read it for style):
1. Probe the settings of an EXISTING site webm first and reuse them:
     ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate -of default=nw=1 \
       "Website/website/static/Videos/SortingAlgorithms/BubbleSort.webm"
   Build the ffmpeg command from what you find (likely VP9 video, no/opus audio; manim output is
   silent, so no audio track is expected — if the probe shows no audio stream, do not encode one).
   Default fallback if probing is inconclusive:
     ffmpeg -y -i <in> -c:v libvpx-vp9 -crf 33 -b:v 0 -an <out>
2. CLI: argparse with --category (one or more media/videos subdirs), --scene (filter by scene
   name), --dry-run (list what would convert), --force (overwrite existing), default behavior
   skips existing outputs. Batch over all found mp4s at 480p15 quality only.
3. Output path: Website/website/static/Videos/<category>/<Scene>.webm using pathlib; CREATE parent
   dirs. Map category names as-is from media/videos (the site-side folder name equals the
   category). Add a module-level CATEGORY_ALIASES = {} dict (empty for now) where PROMPT 024 will
   later register the SortingAlgoritms -> SortingAlgorithms mapping.
4. Print a summary table (converted / skipped / failed) and a final line of total bytes written.
5. Convert ONE pilot file as proof: the Stack-Queue category's Queue scene
   (media/videos/Stack-Queue/480p15/Queue.mp4 if it exists, otherwise pick any scene missing
   from static/Videos) and ffprobe the result.

CONSTRAINTS
- pathlib everywhere; exact-case output paths; no backslashes in any path passed to ffmpeg —
  convert with Path.as_posix().
- Never overwrite existing webms unless --force.
- Do not commit the pilot webm without asking the user (media-commit rule in AGENTS.md).

VERIFICATION (all must pass)
1. python tools/convert_webm.py --dry-run lists every mp4 it would convert with correct
   source -> destination paths.
2. The pilot webm exists at the expected exact-case path, ffprobe reports a valid VP9/webm
   stream, and it plays (open it in a browser or report ffprobe evidence).
3. Re-running the command without --force skips the existing pilot (prints "skipped").

REPORT
- The probed settings used, files created, dry-run summary, verification evidence.
- Tick TASKBOARD row F5.
`````

### PROMPT 005 — CI workflow

Plan card(s): F6 (`docs/Plan/01-Foundation.md`) · Agent: general · Depends on: 001, 003 · Tick TASKBOARD rows: F6

`````text
PROMPT 005 — CI WORKFLOW (GITHUB ACTIONS)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. PROMPTs 001-004 created pinned
requirements.txt + requirements-dev.txt, tools/link_check.py, and pytest tests (tests/test_links.py,
tests/test_routes.py). There is no CI at all today (no .github/ directory). The site deploys to
Linux, and CI on ubuntu is what catches Windows-only assumptions (e.g. case-insensitive static
paths). Check the default branch name with `git branch --show-current` and use it in the workflow.

TASK
Create .github/workflows/ci.yml:
1. Triggers: push and pull_request on the default branch.
2. Job "test" on ubuntu-latest:
   - actions/checkout@v4
   - actions/setup-python@v5 with python-version "3.11" and pip caching enabled
   - Install: pip install -r requirements.txt -r requirements-dev.txt
     (this installs manim too — heavy but simple and cacheable; note the install time in a
     workflow comment)
   - Run: pytest (this includes the link checker and route smoke tests — on ubuntu they will
     catch any static-path casing bugs; the tests must pass with the allowlist from PROMPT 003)
   - Run: ruff check Animations Website tools mp4_to_gif_converter.py --exit-zero
     (--exit-zero keeps CI green while lint findings are the Phase 3 backlog; add a workflow
     comment: remove --exit-zero after PROMPT 026)
3. Job "lint" is NOT needed separately; keep one job for simplicity.
4. Add nothing else: no manim rendering in CI, no deployment, no other jobs.

CONSTRAINTS
- Do not change any application code to make this work.
- If pytest or the link checker currently fail on Windows in your local run, fix ONLY test/tool
  bugs (not app bugs) — e.g. path handling in the checker — and report what you had to touch.

VERIFICATION (all must pass)
1. The YAML parses: python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml'))"
   (install pyyaml if needed and note it).
2. All commands the workflow runs succeed locally on this machine in the same order
   (pytest then ruff --exit-zero).
3. git status shows only .github/workflows/ci.yml added (plus any reported test-tool fixes).

REPORT
- The workflow file content summary; local verification evidence; anything the user must do
  (e.g. push to GitHub to see the first real run).
- Tick TASKBOARD row F6.
`````

## Phase 1 — Bugfixes

### PROMPT 006 — Fix broken links + dead nav, honestly

Plan card(s): B2, B3, B4 (`docs/Plan/02-Bugfixes.md`) · Agent: dsa-bugfixer · Depends on: 003 · Tick TASKBOARD rows: B2, B3, B4

`````text
PROMPT 006 — BROKEN LINKS: FIX THE FIXABLE, HIDE THE REST HONESTLY

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-verify" skill and use
it at the end. Full bug list: docs/Audit/04-Bugs.md section 1. PROMPT 003 built the link checker
(tools/link_check.py) and recorded today's broken links in docs/Plan/baseline-broken-links.txt.
This prompt eliminates every broken link from the site WITHOUT building any new pages (pages for
Trees/Heaps/Graphs/etc. arrive in Phase 4 — until then the nav must be honest about it).

TASK
1. Static-path casing (B2): these 8 templates reference lowercase videos/ — change to Videos/
   (the real static folder; capital V, exact case):
     Website/website/templates/SearchingAlgorithms/linear_search.html:47
     Website/website/templates/SortingAlgorithms/bubble_sort.html:53
     Website/website/templates/SortingAlgorithms/heap_sort.html:78
     Website/website/templates/SortingAlgorithms/insertion_sort.html:63
     Website/website/templates/SortingAlgorithms/merge_sort.html:89
     Website/website/templates/SortingAlgorithms/quick_sort.html:83
     Website/website/templates/SortingAlgorithms/selection_sort.html:59
     Website/website/templates/StackAndQueue/stack.html:94
2. Fix broken hrefs that HAVE real targets (B4) — use url_for, never hardcoded paths:
   a. templates/DSA/data_structures.html lines 40, 61, 87, 105, 126, 177, 199, 230 contain
      relative links: "Arrays", "Linked%20Lists", "Stacks", "Queues", "Trees", "Hash%20Tables",
      "Graphs", "Union-Find".
      - "Arrays" -> url_for the /arrays route; "Linked%20Lists" -> the /linked list route;
        "Stacks" -> the /stack route; "Queues" -> the /queue route.
        (Find exact endpoint names by reading Website/website/views.py function names.)
      - "Trees", "Hash%20Tables", "Graphs", "Union-Find" have NO pages yet: convert each
        <a> into <span class="nav-item-pending">Trees</span> (plain span, no href) and add
        <span class="nav-pending-note">(page coming soon)</span> styling consistent with the
        page's look.
   b. templates/DSA/algorithms.html:268 href="Sorting%20Algorithms" ->
      url_for the /sorting algorithms route.
   c. templates/LinkedList/linked_list.html:124 href="Doubly%20Linked%20Lists.md" (a nonexistent
      Markdown file) -> url_for the /doubly linked list route.
3. Dead navigation (B3): in templates/content.html the sidebar section around lines 60-99 has
   17 links to routes that do not exist (/types_of_trees, /properties_of_trees, /traversal,
   /breadth_first_search, /depth_first_search, /list_tree_correlation, /binary_search_tree,
   /ternary_tree, /avl_tree, /types_of_heaps, /properties_of_heap, /types_of_graphs,
   /graph_representation, /dijkstra_algorithm, /floyd_warshall_algorithm, /bellman_ford_algorithm,
   /prims_algorithm, /kruskal_algorithm) plus a /rotation link at line 56.
   - Convert every one of those <a href="..."> entries into
     <span class="nav-item-pending" data-target="/original-url">...label...</span>
     (keep the label text; keep the section headings; data-target preserves the intended route
     so Phase 4 can re-activate them by grepping "nav-item-pending").
   - Add ONE small note under the sidebar: <p class="nav-pending-note">More topics are being
     added — these sections arrive soon.</p>
   - In templates/base.html lines 118-187 the footer has ~27 <a> tags with NO href (Our Team,
     Contact Us, Privacy Policy, Terms of Service, algorithm names, ...): wrap that whole
     footer-links block with hidden="hidden" (keep the markup for Phase 4/5 to rewire).
   - Add CSS in Website/website/static/styles.css: .nav-item-pending { color: #888;
     cursor: default; } and .nav-pending-note { color: #888; font-size: 0.8rem; }
     (match existing CSS conventions in the file).
4. Baseline allowlist (docs/Plan/baseline-broken-links.txt): after your fixes, re-run the checker.
   Remove from the allowlist every entry that is now fixed, and remove entries that no longer
   exist because you converted them to spans/hidden. Target: the file contains ONLY its header
   comment. The goal state is: python tools/link_check.py exits 0 with an EMPTY allowlist, and
   with --strict it also exits 0.
5. If the checker reports broken links the audit did NOT mention: fix them the same way if a
   real target exists; otherwise convert to spans per step 3 and leave a note in your report.

CONSTRAINTS
- Do not create any new routes, pages, or content sections.
- Do not delete any existing markup sections — only convert <a> to <span> or add hidden.
- url_for everywhere for real links; never hardcode paths.

VERIFICATION (all must pass)
1. python tools/link_check.py -> exit 0, zero broken (allowlist empty or header-only).
2. pytest -q green.
3. Manually render 3 pages (home, /data structures, /linked list) with the dev server: sidebar
   pending items visibly grayed, no console errors, footer links block invisible.
4. Existing pages' videos still load (spot-check one video URL from stack.html).

REPORT
- Per-fix summary; final allowlist state; evidence for each verification step.
- Tick TASKBOARD rows B2, B3, B4.
`````

### PROMPT 007 — Website content accuracy + CSS defects

Plan card(s): B5, B6, B7, B8, B9 (`docs/Plan/02-Bugfixes.md`) · Agent: dsa-bugfixer · Depends on: 003 · Tick TASKBOARD rows: B5, B6, B7, B8, B9

`````text
PROMPT 007 — CONTENT ACCURACY: WRONG CODE SAMPLES, WRONG COMPLEXITY CLAIMS, COPY + CSS DEFECTS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-verify" skill and
use it at the end. These are educational pages — WRONG MATH AND CODE IN TEACHING MATERIAL ARE
CRITICAL BUGS. Full list with locations: docs/Audit/04-Bugs.md section 3 (content) and section 4
(CSS). The ground truth for complexity claims is the notebooks in Understanding/ (Trees.ipynb,
AVLTrees.ipynb, Graphs.ipynb) and standard CLRS results; if you cannot verify a claim against
them, do not state it. All paths below are relative to Website/website/templates/.

TASK — code samples
1. SearchingAlgorithms/binary_search.html:48-51: the displayed binary search runs on an UNSORTED
   array [5,2,4,6,3,1] and is called with high = N (off-by-one IndexError for large x).
   Fix the displayed code to: sorted array [1,2,3,4,5,6] (the video itself sorts first — watch
   the Animations/SearchingAlgorithms.py BinarySearch construct() to confirm the demo), and
   high = len(arr) - 1 with a standard low <= high loop.
   THEN re-check this page's inline highlightMap (const highlightMap = [...] around line 244):
   every entry's "lines" value must reference line numbers of the NEW code block. Watch the page's
   video once with the dev server and adjust "lines" strings so highlighting matches the code
   shown. Do not invent new timings — shift line references only.

TASK — complexity and math claims (edit the sentences; keep MathJax syntax working)
2. SortingAlgorithms/sorting_algorithms.html:
   :91 Insertion sort "typically O(n)" -> O(n^2) average/worst case, O(n) best case.
   :96 Selection sort "$O(n)$" -> "$O(n^2)$".
   :103 Quick sort "worst-case running time is $O(n)$" -> "$O(n^2)$" worst case (mention
        O(n log n) average if the sentence allows).
3. SortingAlgorithms/insertion_sort.html:266: "quadratic time complexity (O(n))" -> "(O(n^2))".
4. DSA/dsa.html:113-114: "square of its input size $O(n)$" -> "$O(n^2)$" (first occurrence only;
   the later "slower than ... $O(n)$" comparison stays).
5. DSA/algorithms.html:
   :175 "$\frac{n}{2}=1$, meaning $n=2$" -> the halving repeats until the size hits 1
        (i.e. after k steps n/2^k = 1, so k = log2(n)).
   :225-226 "$n$ dominates $n$. Thus $T(n) = \Theta(n)$" -> "$n^3$ dominates $n$. Thus
        $T(n) = \Theta(n^3)$" (read the surrounding worked example and make the whole
        master-theorem paragraph consistent with it).
6. SearchingAlgorithms/linear_search.html:
   :116-119 worst-case Theta(n) described as "an upper bound" -> Theta is a TIGHT bound;
        O is the upper bound. Reword accordingly.
   :140-142 "average-case running time ... quadratic function" -> average case is linear,
        Θ(n) (about (n+1)/2 comparisons for a present key).

TASK — copy defects
7. StackAndQueue/stack.html:85: displayed code `s.push(data):` (trailing colon) -> s.push(data).
8. StackAndQueue/stack.html:101-112: malformed <li> elements floating outside any list ->
   wrap them in a proper <ul> (or convert to <p> — match surrounding markup).
9. Arrays/2Darrays.html:28: "would be at <code>A</code>" -> "at <code>A[0][0]</code>" (indices
   were lost).
10. auth/signup.html:27-29: submit button labeled "LogIn" on the SIGN-UP page -> "Sign Up".
11. DSA/algorithms.html:1: page <title> block says "DSA" -> give it a proper title matching the
    pattern of sibling templates (e.g. "Algorithms - DSA Animations" — check how other pages do
    the title block first).
12. home.html:49 "Feature Topics" -> "Featured Topics".
13. home.html:429-433: the "Concept-to-Code Connection" card reuses the "Animated Clarity"
    description verbatim -> write an honest, distinct one-sentence description (the site really
    does show code that lights up in sync with the video).
14. LinkedList/singly_linked_list.html:604 and :616: the delete-function highlight map is labeled
    "insertNode" -> "deleteNode" (function name text only; do not touch timings).
15. AI meta-text scrub (rewrite as direct prose, keep the factual content):
    Arrays/arrays.html:28-32 ("While the sources do not explicitly detail..."),
    Arrays/2Darrays.html:13, 31 ("in the sources", "The sources provide..."),
    LinkedList/linked_list.html:19, 108,
    SortingAlgorithms/sorting_algorithms.html:123-124, 194,
    SortingAlgorithms/heap_sort.html:125.
    After editing, grep the whole templates tree for "the sources", "given sources", "mentioned
    in the sources" — zero hits.

TASK — home-page honesty
16. home.html: remove all fake ratings ("4.6", "(1.2k)" etc.) from the topic cards (around
    lines 86-94 and every sibling card).
17. home.html around 389-393: the claim "Pause, play, speed up, or step through" implies
    interactive controls that do not exist (videos are plain <video controls>) -> reword to
    describe reality (e.g. "Play, pause, scrub, and watch the code light up as the animation
    runs").

TASK — CSS defects (Website/website/static/styles.css)
18. :565-567 `.carousel::-webkit-scrollbar { display: none; }` targets the WRONG class — the
    real class is .topic-carousel. Fix the selector (and verify no ::-moz equivalent has the
    same wrong class).
19. :125 `justify-content: flex;` is invalid CSS (silently dropped). Read the rule's context;
    if the items are meant to spread horizontally, use space-between; if it was meaningless,
    delete the declaration. Explain your choice in the report.
20. :556 and :560: duplicate `scrollbar-width: none` in the same rule -> keep one.

CONSTRAINTS
- Each complexity claim you write must be verifiable against Understanding/*.ipynb or CLRS
  standard results. When in doubt, write less, not more.
- Do not restructure pages, do not touch sync timings except where a code block's line numbers
  changed (step 1), do not touch any Python code.

VERIFICATION (all must pass)
1. pytest -q green; link checker exit 0.
2. Grep checks: zero hits for "the sources", "given sources", "4.6", "1.2k"; grep "s.push(data):"
   zero hits; "O(n)$" no longer appears where it contradicts quadratic claims (spot-check the
   five edited complexity sentences render their MathJax).
3. Dev server: binary_search page video + code highlighting still sync (watch ~30s);
   signup button reads "Sign Up"; stack page lists render properly.
4. Chrome/Edge devtools console: no CSS parse warnings for the edited declarations, and the
   topic carousel shows no visible scrollbar after fix 18 (WebKit check matters).

REPORT
- Table of edit -> file:line -> before/after gist; verification evidence per item.
- Tick TASKBOARD rows B5, B6, B7, B8, B9.
`````

### PROMPT 008 — Manim quick fixes: AVL label, QuickSort guard

Plan card(s): B10, B12 (`docs/Plan/02-Bugfixes.md`) · Agent: dsa-bugfixer · Depends on: 001 · Tick TASKBOARD rows: B10, B12

`````text
PROMPT 008 — MANIM FIXES #1: AVL LEFT-LEFT LABEL + QUICKSORT BASE-CASE GUARD

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. These are Manim animation SOURCE
fixes: do NOT render anything in this prompt (rendering happens in a batch later — PROMPT 012).
Bug details: docs/Audit/04-Bugs.md section 5. Manim renders are slow; your job is a correct,
minimal source diff verified by reading, not by rendering.

TASK
1. Animations/AVLTree.py line ~646, inside class LeftLeftCase: the on-screen text label says
   "Left Rotation" while the code below it performs a RIGHT rotation (the docstring around line
   541 already says this case needs a right rotation — the rotation code at lines ~655-672 is
   correct; only the label is wrong).
   - Read the class construct() around lines 540-680 first to confirm which mobject holds the
     label text.
   - Change the label string to "Right Rotation". Change NOTHING else in the file.
2. Animations/SortingAlgoritms.py lines ~416-419, inside the QuickSort scene's partition
   visualization: the base-case block marks arr[low] with an arrow even when the subarray is
   EMPTY (low > high) — which also raises IndexError when low == len(arr).
   - Read the surrounding construct()/partition-animation code first (lines ~380-450).
   - Wrap the arrow-creation block in `if low <= high:` so the marking happens only for
     non-empty subarrays. The demo input [5,2,4,6,3,1] must render IDENTICALLY to before —
     reason through the recursion for that input and state in your report that no visible
     step changes for it.
   - Note: there is a separate known oddity at ~444-446 (make_arrow called with i = -1 indexing
     arr[-1] before repositioning) — do NOT touch it here; it is harmless and listed in the
     audit as low severity.

CONSTRAINTS
- Minimal diffs: exactly these two changes, nothing else in these or any other files.
- No debug prints, no reformatting, no renames (renames happen in PROMPT 024).
- Do not render. Do not commit.

VERIFICATION (all must pass)
1. python -c "import sys; sys.path.insert(0, 'Animations'); import AVLTree, SortingAlgoritms"
   — both modules import without errors.
2. Read-back proof: quote in your report (a) the corrected label line with 3 lines of context,
   (b) the guarded block with 3 lines of context.
3. Trace check: for QuickSort on [5,2,4,6,3,1], list every (low, high) pair the recursion visits
   and confirm none of them hit the new guard in a way that changes visuals for this input.

REPORT
- The two diffs, the import check, the trace table, and a note that LeftLeftCase needs a
  re-render in PROMPT 012 (add "RB1" to the Notes column of TASKBOARD row B10; mark B12 with
  "no re-render needed").
- Tick TASKBOARD rows B10, B12.
`````

### PROMPT 009 — Manim Graphs fixes: Floyd-Warshall, adjacency tuples, typo

Plan card(s): B11 (`docs/Plan/02-Bugfixes.md`) · Agent: dsa-bugfixer · Depends on: 001 · Tick TASKBOARD rows: B11

`````text
PROMPT 009 — MANIM FIXES #2: FLOYD-WARSHALL SKIPPED VERTEX + ADJACENCY SETS + TYPO

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. Do NOT render in this prompt
(render batch is PROMPT 012). Bug details: docs/Audit/04-Bugs.md section 5. All work is in
Animations/Graphs.py. The reference CORRECT implementations live in
Understanding/Graphs/Graphs.ipynb — consult them.

TASK
1. Line ~1809, class FloydWarshall: the intermediate-vertex loop is
   `for k in range(1, len(vertices))` — it SKIPS vertex 0 as an intermediate. It happens to work
   only because vertex 0 has in-degree 0 in this demo graph. Change to
   `for k in range(len(vertices))`. Check the notebook's FloydWarshall (cell ~12) to confirm
   the correct form is k over ALL vertices, and make sure the animation's matrices/labels still
   line up (the loop body builds per-k tableaux — adding k=0 means one MORE tableau step appears;
   state that explicitly in your report as an intended visual change, since the rendered video
   will gain a step).
2. Lines ~1192-1193 (class WeightedAdjecencyListUD) and ~1419 (class WeightedAdjecencyListD):
   the adjacency list is built by appending an unordered SET literal, e.g.
   adjecencyList[u].append({v, w}) — which displays as {10, 1} with braces and unstable order in
   the rendered video. Replace the set literals with TUPLES (v, w) (or the pair-strings your
   read of the surrounding rendering code shows it builds — read the rendering loop first and
   pick the representation that displays as a clean ordered pair, no braces). Apply to BOTH
   classes; keep their visuals otherwise identical.
3. Line ~1932 (class PrimsMCST area): on-screen text contains "egde" -> "edge".

CONSTRAINTS
- Minimal diffs; no renames (the Adjecency class-name typo is fixed in PROMPT 024 — do NOT
  rename classes here); no reformatting; do not render; do not commit.
- For fix 1: if the construct() uses `len(vertices)` elsewhere to pre-compute counts of steps
  (wait durations, table groups), make sure the added k=0 iteration is handled consistently —
  read carefully before editing.

VERIFICATION (all must pass)
1. python -c "import sys; sys.path.insert(0, 'Animations'); import Graphs" — imports clean.
2. Read-back proof: quote each corrected block with 3 lines of context.
3. Consistency proof for fix 1: list the (i, j) relaxations that the k=0 iteration would skip
   under the old code for this demo graph, and confirm none of them would change any distance
   value in THIS graph (so the final matrix shown in the video is unchanged; only an extra
   intermediate tableau appears).

REPORT
- The three diffs, import check, consistency proof.
- Add "RB1" to the Notes column of TASKBOARD row B11 (FloydWarshall, WeightedAdjecencyListUD,
  WeightedAdjecencyListD need re-render).
- Tick TASKBOARD row B11.
`````

### PROMPT 010 — Manim heaps + D&C latent-crash fixes

Plan card(s): B13, B14 (`docs/Plan/02-Bugfixes.md`) · Agent: dsa-bugfixer · Depends on: 001 · Tick TASKBOARD rows: B13, B14

`````text
PROMPT 010 — MANIM FIXES #3: HEAP ROOT-INSERT ARTIFACTS + D&C CRASH GUARDS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. Do NOT render here (render batch is
PROMPT 012). Bug details: docs/Audit/04-Bugs.md section 5. Files: Animations/Trees.py and
Animations/DivideAndConquer.py.

TASK — Animations/Trees.py (MaxHeap + MinHeap scenes)
1. MaxHeap scene lines ~1196-1197 (and the mirrored MinHeap code at ~1298-1299): when a new value
   is inserted at the ROOT (parent_index works out to -1), the code creates a degenerate
   zero-length Line mobject AND adds a self-loop edge to the networkx graph
   (G.add_edge(v, v) via parent_index=-1 indexing the last element).
   - Read the insertion loop first (roughly lines 1150-1260 for MaxHeap; 1250-1360 for MinHeap).
   - Guard BOTH the Line creation and the G.add_edge call with `if parent_index >= 0:` so the
     root case simply draws the node with no edge.
2. MaxHeap ~1239 / MinHeap ~1341: the post-sift comparison text uses arr[parent_index] which,
   when the inserted value bubbled all the way to the root, indexes with parent_index = -1 and
   compares against the LAST element — wrong on-screen text.
   - Guard the comparison-text creation with `if parent_index >= 0:` as well (when the value
     reaches the root there is no parent comparison to show). The demo sequences in both
     scenes DO hit this path, so the rendered videos change slightly — that is intended; say so
     in your report.

TASK — Animations/DivideAndConquer.py
3. LongestCommonSubsequence ~553-554: the DP table layout (np.hstack of a range column with the
   (m+1)x(n+1) matrix, then a vstack) only works when BOTH strings have equal length — crashes
   otherwise. Add a guard at the start of construct():
     if len(s1) != len(s2):
         raise ValueError("LCS demo animation currently requires equal-length strings")
   (find the actual variable names in the file). Generalizing to unequal lengths is FUTURE work
   — do not attempt it.
4. ClosestPairPoint ~465-469: the strip-check seeds only the pair (Sy[0], Sy[1]) then loops from
   i=1, so pairs (Sy[0], Sy[k>1]) are never compared — the true closest pair can be missed.
   Read the whole strip block, then rewrite it as the standard form:
   for i in range(len(Sy)): for j in range(i+1, len(Sy)): if (Sy[j].y - Sy[i].y) >= current_min:
   break; compare and update current_min. (Match the file's actual point representation — it may
   store x/y in attributes or tuples.) The demo input's FINAL ANSWER must be unchanged — verify
   by tracing the demo points; only the checking pattern changes.
5. Lines ~391-404: fade_in / fade_out are only defined inside `if` branches but used
   unconditionally at line ~404, and the final self.play(...) passes fade_in twice. Restructure
   so the two mobjects are always defined (compute once) and the conditional only picks WHICH
   text to Write, with a single play call that references each animation exactly once. Keep the
   visible output identical for the fixed demo input (the current branches catch small sizes
   first; state in your report which branch actually runs for this input).

CONSTRAINTS
- Minimal diffs; no refactors of surrounding animation code; no rendering; no commits.
- Do not rename anything; do not remove commented-out code (that is PROMPT 023).

VERIFICATION (all must pass)
1. python -c "import sys; sys.path.insert(0, 'Animations'); import Trees, DivideAndConquer" —
   imports clean.
2. Read-back proof: quote each guarded/rewritten block (3 lines context).
3. Trace proofs: (a) for the MaxHeap demo insertions, list which insertions hit parent_index=-1
   and confirm the videos' other steps are untouched; (b) for ClosestPairPoint, run the demo
   points through both the OLD logic (as a local throwaway script if helpful — do not leave
   files behind) and the NEW logic and show the closest pair is identical.

REPORT
- All diffs, import check, both trace proofs.
- Add "RB1" to Notes of TASKBOARD rows B13 and B14 (MaxHeap, MinHeap, LongestCommonSubsequence,
  ClosestPairPoint need re-render).
- Tick TASKBOARD rows B13, B14.
`````

### PROMPT 011 — Greedy labels + GIF converter + notebooks

Plan card(s): B15, B16, B17 (`docs/Plan/02-Bugfixes.md`) · Agent: dsa-bugfixer · Depends on: 001 · Tick TASKBOARD rows: B15, B16, B17

`````text
PROMPT 011 — MANIM FIXES #4 + CONVERTER + NOTEBOOKS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. Do NOT render scenes here (render
batch is PROMPT 012; only the Greedy scene queues for it). Bug details: docs/Audit/04-Bugs.md
section 5 (Greedy) and section 6 (converter). moviepy 2.2.1 is the installed version.

TASK — Animations/Greedy.py
1. IntervalScheduling: the timeline ruler labels are shifted one unit relative to the interval
   rectangles — tick i is labeled i+1 while intervals start at RIGHT * s (lines ~74-81 build
   the ruler; lines ~63-65 position intervals). Read both blocks, then fix the label
   generation so tick at x-coordinate i is labeled with the SAME value the interval starting at
   s aligns to (i.e., labels[0] == 0 aligns with the first interval's start position). The
   rendered video changes slightly (intended); say so in the report.

TASK — mp4_to_gif_converter.py + convert_mp4_to_gif.bat + requirements_converter.txt
2. mp4_to_gif_converter.py:
   a. Line ~74: gif_path = mp4_path.replace(".mp4", ".gif") — naive replace mangles paths where
      ".mp4" appears inside a directory name. Use pathlib:
      Path(mp4_path).with_suffix(".gif") (preserve the existing str/Path usage style of the file).
   b. Lines ~82-92: the conversion has no cleanup on failure — wrap the write_gif call in
      try/finally with clip.close() in the finally block.
   c. Line ~86: clip.resize(...) was removed in moviepy 2.x -> use clip.resized(...) with the
      same arguments.
3. convert_mp4_to_gif.bat: add `if errorlevel 1 exit /b 1` after the pip install line, and skip
   the pip install when a flag arg --no-install is passed (keep default behavior unchanged).
4. requirements_converter.txt: confirm it now reads moviepy>=2.0,<3.0 (PROMPT 001 should have
   set it; if not, set it now).

TASK — notebooks
5. Understanding/Graphs/Graphs.ipynb:
   a. In the Dijkstra cell (~cell 12): the neighbor test `adj_matrix[u][v] > 0` treats np.inf
      (non-edge) as a valid neighbor — works only by luck. Change to test
      `adj_matrix[u][v] < np.inf` (keep the rest of the relaxation logic identical).
   b. Rename the typo'd classes/variables: WieghtedDirectedGraph -> WeightedDirectedGraph,
      WieghtedUndirectedGraph -> WeightedUndirectedGraph, AMGaphD -> AMGraphD (rename ALL
      occurrences in ALL cells).
6. Understanding/Trees/Trees.ipynb: MinHeap.delete and MaxHeap.delete crash on a single-node
   heap (parent_of_last ends up None -> AttributeError) and skip the heapify-up step after
   replacement. Read both delete methods, then: guard the parent_of_last usage (if the heap has
   only the root, just remove it and return), and keep behavior identical for every case that
   already worked.
7. Execute BOTH notebooks end-to-end to prove they still run:
     jupyter nbconvert --to notebook --execute --inplace Understanding/Graphs/Graphs.ipynb
     jupyter nbconvert --to notebook --execute --inplace Understanding/Trees/Trees.ipynb
   (If jupyter/nbconvert is not installed, pip install it into the current environment first and
   note it; do NOT add it to requirements.txt — ask the user whether to pin it in
   requirements-dev.txt.)

CONSTRAINTS
- Minimal diffs everywhere; no refactors; no scene rendering; no commits.
- Notebooks: preserve cell outputs after execution (they are ground truth references).

VERIFICATION (all must pass)
1. All edited modules import: Animations/Greedy.py, mp4_to_gif_converter.py.
2. Converter live test: convert ONE small mp4 (pick the smallest under
   Animations/media/videos/SearchingAlgorithms/480p15/) to a gif in a TEMP directory (use the
   --output-dir option if the script has it, else test with --dry-run plus one real conversion
   and DELETE the produced gif afterwards — do not commit it) both with and without --resize;
   both succeed with moviepy 2.2.1.
3. Both notebooks execute fully with no errors (nbconvert exit 0).

REPORT
- Diffs summary; converter test evidence (command + output tail); notebook execution evidence.
- Add "RB1" to Notes of TASKBOARD row B15 (IntervalScheduling needs re-render).
- Tick TASKBOARD rows B15, B16, B17.
`````

### PROMPT 012 — Render batch RB1 (9 scenes)

Plan card(s): RB1 (`docs/Plan/02-Bugfixes.md`) · Agent: general (load skill: dsa-render) · Depends on: 008, 009, 010, 011 · Tick TASKBOARD rows: RB1

`````text
PROMPT 012 — RENDER BATCH RB1: RE-RENDER THE 9 SCENES FIXED IN PROMPTS 008-011

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-render" skill and
follow it. Source fixes for 9 scenes landed in PROMPTS 008-011; their rendered videos under
Animations/media/videos/ are now stale. Renders take minutes each — run exactly these 9, in this
order, and nothing else.

TASK
1. From the Animations/ directory render each scene at web quality (-ql = 480p15):
   Animations/AVLTree.py           -> LeftLeftCase
   Animations/Graphs.py            -> FloydWarshall, WeightedAdjecencyListUD, WeightedAdjecencyListD
   Animations/Trees.py            -> MaxHeap, MinHeap
   Animations/DivideAndConquer.py  -> LongestCommonSubsequence, ClosestPairPoint
   Animations/Greedy.py           -> IntervalScheduling
   Command pattern (run from inside Animations/):  manim <File>.py <Scene> -ql
2. If a render fails, capture the traceback, SKIP to the next scene, and report the failure —
   do not attempt code fixes during this batch.
3. Spot-check each output mp4 at the specific moments the fixes changed (expected locations):
   - LeftLeftCase: the on-screen label must read "Right Rotation" during the rotation.
   - FloydWarshall: a tableau step for intermediate vertex 0 must now exist; final matrix
     unchanged for this demo graph.
   - WeightedAdjecencyListUD / WeightedAdjecencyListD: adjacency list entries display as
     ordered pairs with parentheses — NO braces { } and stable order.
   - MaxHeap / MinHeap: during the insertion that bubbles a value to the ROOT there is no
     stray zero-length line/self-loop and no bogus "x <= y" comparison text at the root.
   - LongestCommonSubsequence / ClosestPairPoint: videos complete without errors (fixes were
     internal guards; visuals for the demo input should look unchanged).
   - IntervalScheduling: ruler tick labels align with the interval start positions.

CONSTRAINTS
- Render ONLY these 9 scenes, ONLY at -ql.
- Do NOT commit any media file without explicit user approval (AGENTS.md rule). Default:
  leave the new mp4s on disk uncommitted and tell the user what changed.
- Do not edit scene code in this prompt.

VERIFICATION (all must pass)
1. All 9 mp4s exist with fresh timestamps under the correct
   Animations/media/videos/<File>/480p15/ paths.
2. The spot-check list above is confirmed per video (report pass/fail per video).

REPORT
- Render time per scene, pass/fail spot-check table, any failures with tracebacks, and a clear
  statement of which files are new/uncommitted (awaiting the user's media-commit decision).
- Tick TASKBOARD row RB1.
`````

### PROMPT 013 — Phase 1 gate: adversarial re-verification

Plan card(s): G1 (`docs/Plan/02-Bugfixes.md`) · Agent: dsa-auditor · Depends on: 006, 007, 008, 009, 010, 011, 012 · Tick TASKBOARD rows: G1

`````text
PROMPT 013 — PHASE 1 GATE: INDEPENDENTLY RE-VERIFY EVERY BUGFIX CLAIM

CONTEXT
You are the independent auditor for D:\Git-Projects\DSA-Animations. Read AGENTS.md first. You
NEVER edit any file in this prompt (you may run read-only commands and the dev server). Bugfixes
PROMPT 002 and 006-012 claim to have fixed every row of docs/Audit/04-Bugs.md sections 1-4, and
the manim rows of section 5 at source level (9 scenes re-rendered). Your job: adversarially
confirm or refute, row by row.

TASK
1. Re-derive, do not trust: for EACH row in docs/Audit/04-Bugs.md sections 1, 2, 3, 4 — open
   the cited file/line and prove the bug no longer holds (link targets resolve; sample code is
   sorted + bounds-correct; complexity values match Understanding/*.ipynb or CLRS; CSS
   declarations valid; DB path uses instance_path; SECRET_KEY from env).
2. Section 5 (manim): confirm each source fix is present and correct in code (quotes with line
   numbers), and spot-watch at least THREE of the re-rendered videos from PROMPT 012
   (LeftLeftCase, one WeightedAdjecencyList*, MaxHeap) to confirm the on-screen fixes are
   actually visible in the rendered output.
3. Run the full verification stack yourself:
   - pytest -q                       (expect all green)
   - python tools/link_check.py      (expect exit 0, empty-or-header-only allowlist)
   - Route smoke: every one of the 25 routes returns 200 (302 for /logout) via the test client.
4. Hunt for collateral damage:
   - git status / git diff --stat over the whole tree: any unexpected files (DBs, logs, media)?
   - The 3 pages most edited (binary_search.html, stack.html, data_structures.html): open in the
     dev server, check the video + code-highlight sync still works and MathJax renders.
   - Confirm no AI-meta text regressed anywhere: grep templates for "the sources" etc.
5. Verify TASKBOARD hygiene: rows B1-B17, RB1 and F1-F6 are ticked with sensible notes.

REPORT (format — per item: VERIFIED / NOT FIXED / PARTIAL + file:line evidence)
- One line per audit row you re-checked (sections 1-4 fully; section 5 at source level + 3
  video spot-checks).
- Verification-stack outputs (summary + exit codes).
- Collateral-damage findings.
- Overall verdict: PHASE 1 PASSED / BLOCKED (with the blocker list).
- Tick TASKBOARD row G1 (only if verdict is PASSED; if BLOCKED, leave G1 unticked and list
  blockers).
`````

## Phase 2 — Sync Tool (the highlightMap generator)

### PROMPT 014 — Sync tool spike + design document

Plan card(s): T1 (`docs/Plan/03-Sync-Tool.md`) · Agent: explore · Depends on: 001 · Tick TASKBOARD rows: T1

`````text
PROMPT 014 — SPIKE: HOW TO RUN A MANIM SCENE WITHOUT RENDERING (RESEARCH + ONE DESIGN DOC)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. GOAL of the phase this spike opens:
today, website templates contain hand-eyeballed JS arrays ("highlightMap") mapping video
timestamps to code lines (see Website/website/templates/content.html lines 104-137, and
singly_linked_list.html lines 532-660 for the multi-video variant). They drift whenever a
scene's animation timings change. We will build tools/syncmap — a recorder that imports a Scene
class, runs construct() WITHOUT rendering, accumulates exact run_times from play()/wait() calls,
and records code_step(lines) events — producing machine-precise maps. This spike de-risks the
recorder design. This is a RESEARCH task: the ONLY file you may create/edit is
tools/syncmap/DESIGN.md. Do not write product code yet.

TASK — investigate and document in tools/syncmap/DESIGN.md
1. Read the existing manual harness for context: utils/createHighlightMap.ipynb (it re-simulates
   scenes' run_times by hand — we are productizing exactly this) and
   Website/website/templates/content.html:104-137 + LinkedList/singly_linked_list.html:532-660
   (the JS consumer formats).
2. Find the installed manim source: python -c "import manim, inspect; print(inspect.getfile(manim))"
   — then READ manim's Scene internals (scene/scene.py): Scene.__init__ (what renderer it
   requires), Scene.render, Scene.play, Scene.wait, Scene.add_sound, and how run_time is
   resolved from animations (animation.run_time, AnimationGroup, Succession, LaggedStart,
   LaggedStartFromEdges, Wait(duration), and the default 1s when play() gets no run_time).
   Cite exact manim source file paths + line numbers in the design doc.
3. Determine the cleanest recorder mechanism and RECOMMEND ONE:
   Option A: instantiate the Scene with a mock/null renderer object (what minimal interface
   must the fake renderer expose for construct() to complete without touching ffmpeg/GL?),
   Option B: monkey-patch Scene.play/Scene.wait on the instance/class with pure-Python
   replacements that only accumulate time.
   For the chosen option, list every method that must be patched (play, wait, and anything else
   that advances time or touches cairo/ffmpeg), and what a fake needs to provide (e.g. mobjects
   never get drawn — confirm Succession/LaggedStart still expose their total run_time without
   rendering).
4. Time model: write the exact rules (with manim source citations) for computing the cumulative
   timeline: default play run_time; explicit run_time kwarg; wait(d); wait() default; nested
   AnimationGroup/Succession/LaggedStart totals; lag_ratio effect on total duration (should be
   none — verify); anything Scene does at start/end (e.g. implicit waits) that contributes time.
   Note how scene-internal pause/sleeps or sound calls would be handled.
5. Risks & edge cases: scenes that depend on renderer state (Transform cached mobjects,
   updater functions with dt, scene.clock), scenes whose construct() builds mobjects that need
   a camera (e.g. .get_right() on rendered text) — does that work headless? Test empirically:
   try running construct() headless for 3 representative scenes (LinearSearch, TreeBFS,
   Dijkstra) via a throwaway python script (do NOT leave the script or any artifacts except
   DESIGN.md) and record what breaks and the workaround.
6. Event schema proposal for the timeline JSON (scene, module, manim_version, source_sha256,
   events[{t, type: play|wait|code_step, lines, key, run_time}]) and for the website map JSON
   (video, code[], map[{time, lines}]) — copy the consumer format from content.html exactly.
7. A step-by-step build plan for PROMPTS 015-019 (recorder, SyncedScene, snapshot CLI, map emit,
   check).

CONSTRAINTS
- Create exactly ONE file: tools/syncmap/DESIGN.md (create the folder). Nothing else. No repo
  edits, no commits. Throwaway scripts must be deleted after use.

VERIFICATION
1. DESIGN.md exists and covers items 2-7 with concrete manim-source citations and the empirical
   headless-run results for the 3 test scenes (including any failures + workarounds).
2. git status shows only tools/syncmap/DESIGN.md as new.

REPORT
- Summary of the recommended mechanism + the 3 empirical run results + top 3 risks.
- Tick TASKBOARD row T1.
`````

### PROMPT 015 — Sync tool: recorder core + SyncedScene convention

Plan card(s): T2, T3 (`docs/Plan/03-Sync-Tool.md`) · Agent: general · Depends on: 014 · Tick TASKBOARD rows: T2, T3

`````text
PROMPT 015 — RECORDER CORE (tools/syncmap/recorder.py) + SyncedScene (Animations/synced.py)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. PROMPT 014 produced
tools/syncmap/DESIGN.md — read it fully and implement its recommended recorder mechanism and
time model. Create the tools/syncmap package now (tools/syncmap/__init__.py, recorder.py, and
tests). The website's JS consumes maps shaped like: [{"time": 1.5, "lines": "3-5"}, ...]
(content.html:104-137).

TASK
1. Animations/synced.py — the annotation convention (zero rendering impact):
     from manim import Scene
     class SyncedScene(Scene):
         DISPLAY_CODE: list[str] = []          # exact code the website page displays
         def code_step(self, lines: str, key: str = "") -> None:
             """No-op while rendering. The syncmap recorder captures the current timestamp."""
   That is all. Importing it must not start any renderer or print anything.
2. tools/syncmap/recorder.py — implement per DESIGN.md:
   - A function record_scene(module_path: str, scene_name: str) that imports the module,
     finds the Scene subclass, runs construct() headless, and returns the event list
     [{t, type: "play"|"wait"|"code_step", lines, key, run_time}, ...] with cumulative times.
   - The patched play/wait accumulate time EXACTLY per the design doc's time model (default
     run_time, explicit run_time, wait durations, nested group totals).
   - code_step events capture the timestamp at call time and do NOT advance it.
   - Deterministic: same source -> byte-identical event list (no dict-ordering or
     float-precision surprises — round times to a fixed precision, e.g. 1e-9, consistently).
   - A scene that does not subclass SyncedScene records fine too (it just yields no
     code_step events) — print a warning that the scene has no code annotations.
   - A scene whose construct() raises: capture the traceback into the returned result object
     ({'error': str(e), 'traceback': ...}) instead of crashing the caller.
3. Unit tests (tests/test_syncmap_recorder.py) with SYNTHETIC minimal Scene subclasses defined
   inside the test module (they may subclass SyncedScene directly):
   - play with default run_time -> event t=0, run_time=1.0; a second play -> t=1.0.
   - wait(2) -> t advances by 2.0.
   - play(run_time=0.5) honored.
   - code_step("3-5") between plays records at the CURRENT t and does not advance time;
     code_step BEFORE any play records at t=0.
   - a Succession or LaggedStart totals its parts (assert the total, per DESIGN.md's model).
   - determinism: record the same synthetic scene twice -> identical lists.
   - an empty construct() -> zero events, no error.
   (If constructing bare Scene subclasses headless requires a renderer trick, follow
   DESIGN.md — the spike validated this.)

CONSTRAINTS
- Do NOT touch any existing animation file (Trees.py etc.) — synthetic test scenes only.
- No new pip dependencies.
- No rendering anywhere; the recorder must run a full scene in seconds.

VERIFICATION (all must pass)
1. pytest -q fully green (old tests + new recorder tests).
2. Live proof: run a small throwaway python snippet that records a REAL scene
   (Animations.SearchingAlgorithms LinearSearch) and prints its event list; total duration must
   equal a manual sum of the play/wait run_times you read from the scene source (compute the
   manual sum in the snippet by counting the first 8 play/wait calls in the file's construct()).
3. Importing Animations/synced.py and recording a non-SyncedScene both produce the expected
   warnings without errors.

REPORT
- DESIGN.md mechanism actually used; test results; the LinearSearch manual-sum proof
  (computed vs recorded total).
- Tick TASKBOARD rows T2, T3.
`````

### PROMPT 016 — Sync tool: snapshot CLI

Plan card(s): T4 (`docs/Plan/03-Sync-Tool.md`) · Agent: general · Depends on: 015 · Tick TASKBOARD rows: T4

`````text
PROMPT 016 — SNAPSHOT CLI (python -m tools.syncmap snapshot)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. PROMPT 015 built
tools/syncmap/recorder.py (record_scene -> events). Now wrap it in a CLI that produces
byte-comparable timeline JSON files — these become the BEHAVIOR-PRESERVATION ORACLE for the
Phase 3 refactor: before/after a refactor, snapshots must be byte-identical.
Target layout:
  tools/syncmap/timelines/<SceneName>.json   {"scene": ..., "module": ..., "manim_version": ...,
                                              "source_sha256": <sha256 of the scene's module file>,
                                              "events": [...]}
  tools/syncmap/timelines/manifest.json     {"scenes": {...scene: module...}, "generated": ...,
                                              "errors": [...]}
Note the "module" for each scene must be the dotted path (e.g. "Animations.Trees"), NOT a
filesystem path, so the timeline identifies code, not files.

TASK
1. Create tools/syncmap/__init__.py, cli.py, __main__.py such that this works:
     python -m tools.syncmap snapshot --scene Animations.Trees TreeBFS
     python -m tools.syncmap snapshot --all --batch 10
   - --scene: module + scene name -> record -> write timelines/<Scene>.json (create dirs).
   - --all: enumerate EVERY Scene subclass across the 11 modules in Animations/ (import each
     module, walk vars() for Scene subclasses defined in it), record each, write files +
     manifest. --batch N records N scenes per progress line. Scene modules to enumerate:
     SearchingAlgorithms, SortingAlgoritms, Arrays, LinkedList, Stack-Queue, Trees, AVLTree,
     BTrees, Graphs, DivideAndConquer, Greedy (note Stack-Queue and the SortingAlgoritms
     spelling — import exactly as the files are named; also skip helper classes like Node,
     BTree, WeightedLine, DAGArrow, NodeVisual, AVLNode, ListElement, BTreeElement — anything
     that is not a Scene subclass, and skip imported base classes like Scene itself).
   - JSON must be deterministic: json.dump(..., sort_keys=True, separators=(",", ":")) — two
     runs over the same code must produce byte-identical files.
   - Round all times consistently (recorder already does).
   - Scene errors are recorded in manifest["errors"], never abort the batch.
2. Tests (tests/test_syncmap_cli.py):
   - snapshot of ONE synthetic scene (from a test fixture module) writes valid JSON with the
     schema above.
   - Determinism test: snapshot the same scene twice; assert file bytes equal.
   - Manifest error path: a scene that raises in construct() lands in errors, exit code still 0,
     and no timeline file is written for it.

CONSTRAINTS
- --all must NOT render or write anything outside tools/syncmap/timelines/.
- No modification of any Animations file in this prompt.
- CLI must work from repo root; use importlib, never exec/subprocess on generated code.

VERIFICATION (all must pass)
1. python -m tools.syncmap snapshot --scene Animations.SearchingAlgorithms LinearSearch
   writes a timeline with sensible events; re-run -> byte-identical file (prove with a hash
   compare, e.g. Get-FileHash / sha256sum, in your report).
2. pytest -q fully green.
3. Dry benchmark: time the --all run of ONE small module (Animations.SearchingAlgorithms — 2
   scenes) and report seconds per scene (budget: <30s per scene; if exceeded, note which scenes
   and why — do not optimize yet, just report).

REPORT
- Files created; the hash-determinism proof; the small-module benchmark; any scenes that error
  and their tracebacks (from manifest errors).
- Tick TASKBOARD row T4.
`````

### PROMPT 017 — Sync tool: map emission + website loader

Plan card(s): T5 (`docs/Plan/03-Sync-Tool.md`) · Agent: general · Depends on: 016 · Tick TASKBOARD rows: T5

`````text
PROMPT 017 — MAP EMISSION (sync/<slug>.json) + WEBSITE LOADER UPGRADE

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. PROMPTs 015-016 built the recorder
and snapshot CLI. Now: (a) the "map" command that turns a SyncedScene's DISPLAY_CODE + code_step
events into the JSON a website page consumes, and (b) the content.html loader upgrade so pages
can load maps from JSON files instead of inline JS. Current consumer behavior
(content.html:104-137): a global JS array highlightMap = [{time, lines}, ...] is scanned every
100ms against video.currentTime; the matched "lines" string is set as the code block's
data-line attribute and Prism re-highlights. Multi-video pages (singly_linked_list.html:532-660)
use several named arrays + a mapVar registry. DO NOT BREAK any of that — the inline path keeps
working untouched; JSON is an ADDITIVE path.

TASK
1. Add the map command to tools/syncmap (python -m tools.syncmap map <Module> <Scene>
   --slug <slug> --category <Category>):
   - Requires the scene to subclass SyncedScene (error with a helpful message if not).
   - Output: Website/website/static/sync/<slug>.json:
       {"video": "Videos/<Category>/<Scene>.webm",
        "code":  [...DISPLAY_CODE lines...],
        "map":   [{"time": <t>, "lines": "<lines>"}, ...]}
   - Validation before writing: every map entry's lines references valid line numbers — parse
     "lines" as a Prism data-line spec (integers, ranges "a-b", comma lists) and check every
     number is >= 1 and <= len(DISPLAY_CODE). Fail loudly on violations.
   - Times come from code_step events (the timestamp of each event; dedupe consecutive entries
     with identical "lines"; ALWAYS include a final sentinel entry at the last event time if the
     last code_step differs from the first, so highlighting ends sensibly — just dedupe, no
     invention).
2. Upgrade the loader in Website/website/templates/content.html (keep it vanilla JS):
   - If the page's video container (the element holding <video id="code-video">) has a
     data-sync attribute (a URL), fetch it on DOMContentLoaded; on success use the fetched
     {map} as highlightMap and (if the code block is empty or has data-from-sync) fill the
     <code> element's text with the fetched code joined by newlines, then Prism.highlightElement.
   - On fetch failure or no data-sync attribute: existing inline-highlightMap behavior, byte for
     byte.
3. PROOF PAGE (temporary, then removed): create a scratch route /__sync_test__ + minimal
   template in Website/website/views.py + templates/ that extends content.html and contains ONE
   video + code block wired via data-sync to a real map. Steps:
   a. Edit Animations/SearchingAlgorithms.py: make LinearSearch subclass SyncedScene, add
      DISPLAY_CODE with the same ~10-line linear-search snippet the existing
      SearchingAlgorithms/linear_search.html page displays (read that template), and insert
      code_step("N") calls immediately before each self.play(...) that demonstrates code line N
      (watch the mp4 or read the scene to place them faithfully). This edit is SMALL and must
      not change animations/timings — only add the subclass, the attribute, and no-op calls.
   b. python -m tools.syncmap map Animations.SearchingAlgorithms LinearSearch --slug
      linear-search-test --category SearchingAlgorithms
   c. Point the scratch page's video at the EXISTING linear search webm
      (static/Videos/SearchingAlgorithms/LinearSearch.webm) and its data-sync at the new JSON.
   d. Open the page; confirm the code block content comes from JSON and highlighting tracks the
      video PRECISELY (watch fully once; compare with the hand-eyeballed inline map on the real
      /linear search page and report differences in seconds).
   e. AFTER verification: remove the scratch route/template AND the scratch JSON — but KEEP the
      LinearSearch SyncedScene annotation (it is harmless and useful later).
4. Tests (tests/test_syncmap_map.py): validation failures (lines out of range), dedupe of
   consecutive identical entries, JSON shape, non-SyncedScene error message. Also a Flask test
   that GETs a page with data-sync (reuse the scratch page before you delete it, or a fixture
   template) and asserts 200 + the JSON URL resolves via the test client.

CONSTRAINTS
- The content.html change must keep working when neither fetch nor inline map exists.
- The LinearSearch annotation edit must not alter the timeline: after editing, re-run
  python -m tools.syncmap snapshot --scene Animations.SearchingAlgorithms LinearSearch and
  diff against the snapshot from PROMPT 016 — must be byte-identical (proves code_step is a
  true no-op in the event stream).
- Do not migrate any real page in this prompt.

VERIFICATION (all must pass)
1. All map unit tests + existing tests green (pytest -q).
2. The proof page demonstration works as described (report the observed sync quality and the
  differences vs the eyeballed inline map).
3. Snapshot determinism proof after the LinearSearch edit (hash equal).
4. Scratch route/template/JSON removed afterwards; git status clean of them.

REPORT
- The map JSON emitted; loader diff summary; proof-page evidence; determinism hashes.
- Tick TASKBOARD row T5.
`````

### PROMPT 018 — Sync tool: drift check + documentation

Plan card(s): T6, T8 (`docs/Plan/03-Sync-Tool.md`) · Agent: general · Depends on: 016, 017 · Tick TASKBOARD rows: T6, T8

`````text
PROMPT 018 — DRIFT CHECK (python -m tools.syncmap check) + TOOL DOCUMENTATION

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. The syncmap tool now has snapshot
(PROMPT 016) and map (PROMPT 017). "check" is the guard that keeps everything honest from now
on: it re-derives live timelines/maps and compares them with the committed ones, so any timing
change someone forgot to regenerate is caught.

TASK
1. Add the check command:
     python -m tools.syncmap check [--legacy]
   - Live vs timelines: for every scene with a committed timeline in tools/syncmap/timelines/,
     re-record it and compare event lists; report scene name + first differing event for any
     mismatch. (Comparing committed JSON's events against fresh recording; byte-compare the
     re-serialized JSON for simplicity.)
   - Live vs maps: for every file in Website/website/static/sync/, re-derive the map from the
     scene (as the map command does, into a temp buffer) and compare JSON; report drift.
   - --legacy: additionally parse templates for inline JS maps (the pattern is
     "const <name>HighlightMap = [" / "const highlightMap = [" followed by JSON-ish
     {time:..., lines:"..."} entries) and report pages whose inline maps roughly correspond to
     scenes whose live recording differs by more than 1.0s at any code_step — informational
     warnings only (legacy pages are hand-eyeballed; exact comparison is impossible by design).
   - Exit code 0 = no drift; 1 = drift found; print a summary table (checked / clean / drifted).
2. Tests (tests/test_syncmap_check.py):
   - A committed timeline that matches live -> clean.
   - INJECT drift: copy a synthetic scene, snapshot it, mutate the source's run_time (in the
     test fixture only), re-check -> must flag. (Clean up the fixture state afterwards.)
   - A missing timeline for an existing scene = warning listing what is un-snapshotted, exit 0.
3. Write tools/syncmap/README.md:
   - What the tool is for (replaces hand-eyeballed highlightMap JS; doubles as refactor oracle).
   - The SyncedScene/DISPLAY_CODE/code_step convention with the code block from
     Animations/synced.py.
   - CLI usage for snapshot / map / check with concrete command lines and the output schemas.
   - The time model in 5 lines (point to DESIGN.md for details).
   - How a page consumes a map (content.html data-sync loader).
4. Cross-check the "dsa-highlightmap" skill (.opencode/skills/dsa-highlightmap/SKILL.md)
   against what you actually built — if CLI flags or schemas drifted from the skill text,
   DO NOT edit the skill yourself; instead list every discrepancy in your report (the user
   will update the skill).

CONSTRAINTS
- No changes to scene files, templates, or committed timelines in this prompt (the injected
  drift in tests is fixture-local).
- Do not edit .opencode/skills/ (report-only for discrepancies).

VERIFICATION (all must pass)
1. python -m tools.syncmap check -> exit 0 today (LinearSearch timeline from PROMPTs 016-017
   still matches; report the checked-scene count).
2. Manual injection proof (then revert): temporarily change one run_time in
   Animations/SearchingAlgorithms.py LinearSearch, run check -> it MUST flag that scene; revert
   the edit, re-run check -> clean. Report both outputs.
3. pytest -q fully green.

REPORT
- check outputs (before/after injection/reverted), README content summary, skill discrepancies
  list.
- Tick TASKBOARD rows T6, T8.
`````

### PROMPT 019 — Baseline snapshots of all 72 scenes

Plan card(s): T7 (`docs/Plan/03-Sync-Tool.md`) · Agent: general · Depends on: 012, 015 · Tick TASKBOARD rows: T7

`````text
PROMPT 019 — BASELINE SNAPSHOTS: THE REFACTOR ORACLE FOR ALL 72 SCENES

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. Phase 1 manim bugfixes (PROMPTs
008-012) are DONE — the code is in its post-fix state. These snapshots capture today's
behavior so the Phase 3 refactor (PROMPTs 021-028) can prove it changed nothing. IMPORTANT:
this prompt's output files are meant to be COMMITTED — after your verification, explicitly tell
the user "ready to commit tools/syncmap/timelines/" (or commit if the user already said
"commit" for this session).

TASK
1. Run the full baseline:
     python -m tools.syncmap snapshot --all --batch 10
2. Expected scene count: the audit counted 72 Scene classes across 11 modules
   (SearchingAlgorithms 2, SortingAlgoritms 6, Arrays 4, LinkedList 9, Stack-Queue 2, Trees 14,
   AVLTree 6, BTrees 1, Graphs 22, DivideAndConquer 4, Greedy 2). The manifest must show every
   module enumerated (some scenes may be skipped if their count differs — reconcile the count
   and explain any difference in your report).
3. For every scene that ERRORED (manifest["errors"]): read the traceback, classify the cause:
   - needs-renderer internals (DESIGN.md should have predicted some) -> document it in the
     manifest errors as a KNOWN LIMITATION (do not code around it in this prompt);
   - anything else -> report it to the user as a blocker finding BEFORE finishing.
4. Determinism pass: re-run --all a second time; compare file hashes — every timeline must be
   byte-identical between the two runs (any nondeterminism found: fix in the recorder and
   re-run; report what you fixed).
5. Report the total on-disk size of tools/syncmap/timelines/ (should be a few MB at most).

CONSTRAINTS
- This prompt writes ONLY under tools/syncmap/timelines/.
- Do not touch any animation source code (if determinism requires a recorder fix, that is a
  tools/syncmap change, not a scene change).
- No rendering, no media writes.

VERIFICATION (all must pass)
1. timelines/ contains one JSON per successfully recorded scene + manifest.json; count matches
   the reconciliation in step 2.
2. Two-run hash determinism proof (include the hash of 3 sample timelines from each run).
3. python -m tools.syncmap check -> exit 0 (committed state matches live).
4. pytest -q green.

REPORT
- Scene count reconciliation; errors classification; determinism proof; total size; the
  "ready to commit" statement.
- Tick TASKBOARD row T7.
`````

### PROMPT 020 — Phase 2 gate

Plan card(s): G2 (`docs/Plan/03-Sync-Tool.md`) · Agent: dsa-auditor · Depends on: 014, 015, 016, 017, 018, 019 · Tick TASKBOARD rows: G2

`````text
PROMPT 020 — PHASE 2 GATE: AUDIT THE SYNC TOOL

CONTEXT
You are the independent auditor for D:\Git-Projects\DSA-Animations. Read AGENTS.md first. You
NEVER edit files. PROMPTs 014-019 built tools/syncmap (DESIGN.md, recorder, SyncedScene,
snapshot/map/check CLIs, README, baseline timelines). This gate certifies the tool before the
refactor phase relies on it.

TASK
1. Determinism re-proof: run python -m tools.syncmap snapshot --all --batch 10 into the real
   timelines dir and diff hashes against what is committed — 100% byte-identical required.
   (Read-only verdict: if the two runs differ, the phase FAILS.)
2. Map correctness audit: verify the one live proof artifact allowed to remain — the LinearSearch
   SyncedScene annotation (PROMPT 017): 
   - confirm the annotation added no play/wait/codes that altered the LinearSearch timeline
     (timeline hash matches the pre-annotation pattern: re-record and compare to committed).
   - emit a fresh map with the map command to a TEMP path, validate its lines vs DISPLAY_CODE,
     and diff against the linear-search-test JSON if any trace remains — else confirm the
     scratch artifacts are fully removed (route, template, JSON).
3. Drift-detection proof: temporarily (in a scratch checkout — do NOT touch the repo's files;
     use python -c monkeypatching or copy the module) verify check flags a 0.5s run_time
     change on one scene and passes after revert. Report the mechanism you used to prove it
     without editing committed files.
4. Tool docs audit: read tools/syncmap/README.md against the actual CLI (--help output) and
   the Animations/synced.py convention — list any inaccuracies. Read the
   dsa-highlightmap skill and list discrepancies (report-only).
5. Full stack: pytest -q green; link checker exit 0; 25 routes smoke (200 / 302).
6. TASKBOARD hygiene: T1-T8 ticked with notes.

REPORT
- Per audit item: VERIFIED / FAILED + evidence (commands + outputs).
- Verdict: PHASE 2 PASSED / BLOCKED + blocker list.
- Tick TASKBOARD row G2 (only on PASSED).
`````

## Phase 3 — Refactor (behavior-preserving, oracle-proven)

> Every Phase 3 prompt MUST re-run `python -m tools.syncmap check` before and after its edits.
> Timeline files must stay byte-identical unless the prompt lists expected visual diffs
> (PROMPT 024 is the only one). That is the whole point of the baseline from PROMPT 019.

### PROMPT 021 — common.py shared visual classes

Plan card(s): R1 (`docs/Plan/04-Refactor.md`) · Agent: dsa-refactorer · Depends on: 020 · Tick TASKBOARD rows: R1

`````text
PROMPT 021 — REFACTOR #1: EXTRACT DUPLICATED VISUAL CLASSES INTO Animations/common.py

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then the dsa-refactorer agent rules:
BEHAVIOR MUST NOT CHANGE. The oracle is the timeline baseline (PROMPT 019) — run
python -m tools.syncmap check BEFORE you start (must be clean) and AFTER (must be clean again;
this prompt has NO expected visual diffs). The audit's duplication inventory is
docs/Audit/02-Implemented-But-Can-Be-Improved.md section 1 (items 1-4, 7).

TASK
1. Create Animations/common.py (Animations/env_config.py shows the existing shared-module
   style). Import env_config constants there rather than redefining them.
2. Consolidate these duplicated classes/helpers into common.py (one implementation each,
   parameterized for the small variations — compare ALL copies first and list the varying
   parameters in your report):
   a. ListElement — copies in SearchingAlgorithms.py:9-33, SortingAlgoritms.py:7-31,
      Arrays.py:13-31, plus a variant in DivideAndConquer.py:9-35 (some are VGroup-based,
      some plain; one canonical class may need a flag or the two shapes may genuinely differ —
      if they differ visually, keep TWO clearly-named variants in common.py and say why).
   b. Node / NodeVisual — copies in Arrays.py:33-48, Trees.py:14-35, Graphs.py:10-25,
      AVLTree.py:14-35 (NodeVisual), SortingAlgoritms.py:540-561.
   c. WeightedLine — Graphs.py:28-87 and Greedy.py:138-186 (the Greedy one handles background
      differently — capture that as a parameter).
   d. make_dynamic_bezier_updater + make_arrowhead_updater — the SAME ~16-line pair is
      copy-pasted into all 7 LinkedList scenes (LinkedList.py:145-160, 226-242, 308-324,
      396-412, 523-538, 639-654, 957-981) and partly in Trees.py playSurroundingNodeAnimation.
   e. playSurroundingNodeAnimation — copied into 3 scenes (Trees.py:40-48, 846-854, 939-947,
      1025-1033).
3. Migrate every usage file-by-file (delete the local copy, import from common) in this order,
   running the oracle after EACH file: SearchingAlgorithms, Arrays, SortingAlgoritms,
   DivideAndConquer, Greedy, Graphs, AVLTree, Trees, LinkedList.
4. If any pair of "duplicates" turns out NOT to be identical in behavior (different mobject
   hierarchy, different defaults that scenes rely on), STOP for that pair: leave it duplicated,
   and report it as a false positive. Do not force it.

CONSTRAINTS
- Behavior preservation is the ONLY acceptance criterion: every scene's timeline must hash
  unchanged. If a migration perturbs any timeline (e.g. a default color differs by one
  constant), revert that file's migration and report it — do not "fix" scenes to match.
- No renames of public Scene class names. No changes to views/templates.
- No new dependencies. No comments/no dead code left behind.

VERIFICATION (all must pass)
1. python -m tools.syncmap check -> exit 0 BEFORE starting and AFTER finishing (no drift).
2. Visual spot-render: render exactly ONE scene that uses migrated helpers —
   SortingAlgoritms.py BubbleSort at -ql (load the dsa-render skill) — and compare it
   side-by-side with the existing committed mp4: colors, spacing, and motion identical.
3. grep proof: the duplicated definitions are gone (e.g. "class ListElement" only in
   common.py; the updater pair defined only once; list each grep with counts).
4. pytest -q green; link checker exit 0.

REPORT
- The canonical-vs-variant decisions with parameter lists; per-file migration + oracle result;
  the BubbleSort visual comparison verdict; any false positives you left alone.
- Tick TASKBOARD row R1.
`````

### PROMPT 022 — Traversal + edge-removal helpers

Plan card(s): R2, R3 (`docs/Plan/04-Refactor.md`) · Agent: dsa-refactorer · Depends on: 021 · Tick TASKBOARD rows: R2, R3

`````text
PROMPT 022 — REFACTOR #2: BFS/DFS BOILERPLATE + BST EDGE-REMOVAL BLOCKS -> SHARED HELPERS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. Same rules as PROMPT 021:
oracle-clean before and after; NO expected visual diffs. Inventory: docs/Audit/02 section 1
(items 5-6).

TASK
1. The ~90-line BFS/DFS animation while-loop exists 6 times:
   - Animations/Trees.py:285-341 (TreeBFS), :395-451 (TreeDFS)
   - Animations/Graphs.py:365-427 (UndirectedGraphBFS), :469-531 (UndirectedGraphDFS),
     :746-808 (DirectedGraphBFS), :850-912 (DirectedGraphDFS)
   Read all six, map their varying parts (adjacency structure, container type queue/stack,
   neighbor ordering, label formatting, visit-coloring, per-step extra animations, positioning
   lookups), and write ONE helper in Animations/common.py, e.g.
   animate_traversal(scene, structure, *, use_stack=False, neighbors_of=..., on_visit=...,
   label=...) with hook callbacks for the varying bits. Migrate all 6 sites.
2. The ~55-line "find the mobject line connecting two nodes and fade/remove it" block exists 7
   times inside Trees.py's BST deletion scene (:1688-1704, :1735-1751, :1754-1769, :1811-1827,
   :1830-1845, :1936-1952, :1960-1975). Write ONE helper (e.g. remove_edge_visual(scene,
   lines_group, parent_node, child_node) returning the removed mobject) and migrate all 7 sites.
3. Oracle discipline: after migrating Trees.py run the check; then after Graphs.py run it again.
   All timelines byte-identical.

CONSTRAINTS
- Same acceptance rule as PROMPT 021: any timeline drift = revert that site and report.
- Keep each scene's observable animation sequence EXACTLY (same play order, same run_times,
  same wait durations). The helper may take as many keyword hooks as needed — do not compress
  behavior to fit a simpler signature.
- No renames, no renames of Scene classes, no template changes.

VERIFICATION (all must pass)
1. python -m tools.syncmap check -> exit 0 before and after.
2. grep proof: the while-loop signature fragments (e.g. "while len(queue)" / the
   edge-search idiom) appear once (helper) instead of 6/7 times — report grep counts before
   vs after.
3. pytest -q green; link checker exit 0.

REPORT
- Helper signatures; per-site migration table with oracle results; any sites you had to leave
  because the pattern genuinely diverged.
- Tick TASKBOARD rows R2, R3.
`````

### PROMPT 023 — Dead-code sweep + BTrees logger

Plan card(s): R4, R5 (`docs/Plan/04-Refactor.md`) · Agent: dsa-refactorer · Depends on: 021 · Tick TASKBOARD rows: R4, R5

`````text
PROMPT 023 — REFACTOR #3: DEAD CODE SWEEP + BTREES LOGGER SIDE-EFFECTS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. Same oracle rules: check clean
before and after; NO expected visual diffs (dead code cannot change timelines — if it does,
the "dead" code was alive and you must revert). Inventory sources: docs/Audit/03 (section 2)
and docs/Audit/02 (items 14, 16-19 of section 3).

TASK — remove dead code (verify each with a grep/usage check BEFORE deleting; if used, leave it
and report the false positive)
1. Animations/AVLTree.py: insert_into_AVLTree() + insert() (~1551-1611, unused — construct uses
   build_tree_silently); reconnect_after_rotation() (~1545-1549); duplicate
   old_balance/new_balance computation (~282-285).
2. Animations/BTrees.py: remove_keys_after() (~188-191).
3. Animations/Graphs.py: the Prim's distance dict that is written but never read
   (~1919-1930 and the write at ~1986-1988) — remove the dict AND its writes (keep the
   try/except KeyError edge lookup unless you can simplify it safely; when in doubt leave it).
4. Animations/Trees.py: networkx graphs built/updated but never rendered in MaxHeap/MinHeap
   (~1262, ~1364 — the G.ghost graph); duplicated assignments in BinarySearchTreeDeletion
   (~1390-1394) and the parent_node assigned-then-overwritten pattern (~1404 -> ~1450).
5. Animations/Greedy.py: the always-true hasattr check (~393).
6. Debug prints: Animations/AVLTree.py:293, 297, 301, 307, 381.
7. Commented-out code blocks (delete exactly these): Arrays.py:229-233, Stack-Queue.py:243-248,
   Trees.py:2121, Graphs.py:131-142, Graphs.py:994-995, Graphs.py:1025-1036, Graphs.py:1230-1231,
   Graphs.py:1570-1572, Graphs.py:1991, DivideAndConquer.py:436-437, :440, :522. (Line numbers
   are approximate post-Phase-1 — relocate by reading the surrounding code; these are
   "# self.play" blocks, "# print(minCost)", "#print(Px, Py)" style remnants.)
8. Unused imports everywhere: run `ruff check Animations --select F401,F403` and remove every
   unused import it lists (expect Percent/Pixels/CurvedArrow across 7 files). Also fix the
   mid-file imports: SortingAlgoritms.py ~535-538 (import networkx inside a class; move to
   top; DELETE the local EDGE_COL/NODE_COL re-definitions that shadow env_config), and
   DivideAndConquer.py ~268 (from math import ... mid-file -> top).
9. Loop-variable shadowing (rename inner index; pure rename, no logic change):
   LinkedList.py:703/:745 inner `for i in range(num_objects-1)` shadowing outer i (and the
   `nodes[_]` idiom), Graphs.py:105-107, :547-548, :999-1000, :1235-1236 (same pattern).
10. Animations/BTrees.py logger hijack (lines ~6-23): the module does logging.basicConfig(...)
    at import time and writes btree_operations.log into the source tree, with ~90 INFO calls
    that never emit (level=WARNING). Replace with: a module-level
    `logger = logging.getLogger(__name__)`, DELETE the basicConfig + FileHandler lines, and
    change the log-file-writing INFO calls to logger.debug calls ONLY where they carry
    genuinely useful info; delete the rest of the noise. Importing the module must now
    produce zero side effects (no file, no output).

CONSTRAINTS
- Before deleting ANY function/dict/block: grep the whole repo for its name/usage. Only delete
  when unused. Report every "kept because actually used" case.
- The oracle must stay clean; a dirty oracle after a deletion means the code was NOT dead —
  revert it.
- Do not touch Animations/synced.py, tools/, Website/ (Website dead code is a Phase 5 concern).

VERIFICATION (all must pass)
1. python -m tools.syncmap check -> exit 0 before and after.
2. python -c "import sys; sys.path.insert(0,'Animations'); import BTrees" in a scratch cwd ->
   no btree_operations.log created anywhere; no console output (run from a temp dir to be sure,
   then verify no stray file was made).
3. `ruff check Animations --select F401,F403` -> zero findings.
4. pytest -q green; link checker exit 0.

REPORT
- Removal table (item -> where -> proof of unused), false positives kept, logger diff summary,
  oracle status, LOC removed total.
- Tick TASKBOARD rows R4, R5.
`````

### PROMPT 024 — Typo renames (SortingAlgorithms, Adjacency, Prim's, AVLNode typing)

Plan card(s): R6 (`docs/Plan/04-Refactor.md`) · Agent: dsa-refactorer · Depends on: 021 · Tick TASKBOARD rows: R6

`````text
PROMPT 024 — REFACTOR #4: TYPO RENAMES (THE ONLY PHASE-3 PROMPT WITH EXPECTED VISUAL DIFFS)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. THIS prompt intentionally changes
on-screen text in 8 videos, so the oracle WILL report drift for exactly 8 scenes — those diffs
are expected and must match the exact list below; ANY other scene drifting = revert. Renders
happen in PROMPT 028. Inventory: docs/Audit/02 section 2.

TASK
1. RENAME THE SORTING FILE:
   - git mv Animations/SortingAlgoritms.py Animations/SortingAlgorithms.py
   - git mv Animations/media/videos/SortingAlgoritms Animations/media/videos/SortingAlgorithms
   - Update mp4_to_gif_converter.py (~line 56 category list): SortingAlgoritms ->
     SortingAlgorithms.
   - tools/convert_webm.py: register the alias CATEGORY_ALIASES = {"SortingAlgoritms":
     "SortingAlgorithms"} if the media dir still has any old-name references (the git mv makes
     the dir new-named; the alias keeps old gifs/mp4 paths working if any remain).
   - Grep the whole repo for "SortingAlgoritms" and update every CODE/CONFIG/TOOL occurrence.
     Historical documents (docs/Audit/*, docs/Plan/*, this prompts file) keep the old spelling
     where it describes the PAST state — do not rewrite history in docs; only fix live code,
     configs, and tooling.
   - CAUTION: manim derives its output dir from the module file name, so future renders of the
     6 sort scenes will write into media/videos/SortingAlgorithms — consistent with the git mv.
2. RENAME THE 8 ADJACENCY CLASS NAMES in Animations/Graphs.py (classes only, and their
   on-screen TITLES):
   AdjecencyMatrixUD -> AdjacencyMatrixUD, AdjecencyListUD -> AdjacencyListUD,
   AdjecencyMatrixD -> AdjacencyMatrixD, AdjecencyListD -> AdjacencyListD,
   WeightedAdjecencyMatrixUD -> WeightedAdjacencyMatrixUD,
   WeightedAdjecencyListUD -> WeightedAdjacencyListUD,
   WeightedAdjecencyMatrixD -> WeightedAdjacencyMatrixD,
   WeightedAdjecencyListD -> WeightedAdjacencyListD.
   Also fix every RENDERED title string "Adjecency ..." -> "Adjacency ..." in those scenes
   (audit cites Graphs.py:206, 666, 1094, 1330 plus any other occurrences you find).
   Then update tools/syncmap/timelines/manifest.json by RE-RUNNING
   `python -m tools.syncmap snapshot --all --batch 10` — the manifest and the 8 scenes'
   timelines will change (new module-internal names in event keying? class names in filenames?)
   — whatever files change, they must correspond ONLY to the 8 renamed scenes. List every
   changed file in your report.
   NOTE: the old media/video filenames for these 8 scenes (Adjecency*.mp4) will be re-rendered
   under new names in PROMPT 028; do NOT rename the old mp4s by hand (media rule).
3. Website typo: Website/website/templates/base.html:184 "Prims's Algorithm" -> "Prim's
   Algorithm" (footer text; it may currently be hidden per PROMPT 006 — fix it wherever it is).
4. Animations/AVLTree.py: the AVLNode class types value as int but scenes construct it with
   strings ("X", "Y", "5"). Change the annotation to `str | int` on the constructor parameter
   and the self.value attribute (typing only; no runtime change).
5. Expected-drift ledger (verify exactly these and NOTHING else changed):
   - tools/syncmap timelines: 8 Adjacency scenes — their code_step/play events unchanged BUT
     module/class identity fields change (if the timeline stores scene/module names, the files
     rename; the EVENTS inside must be identical apart from nothing — the title strings are
     not in the timeline; confirm events identical, filenames changed).
   - No other scene, no route, no template content changes (the base.html footer text is not
     timeline-tracked).

CONSTRAINTS
- This prompt does NOT render. PROMPT 028 does.
- Use git mv for tracked files (preserve history). Grep before/after every rename.
- Python 3.11 union typing (str | int), not Optional.

VERIFICATION (all must pass)
1. git status: renames staged as renames (R) for the .py and the media dir.
2. grep "Adjecency" -> zero hits in Animations/ and tools/ (docs/audit historical mentions OK);
   grep "SortingAlgoritms" -> zero hits in live code/tools; grep "Prims's" -> zero hits.
3. python -m tools.syncmap check -> drift ONLY for the 8 renamed scenes due to renames, and
   their event lists are identical to before (prove by diffing an old vs new timeline file's
   "events" arrays — include one diff in the report).
4. All modules import clean; pytest -q green; link checker exit 0.

REPORT
- Rename table with grep counts; the events-identical diff proof; changed timeline file list;
  the note that PROMPT 028 must render the 8 renamed adjacency scenes.
- Tick TASKBOARD row R6.
`````

### PROMPT 025 — Flask cleanups + kebab-case route aliases

Plan card(s): R7 (`docs/Plan/04-Refactor.md`) · Agent: dsa-refactorer · Depends on: 021 · Tick TASKBOARD rows: R7

`````text
PROMPT 025 — REFACTOR #5: FLASK LEGACY API + KEBAB-CASE ROUTE ALIASES (LEGACY ROUTES SURVIVE)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. Oracle rules apply but this prompt
touches no scenes, so the syncmap check is a formality — run it anyway. THE RULE THAT MATTERS:
NEVER delete an existing route; kebab-case aliases are ADDED alongside the space-URLs by
stacking a second @views.route decorator on the SAME view function (Flask allows multiple
route decorators per function; both URLs keep working — no redirects needed, zero broken
bookmarks). Inventory: docs/Audit/02 section 4.

TASK
1. Website/website/__init__.py:~32: the user_loader uses the legacy
   User.query.get(int(user_id)) API (deprecation warning under Flask-SQLAlchemy 3.1) —
   replace with db.session.get(User, int(user_id)).
2. Add kebab-case aliases in Website/website/views.py by stacking a SECOND decorator on each
   existing view function. Keep the original decorator untouched. Pairs to add:
     "/data structures"   + "/data-structures"
     "/2D arrays"         + "/2d-arrays"
     "/searching algorithms" + "/searching-algorithms"
     "/linear search"      + "/linear-search"
     "/binary search"     + "/binary-search"
     "/sorting algorithms" + "/sorting-algorithms"
     "/bubble sort"       + "/bubble-sort"
     "/insertion sort"    + "/insertion-sort"
     "/selection sort"    + "/selection-sort"
     "/quick sort"        + "/quick-sort"
     "/merge sort"        + "/merge-sort"
     "/heap sort"         + "/heap-sort"
     "/stack and queue"   + "/stack-and-queue"
     "/linked list"       + "/linked-list"
     "/singly linked list" + "/singly-linked-list"
     "/doubly linked list" + "/doubly-linked-list"
   ("/", "/dsa", "/algorithms", "/arrays", "/stack", "/queue", and auth routes are already
   fine — do not add anything there.)
3. Template sweep: replace hardcoded hrefs with url_for. Find them by grepping templates for
   href="/ (hardcoded absolute paths) and href="x y" style literals. Every route link becomes
   {{ url_for('views.<function_name>') }} — read views.py function names and match them
   exactly. This makes templates work with BOTH route spellings automatically. Do NOT touch
   the nav-item-pending spans from PROMPT 006.
4. tests/test_routes.py: extend the smoke test to assert BOTH spellings of every aliased route
   return 200 (parameterize the list; keep the original 25 assertions).

CONSTRAINTS
- No route deletions, no redirect responses — both spellings must return 200 directly.
- No template structure changes beyond href values.
- Views' Python logic unchanged.

VERIFICATION (all must pass)
1. pytest -q green — including the doubled route smoke assertions.
2. python tools/link_check.py exit 0 (crawled via test client, so both spellings get exercised).
3. python -m tools.syncmap check -> exit 0 (formality; confirm untouched).
4. Manual: dev server, visit /linked-list AND /linked list, /heap-sort AND /heap sort — all 200,
   same page.

REPORT
- Diff summary (decorators added, url_for replacements count per template), test output.
- Tick TASKBOARD row R7.
`````

### PROMPT 026 — Ruff full pass

Plan card(s): R8 (`docs/Plan/04-Refactor.md`) · Agent: dsa-refactorer · Depends on: 022, 023, 024, 025 · Tick TASKBOARD rows: R8

`````text
PROMPT 026 — REFACTOR #6: RUFF FULL PASS (NO UNSAFE FIXES, NO BEHAVIOR CHANGE)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. pyproject.toml (PROMPT 001) already
configures ruff (line-length 100, py311, exclusions). PROMPTs 021-025 did the structural work;
this pass makes `ruff check` exit 0 across the whole repo so the CI --exit-zero flag can be
removed.

TASK
1. Run: ruff check Animations Website tools mp4_to_gif_converter.py
   Fix EVERY finding. Rules of engagement:
   - Prefer NO autofix for anything touching manim code semantics; read each finding and fix
     by hand. ruff's --fix is allowed ONLY for trivially safe categories (unused imports,
     unused variables) and NEVER with --unsafe-fixes.
   - Line-length violations: wrap expressions; do not rename variables to shorten lines.
   - If a fix would alter behavior or risk an animation's output, add a targeted
     `# noqa: <code>` with a one-line reason instead, and list it in the report.
2. Do NOT run ruff format on the whole repo. You MAY run it ONLY on files already modified in
   this Phase 3 (they were touched by PROMPTs 021-025).
3. After fixing: python -m tools.syncmap check must still be exit 0 for ALL scenes (whitespace
   and import changes cannot affect timelines — prove it).

CONSTRAINTS
- The oracle rule still applies: any timeline drift = revert that edit.
- Do not edit docs/ (audit reports reference old code with old line numbers; that is expected).
- Do not touch Understanding/*.ipynb or utils/createHighlightMap.ipynb (excluded in config).

VERIFICATION (all must pass)
1. ruff check Animations Website tools mp4_to_gif_converter.py -> exit 0.
2. python -m tools.syncmap check -> exit 0 (all scenes).
3. pytest -q green; link checker exit 0.
4. Repo-wide behavior spot checks: dev server loads / and one content page; one animation
   module imports and instantiates headless (record one scene via syncmap).

REPORT
- Findings count by rule code, how each class of finding was resolved, the noqa list with
  reasons, files ruff-format touched.
- Tick TASKBOARD row R8. Also: note in the report that .github/workflows/ci.yml can now drop
  --exit-zero (the user or PROMPT 029's auditor confirms).
`````

### PROMPT 027 — OPTIONAL: Huffman single-pass

Plan card(s): R9 (`docs/Plan/04-Refactor.md`) · Agent: dsa-refactorer · Depends on: 021 · OPTIONAL — skip freely · Tick TASKBOARD rows: R9

`````text
PROMPT 027 — OPTIONAL: HUFFMAN SINGLE-PASS RESTRUCTURE (CANCEL THE CARD IF THE TIMELINE MOVES)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first. Animations/Greedy.py runs the
Huffman algorithm TWICE: once to precompute the tree/graph layout (~lines 230-289) and once
more inside the animation to replay the steps (~371-463) — they must be manually kept in sync
(audit item 2.1.8). This card is OPTIONAL and strictly time-boxed: if the unification would
change the animation's timeline in ANY way, CANCEL the card instead.

TASK
1. Read both passes. Design a single-pass structure: compute the merge sequence once, emitting
   "events" the animation consumes (steps like "pop A, pop B, merge -> node C at position P").
2. Attempt the refactor with the hard constraint that the RECORDED TIMELINE for HuffmanEncoding
   stays byte-identical (python -m tools.syncmap check clean for that scene).
3. THE MOMENT it becomes clear the timeline cannot stay identical (e.g. the animation needs
   positions computed per-step that the pre-pass currently feeds it): STOP, revert everything,
   and cancel the card: in docs/Plan/TASKBOARD.md mark R9 with status "cancelled" (or the
   user's preferred marker) and reason "single-pass changes the timeline; deferred to a
   dedicated card with an expected-diff ledger".

VERIFICATION
- EITHER: merged single-pass + oracle clean + pytest green.
- OR: cleanly reverted (git diff shows no Greedy.py changes) + TASKBOARD R9 marked cancelled
  with the reason.
- In both cases: python -m tools.syncmap check exit 0; tick nothing unless merged.

REPORT
- Outcome (merged/cancelled), the design decision that decided it, oracle status.
`````

### PROMPT 028 — Render batch RB2 (8 adjacency scenes)

Plan card(s): RB2 (`docs/Plan/04-Refactor.md`) · Agent: general (load skill: dsa-render) · Depends on: 024 · Tick TASKBOARD rows: RB2

`````text
PROMPT 028 — RENDER BATCH RB2: THE 8 RENAMED ADJACENCY SCENES (TITLES CHANGED ON-SCREEN)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-render" skill and
follow it. PROMPT 024 renamed 8 Graphs scenes and fixed their on-screen titles ("Adjecency" ->
"Adjacency"); their mp4s are stale AND their output filenames change with the class names.
Renders take minutes each — run exactly these 8, nothing else.

TASK
1. From inside Animations/ render at -ql:
   manim Graphs.py AdjacencyMatrixUD -ql
   manim Graphs.py AdjacencyListUD -ql
   manim Graphs.py AdjacencyMatrixD -ql
   manim Graphs.py AdjacencyListD -ql
   manim Graphs.py WeightedAdjacencyMatrixUD -ql
   manim Graphs.py WeightedAdjacencyListUD -ql
   manim Graphs.py WeightedAdjacencyMatrixD -ql
   manim Graphs.py WeightedAdjacencyListD -ql
2. The NEW renders write to Animations/media/videos/Graphs/480p15/ under the new class names.
   The OLD mp4s (Adjecency*.mp4) remain as stale leftovers — do NOT delete them by hand; list
   them in the report and note they should be removed with user approval (they are git-tracked
   media; recommend `git rm` once the user confirms).
3. Spot-check every rendered video: the title text reads "Adjacency ..." (correct spelling)
   and nothing else visibly changed vs the old mp4 (compare side-by-side with the old files).

CONSTRAINTS
- Render ONLY these 8, ONLY -ql.
- No scene code edits in this prompt.
- No media commits without explicit user approval (default: leave on disk, report).

VERIFICATION (all must pass)
1. 8 new mp4s exist under the NEW names; ffprobe confirms valid files.
2. Spot-check table (per video: title fixed? rest unchanged?).

REPORT
- Render times, spot-check table, the stale-old-mp4 list for later cleanup.
- Tick TASKBOARD row RB2.
`````

### PROMPT 029 — Phase 3 gate: oracle must be byte-identical

Plan card(s): G3 (`docs/Plan/04-Refactor.md`) · Agent: dsa-auditor · Depends on: 021, 022, 023, 024, 025, 026, 027, 028 · Tick TASKBOARD rows: G3

`````text
PROMPT 029 — PHASE 3 GATE: PROVE THE REFACTOR CHANGED NOTHING (EXCEPT THE EXPECTED DIFFS)

CONTEXT
You are the independent auditor for D:\Git-Projects\DSA-Animations. Read AGENTS.md first. You
NEVER edit files. PROMPTs 021-028 refactored the animation codebase (shared helpers, dead-code
sweep, renames, lint) with the promise: behavior identical EXCEPT (a) the 8 adjacency scenes'
on-screen titles (PROMPT 024/028) and (b) nothing else. Verify adversarially.

TASK
1. Oracle sweep: run python -m tools.syncmap snapshot --all --batch 10 and compare EVERY
   timeline against the committed baseline (the files as committed after PROMPTs 019+024):
   - For every scene EXCEPT the 8 renamed adjacency scenes: the "events" arrays must be
     byte-identical. For the 8 renamed scenes: events identical, only file/module/class-name
     fields changed.
   - Produce the full comparison table (scene -> identical / expected-rename-diff / DRIFT).
     Any DRIFT = phase failure.
2. Duplication proof: grep proves single definitions — "class ListElement", "class Node",
   "class WeightedLine", "def make_dynamic_bezier_updater", "def playSurroundingNodeAnimation"
   each defined exactly once (in Animations/common.py) and imported elsewhere. Report counts.
3. Dead-code proof: docs/Audit/03 section 2 items still present? (Spot-check 5: insert_into_
   AVLTree, remove_keys_after, reconnect_after_rotation, the BTrees logger side-effects
   (import BTrees from a temp cwd — no log file created), AVL debug prints gone.)
4. Renames & aliases: grep "Adjecency" and "SortingAlgoritms" -> zero hits in live code/tools;
   BOTH route spellings of 5 sampled aliased routes return 200 via test client; base.html
   says "Prim's Algorithm".
5. Full stack: ruff check Animations Website tools mp4_to_gif_converter.py -> exit 0; pytest -q
   green; link checker exit 0.
6. Visual spot-check: watch 3 of the RB2 renders (AdjacencyMatrixUD, WeightedAdjacencyListD,
   one more) — titles fixed, animations otherwise identical to their old Adjecency*.mp4.
7. Confirm .github/workflows/ci.yml still has --exit-zero on ruff; note in the report that it
   can now be REMOVED (PROMPT 026's note) — do not edit it yourself.

REPORT
- The full scene-by-scene oracle table; grep counts; stack results; 3-video spot-check verdict.
- Verdict: PHASE 3 PASSED / BLOCKED + blockers.
- Tick TASKBOARD row G3 (only on PASSED).
`````

## Phase 4 — Website Content (all animations on the site)

> PROMPTs 031-042 are all page-building prompts executed by the `dsa-page-builder` agent. Each
> one follows the `dsa-add-page` + `dsa-highlightmap` skills: annotate the scenes, generate the
> maps, convert the webm, write the pages, wire the nav, run the checklist. The per-prompt text
> below supplies only the TOPIC-SPECIFIC facts (routes, videos, notebook grounding); the recipe
> itself lives in the skills — load them, do not improvise.

### PROMPT 030 — Bulk webm conversion

Plan card(s): C0 (`docs/Plan/05-Website-Content.md`) · Agent: general (load skill: dsa-render) · Depends on: 004, 012, 028 · Tick TASKBOARD rows: C0

`````text
PROMPT 030 — BULK WEBM CONVERSION: EVERY VIDEO THE WEBSITE STILL MISSES

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-render" skill
and follow it. tools/convert_webm.py (PROMPT 004) converts
Animations/media/videos/<Category>/480p15/*.mp4 -> Website/website/static/Videos/<Category>/
<Scene>.webm. The website currently serves only 16 of the needed videos; the topics Trees (14),
Graphs (22), AVLTree (6), BTrees (1 usable), DivideAndConquer (4), Greedy (2), LinkedList
leftovers (NodeExplanation, DoubleNodeExplanation, TraverseLinkedList, ListRotation),
Stack-Queue/Queue, and Arrays (4) have no webms yet.
ASK THE USER FIRST (media-commit rule D7): report the estimated total size (sum the source
mp4 sizes as an upper bound, then measure the real ratio after converting ONE pilot file) and
get explicit approval for adding ~56 webm files (roughly 25-60 MB) to the repo. If the user
declines, STOP after reporting.

TASK
1. Convert ALL 480p15 mp4s that do not yet have a webm in Website/website/static/Videos/:
     python tools/convert_webm.py Arrays --force
     python tools/convert_webm.py AVLTree --force
     python tools/convert_webm.py BTrees --force
     python tools/convert_webm.py DivideAndConquer --force
     python tools/convert_webm.py Graphs --force
     python tools/convert_webm.py Greedy --force
     python tools/convert_webm.py LinkedList --force
     python tools/convert_webm.py SearchingAlgorithms --force
     python tools/convert_webm.py SortingAlgoritms --force     (reads the OLD media dir name if
        it still exists; note the CATEGORY_ALIASES mapping from PROMPT 024 — sorts already have
        webms, so this should mostly skip; run it anyway for consistency)
     python tools/convert_webm.py Stack-Queue --force
     python tools/convert_webm.py Trees --force
   (--force only overwrites stale outputs; report skip counts. Use --dry-run first to preview.)
2. Category-name note: convert_webm writes static/Videos/<Category>/ using the MEDIA category
   spelling (SortingAlgoritms has the typo at the media level; the site's existing folder is
   spelled correctly). If your tooling from PROMPT 004 maps categories via CATEGORY_ALIASES,
   register the needed alias so NEW webms land in the CORRECT existing folder
   (static/Videos/SortingAlgorithms/). Verify where existing sort webms live and match that
   exactly. Same check for any other mismatched folder names — the goal is ONE consistent
   exact-case folder per topic on the static side.
3. Inventory: write a complete list "Scene -> static webm path -> exists? -> size" to your
   report (this becomes the asset registry for PROMPTs 031-042).

CONSTRAINTS
- Convert only 480p15 renders; never 1080p60 variants.
- Do not commit until the user approves the size delta (they approved running this prompt =
   approval to convert; still show the final numbers before saying "ready to commit").
- Exact-case paths; no manual edits inside static/Videos.

VERIFICATION (all must pass)
1. The inventory shows every scene from the 11 categories has a webm (expect ~56 new files;
   the only intentional hole: BTrees/BTree.mp4 is unsourceable — convert BTrees/BTreeScene.mp4
   only).
2. ffprobe three random new webms: valid VP9, no audio track expected.
3. Sizes: report total MB added; every file < 10 MB (flag outliers — one scene at 480p15
   should be a few MB).
4. pytest -q + link checker still green.

REPORT
- The full inventory table, total size, pilot ratio, folder-name decisions.
- Tick TASKBOARD row C0.
`````

### PROMPT 031 — Arrays pages get videos + maps

Plan card(s): C1 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C1

`````text
PROMPT 031 — ARRAYS: GIVE THE EXISTING TEXT-ONLY PAGES THEIR 4 VIDEOS + SYNC MAPS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them end-to-end. Routes /arrays and /2D arrays already
exist (templates Arrays/arrays.html and Arrays/2Darrays.html) but are TEXT-ONLY; their videos
exist as webms since PROMPT 030 (static/Videos/Arrays/). This prompt upgrades both pages in
place — no new routes.

TASK
1. Annotate the 4 scenes in Animations/Arrays.py: MemoryAllocation, Indexing,
   TwoDArraysAsMatrix, TwoDArraysMultiplication — subclass SyncedScene, add DISPLAY_CODE
   (the ~8-15-line code the page will show: e.g. a numpy array creation for MemoryAllocation,
   arr[i] indexing for Indexing, a nested-loop matrix print for TwoDArraysAsMatrix, the i,j,k
   triple loop for TwoDArraysMultiplication), and code_step(...) calls before each play()
   that demonstrates those lines. Read each construct() first and mirror its steps.
   ORACLE RULE: the annotation must not change any timeline — after editing, run
   python -m tools.syncmap snapshot --scene Animations.Arrays <Scene> for all 4 and diff
   against the committed baselines (events identical).
2. Emit maps:
     python -m tools.syncmap map Animations.Arrays MemoryAllocation --slug memory-allocation --category Arrays
     python -m tools.syncmap map Animations.Arrays Indexing --slug array-indexing --category Arrays
     python -m tools.syncmap map Animations.Arrays TwoDArraysAsMatrix --slug 2d-arrays-as-matrix --category Arrays
     python -m tools.syncmap map Animations.Arrays TwoDArraysMultiplication --slug 2d-arrays-multiplication --category Arrays
3. Upgrade arrays.html: add a video+code section for MemoryAllocation and one for Indexing
   (follow the skill's section pattern: intro sentence, <video> + Prism code block wired via
   data-sync, worked example, complexity notes). Content grounding: read
   Animations/Arrays.py to describe EXACTLY what the videos show (memory addresses demo,
   O(1) indexing). Complexity claims: array indexing O(1), traversal O(n) — trivial but state
   them correctly (the page previously had a lost-index bug fixed in PROMPT 007 — keep it that
   way).
4. Upgrade 2Darrays.html: add sections for TwoDArraysAsMatrix and TwoDArraysMultiplication
   (row-major explanation, the triple-loop product; complexity O(m*n) / O(m*n*p) — verify
   against standard references; MathJax fine).
5. No new routes. Sidebar stays as-is (Arrays links already live). Cross-link the two pages
   via url_for where the skill's template pattern calls for next-topic links.

CONSTRAINTS
- The skill's checklist must pass for BOTH pages.
- No invented content, no AI meta-text, complexity only from standard references.
- Syncmap check must stay clean (timelines untouched by annotations).

VERIFICATION (all must pass)
1. Skill checklist for both pages (route 200, videos 200 exact-case, sync JSON loads,
   highlighting tracks the video — watch each fully once).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0.

REPORT
- Sections/pages changed, maps emitted, checklist results, sync-watch observations.
- Tick TASKBOARD row C1.
`````

### PROMPT 032 — LinkedList completion + Queue page

Plan card(s): C2, C3 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C2, C3

`````text
PROMPT 032 — LINKEDLIST LEFTOVERS (NODE/TRAVERSE/ROTATION) + QUEUE PAGE VIDEO

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. Existing pages: singly_linked_list.html (already a
4-video anchored page: create/length/insert/delete), doubly_linked_list.html (1 video),
queue.html (TEXT-ONLY — its Queue video is now converted). TWO webms already sat unused in
static/Videos/LinkedList/ (NodeExplanation.webm, DoubleNodeExplanation.webm) — PROMPT 030 added
the rest (TraverseLinkedList, ListRotation, Queue). New route needed: /rotation for ListRotation
(kebab-case; the old sidebar /rotation placeholder from content.html:56 was converted to a
pending span in PROMPT 006 — reactivate it).

TASK
1. Annotate + emit maps (oracle rule from PROMPT 031 applies — timelines must stay identical):
   - Animations/LinkedList.py NodeExplanation -> slug node-explanation (category LinkedList)
   - TraverseLinkedList -> slug traverse-linked-list
   - ListRotation -> slug list-rotation
   - DoubleNodeExplanation -> slug double-node-explanation
   - Animations/Stack-Queue.py Queue -> slug queue (category StackAndQueue — check where
     PROMPT 030 actually wrote it: static/Videos/Stack-Queue/ or StackAndQueue; use the
     EXISTING folder that holds Stack.webm for consistency and report which you chose).
   DISPLAY_CODE for each: the plain-Python node/queue snippet the page displays (e.g.
   class Node with data/next; enqueue/dequeue via collections.deque or list — read the scenes
   first and mirror what they actually demonstrate).
2. singly_linked_list.html: add a "What is a node?" section at the TOP anchored #node using
   NodeExplanation, and a #traverse section after #length using TraverseLinkedList (extend
   the existing multi-video mapVar registry pattern — lines ~532-660 — with the new slugs;
   fetch-based data-sync pages coexist, follow whichever pattern the page uses and say which).
3. doubly_linked_list.html: add the DoubleNodeExplanation video+code section.
4. NEW PAGE /rotation: create views.py route + template following the skill: what list
   rotation is (rotate the head pointer), the ListRotation video + code, a worked example
   (k=2 on a 5-node list — read the scene for the actual demo), complexity O(k) / O(n),
   pitfalls (k > n), takeaways. Reactivate the sidebar /rotation entry: find the
   nav-item-pending span with data-target="/rotation" (content.html ~line 56) and convert it
   back into an <a href="{{ url_for(...) }}">.
5. queue.html: add the Queue video+code section (enqueue/dequeue animations, FIFO, overflow
   underflow depictions if the scene shows them — read it), worked example, O(1) amortized
   discussion, circular-queue takeaway.

CONSTRAINTS
- Skill checklist per page; content grounded in the scene sources; no new complexity claims
  you cannot verify.
- /rotation is the ONLY new route; kebab-case; no legacy alias needed (the old link never
  worked).
- Oracle: syncmap check exit 0 after annotations.

VERIFICATION (all must pass)
1. Skill checklists pass for: singly (2 new sections), doubly (1), /rotation (new page),
   queue (1 section).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0 (the reactivated sidebar link resolves).

REPORT
- Pages/routes/maps table, checklist results, which static folder spelling you used for
  Queue.webm and why.
- Tick TASKBOARD rows C2, C3.
`````

### PROMPT 033 — Trees I: types, traversals, correlation, union-find

Plan card(s): C4 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C4

`````text
PROMPT 033 — TREES PART 1: FOUR NEW PAGES (TYPES, TRAVERSALS, LIST-CORRELATION, UNION-FIND)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. The sidebar (content.html ~60-99) has pending spans
with data-target="/types_of_trees", "/traversal", "/breadth_first_search", "/depth_first_search",
"/list_tree_correlation" — this prompt creates the real pages under KEBAB-CASE routes and
REACTIVATES those entries (rename them from spans back to links pointing at the new routes;
the underscore spellings in data-target are historical — map each to the new kebab route).
Also /union-find needs a NEW sidebar entry (it was never listed). Ground truth for content:
Understanding/Trees/Trees.ipynb (BinaryTree, traversals, UnionFind with path compression +
union by rank). Videos (webms exist since PROMPT 030): TreeExplanation, TreeBFS, TreeDFS,
InOrderTraversal, PreOrderTraversal, PostOrderTraversal, TreeListCorrelation, UnionFind — all
in Animations/Trees.py.

TASK
1. Annotate the 8 scenes + emit maps (oracle rule: timelines identical):
   TreeExplanation -> slug tree-explanation; TreeBFS -> tree-bfs; TreeDFS -> tree-dfs;
   InOrderTraversal -> in-order-traversal; PreOrderTraversal -> pre-order-traversal;
   PostOrderTraversal -> post-order-traversal; TreeListCorrelation -> tree-list-correlation;
   UnionFind -> union-find. Category: Trees.
2. NEW ROUTE + PAGE /types-of-trees (template Trees/types_of_trees.html):
   - What a tree is (root, parent/child, leaf, depth/height), the taxonomy the video shows
     (read the scene for which types it demonstrates: binary/ternary etc.),
     the TreeExplanation video + code (a small Node class + tree build snippet).
   - Include BinarySearchTreeInsertion/Deletion? NO — those belong to PROMPT 034's
     /binary-search-tree. Keep this page about generic trees.
3. NEW ROUTE + PAGE /tree-traversals (template Trees/tree_traversals.html) — a MULTI-VIDEO
   page with five anchored sections (#bfs #dfs #inorder #preorder #postorder), one video+code
   each (following singly_linked_list.html's multi-video pattern). Content: BFS=level order
   via queue, DFS family via recursion/stack; in/pre/post order results for the SAME demo
   tree the scenes use (read Trees.py to extract the tree — publish the actual traversal
   output lists for that tree in the worked example); complexities O(n) each with O(h) stack
   space discussion.
4. NEW ROUTE + PAGE /tree-list-correlation (template Trees/tree_list_correlation.html):
   how lists represent trees (parent-array/left-child-right-sibling as the scene shows —
   read TreeListCorrelation), worked example with the scene's data, trade-offs vs node-based.
5. NEW ROUTE + PAGE /union-find (template Trees/union_find.html):
   - Content MUST match the notebook's implementation: find with PATH COMPRESSION, union by
     RANK — complexity O(alpha(n)) amortized (state it as near-constant; cite inverse
     Ackermann), the video's demo merges.
   - The scene animates find/union without rank (audit note) — if the video shows plain
     union, describe the video faithfully AND note the optimized variant from the notebook.
6. Sidebar: reactivate the 5 pending entries (types_of_trees/traversal/breadth_first_search/
   depth_first_search/list_tree_correlation -> the new routes; traversal entries point at
   /tree-traversals#bfs and #dfs) and add a new Union-Find entry under the Trees section.
   Footer: if any footer placeholder matches these topics, leave hidden for now (PROMPT 043
   wires the footer wholesale).

CONSTRAINTS
- Skill checklist per page (4 pages); routes kebab-case; content grounded in scene sources +
  the notebook; no invented complexity claims.

VERIFICATION (all must pass)
1. 4 new routes 200; 8 maps emitted; videos 200 exact-case; highlighting tracks (watch
   TreeBFS + UnionFind fully, spot-watch the rest).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0 (reactivated sidebar links resolve).

REPORT
- Routes/pages/maps table; the demo-tree traversal outputs you published; checklist results.
- Tick TASKBOARD row C4.
`````

### PROMPT 034 — Trees II: BST, ternary, heaps

Plan card(s): C5 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C5

`````text
PROMPT 034 — TREES PART 2: BINARY SEARCH TREE, TERNARY TREE, HEAPS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. Pending sidebar spans to reactivate (content.html):
data-target="/binary_search_tree", "/ternary_tree", "/types_of_heaps" (also
"/properties_of_trees" and "/properties_of_heap" exist as pending — this prompt creates
CONTENT for properties inside the relevant pages rather than separate pages; convert those
two spans into links pointing at /types-of-trees#properties and /types-of-heaps#properties
respectively, with the anchor sections actually existing). Ground truth:
Understanding/Trees/Trees.ipynb (BST insert/search/delete, MinHeap/MaxHeap sift-up/down).
Scenes (Animations/Trees.py): BinarySearchTreeInsertion, BinarySearchTreeDeletion,
TernaryTreeExplanation, MaxHeap, MinHeap.

TASK
1. Annotate + emit maps (oracle rule): BinarySearchTreeInsertion -> slug bst-insertion;
   BinarySearchTreeDeletion -> slug bst-deletion; TernaryTreeExplanation -> ternary-tree;
   MaxHeap -> max-heap; MinHeap -> min-heap. Category Trees.
2. NEW ROUTE + PAGE /binary-search-tree (template Trees/binary_search_tree.html):
   - Multi-video page: #insertion (BST insertion video+code) and #deletion (deletion
     video+code) anchored sections.
   - The deletion section MUST describe all 4 cases and mirror the scene's exact approach
     (read Trees.py BinarySearchTreeDeletion: the two-children case replaces with the
     in-order successor — confirm from source and write that faithfully).
   - Worked example: the insertion sequence the scene animates (read the source; list each
     comparison); properties (in-order gives sorted order); complexity O(h), O(n) worst,
     O(log n) balanced; deletion cases table.
3. NEW ROUTE + PAGE /ternary-tree (template Trees/ternary_tree.html): what a ternary tree is
   (max 3 children), the video, worked example from the scene, contrast with binary trees.
   Keep it short and honest — the video is an explanation of the concept.
4. NEW ROUTE + PAGE /types-of-heaps (template Trees/types_of_heaps.html):
   - Multi-video: #max-heap and #min-heap sections with their videos + code.
   - Content: complete-tree property, heap property, array representation (i -> 2i+1/2i+2),
     sift-up on insert O(log n) — ground the sift description in the scene code AND the
     notebook's MinHeap/MaxHeap; worked example = the insertion the MaxHeap scene animates
     (read source for the values inserted).
   - NOTE for future accuracy: the notebook's delete has the single-node edge case fixed
     (PROMPT 011) — pages describe insert here; deletion is a natural future section — do
     NOT invent one.
5. Sidebar: reactivate the 5 spans listed in CONTEXT (binary_search_tree -> /binary-search-tree,
   ternary_tree -> /ternary-tree, types_of_heaps -> /types-of-heaps, properties_of_trees ->
   /types-of-trees#properties, properties_of_heap -> /types-of-heaps#properties). Add the
   #properties anchors in /types-of-trees (a short properties list — root/edges/depth/height
   facts you already wrote there; just add the anchor) and /types-of-heaps.

CONSTRAINTS
- Skill checklists; kebab routes; no unverified claims; deletion-case description must match
  the scene source exactly.

VERIFICATION (all must pass)
1. 3 new routes 200; 5 maps emitted; anchors exist where pointed; highlighting verified
   (watch BST insertion + MaxHeap fully).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0.

REPORT
- Routes/pages/maps table; the insertion demo values you documented; deletion-case notes;
  checklist results.
- Tick TASKBOARD row C5.
`````

### PROMPT 035 — AVL tree page (6 videos)

Plan card(s): C6 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C6

`````text
PROMPT 035 — AVL TREES: ONE HUB PAGE WITH SIX ANCHORED VIDEO SECTIONS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. Pending sidebar span to reactivate:
data-target="/avl_tree" (content.html) -> new route /avl-tree. Ground truth:
Understanding/Trees/AVLTrees.ipynb — the audit verified it as textbook-perfect (balance
factors, LL/LR/RL/RR rotations, insert + delete rebalancing). Scenes (Animations/AVLTree.py):
AVLTreeInsertion, AVLTreeDeletion, LeftLeftCase, LeftRightCase, RightLeftCase, RightRightCase
(the LeftLeftCase label reads "Right Rotation" since PROMPTs 008/012 — describe cases by
ROTATION DIRECTION matching the videos).

TASK
1. Annotate + emit maps (oracle rule — timelines must not change):
   AVLTreeInsertion -> slug avl-insertion; AVLTreeDeletion -> avl-deletion;
   LeftLeftCase -> avl-left-left-case; LeftRightCase -> avl-left-right-case;
   RightLeftCase -> avl-right-left-case; RightRightCase -> avl-right-right-case.
   Category: AVLTree (check the static/Videos folder name from PROMPT 030 and use exactly it).
2. NEW ROUTE + PAGE /avl-tree (template AVLTree/avl_tree.html), multi-video with six anchored
   sections: #insertion #deletion #ll #lr #rl #rr.
   - Intro: why balance matters (BST worst case degenerates to O(n); AVL keeps O(log n)),
     balance factor definition (height(left) - height(right)), |bf| <= 1 invariant.
   - Rotation sections: for EACH of the 4 cases, explain the imbalance shape (which grandchild
     side caused it) and which rotation(s) fix it — LL => single RIGHT rotation, RR => single
     LEFT rotation, LR => left-then-right, RL => right-then-left — matching what each video
     shows (read each scene's construct() and docstring; LeftLeftCase's on-screen label says
     "Right Rotation" — consistent).
   - Insertion section: worked example from the scene's demo values (read the source);
     deletion section: rebalance-on-the-way-up description matching the scene.
   - Complexity table: find/insert/delete O(log n) worst case; rotations O(1); height
     <= 1.44 * log2(n) (state the standard bound; cite AVL standard references).
3. Sidebar: reactivate the /avl_tree span -> /avl-tree under the Trees section.

CONSTRAINTS
- The skill checklist; kebab route; every rotation description must match BOTH the notebook
  and the video. If the video and notebook would ever disagree, follow the NOTEBOOK for text
  and flag the video mismatch in your report.

VERIFICATION (all must pass)
1. /avl-tree 200; 6 maps emitted; all six videos 200; highlighting tracks (watch
   LeftLeftCase + AVLTreeInsertion fully, spot the rest).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0.

REPORT
- Routes/maps table; rotation-case writeup summary; checklist results.
- Tick TASKBOARD row C6.
`````

### PROMPT 036 — B-Tree page

Plan card(s): C7 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C7

`````text
PROMPT 036 — B-TREES: PAGE FOR THE BTreeScene VIDEO (LOST BTree.mp4 HANDLED HONESTLY)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. FACTS: Animations/BTrees.py contains ONE renderable
scene, BTreeScene (PROMPT 030 converted its mp4). A second video, BTree.mp4, is tracked in
media but its source class is GONE (BTree is now just a VGroup — audit docs/Audit/03 section 5)
so it can NEVER be re-rendered; the site must not pretend otherwise. There is NO B-Tree sidebar
span (the Trees section never listed one) — ADD a new sidebar entry "B-Trees" under Trees
pointing at the new route. BTrees.py is a correct CLRS B-Tree implementation (split_child,
insert_non_full, delayed root split) — read it as content grounding.

TASK
1. Annotate + emit map: BTreeScene -> slug b-tree (category BTrees — exact static folder from
   PROMPT 030). DISPLAY_CODE: the core insertion pseudocode the page displays (search the
   tree's insert/split functions — write a condensed, correct Python version reflecting what
   the scene actually steps through; read the scene to see which operations it animates).
   Oracle rule applies.
2. NEW ROUTE + PAGE /b-tree (template Trees/b_tree.html):
   - Intro: why B-Trees (disk-oriented, high branching factor, used by databases/filesystems),
     node structure (n keys, n+1 children, min degree t), properties (all leaves same depth,
     keys sorted within node, t-1 <= keys <= 2t-1).
   - Video+code section for BTreeScene.
   - Worked example: the insert sequence the scene animates (read the source: values inserted,
     when the root splits, when children split — list the actual split events).
   - Complexity: search/insert/delete O(t * log_t n) (standard CLRS bound — t as branching,
     log_t n levels); O(n) space. State them as standard results.
   - HONEST NOTE (plain text, not a fake section): "A standalone B-Tree explanation video is
     coming soon" — do NOT embed or reference the orphaned media BTree.mp4 in any way.
3. Sidebar: add the "B-Trees" entry under the Trees section.

CONSTRAINTS
- The skill checklist; kebab route; content grounded in BTrees.py + CLRS-standard properties.
- No speculation about the lost video's contents.

VERIFICATION (all must pass)
1. /b-tree 200; map emitted; video 200; highlighting verified (watch once).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0.

REPORT
- Route/map table; the worked-example split events you documented; checklist results.
- Tick TASKBOARD row C7.
`````

### PROMPT 037 — Graphs I: types + representations (12 videos)

Plan card(s): C8 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C8

`````text
PROMPT 037 — GRAPHS PART 1: TYPES-OF-GRAPHS + GRAPH-REPRESENTATION (12 VIDEOS)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. Pending sidebar spans to reactivate (content.html):
data-target="/types_of_graphs" -> /types-of-graphs; "/graph_representation" ->
/graph-representation. Ground truth: Understanding/Graphs/Graphs.ipynb (adjacency
matrix + list implementations, weighted variants). Scenes (Animations/Graphs.py, post-rename
titles read "Adjacency" since PROMPT 028): UndirectedGraphs, DirectedGraphs, WeightedUDGraphs,
WeightedDGraphs, AdjacencyMatrixUD, AdjacencyListUD, AdjacencyMatrixD, AdjacencyListD,
WeightedAdjacencyMatrixUD, WeightedAdjacencyListUD, WeightedAdjacencyMatrixD,
WeightedAdjacencyListD. Note the weighted adjacency-LIST videos display (v, w) TUPLES
(fixed in PROMPTs 009/012) — describe entries as ordered pairs in the text.

TASK
1. Annotate + emit 12 maps (oracle rule; category Graphs — exact static folder from
   PROMPT 030): slugs undirected-graphs, directed-graphs, weighted-ud-graphs,
   weighted-d-graphs, adjacency-matrix-ud, adjacency-list-ud, adjacency-matrix-d,
   adjacency-list-d, weighted-adjacency-matrix-ud, weighted-adjacency-list-ud,
   weighted-adjacency-matrix-d, weighted-adjacency-list-d.
2. NEW ROUTE + PAGE /types-of-graphs (template Graphs/types_of_graphs.html) — multi-video,
   4 anchored sections (#undirected #directed #weighted-undirected #weighted-directed):
   - Definitions: undirected vs directed edges, weighted edges, degree vs in/out-degree,
     the demo graphs the scenes use (read the sources for node/edge counts).
   - Each section: video + code (DISPLAY_CODE = the adjacency structure snippet the page
     shows, e.g. a small edge list or matrix construction matching the video).
3. NEW ROUTE + PAGE /graph-representation (template Graphs/graph_representation.html) —
   multi-video, 8 anchored sections grouped in two bands:
   - Band "Unweighted": #matrix-ud #list-ud #matrix-d #list-d
   - Band "Weighted": #w-matrix-ud #w-list-ud #w-matrix-d #w-list-d
   - Content: matrix (VxV grid, O(1) edge lookup, O(V^2) space) vs list (O(V+E) space,
     O(deg) lookup); weighted list entries are (neighbor, weight) pairs; the trade-off
     discussion grounded in the notebook's implementations; small worked example using the
     scenes' demo graphs (read 2 sources for the actual values).
   - Complexity comparison table (has_edge / list neighbors / space for matrix vs list).
4. Sidebar: reactivate the two spans under the Graphs section.

CONSTRAINTS
- Skill checklists for both pages; kebab routes; every claim matches the notebook.
- 12 annotations in one prompt is heavy: if any scene's construct() proves too entangled to
  annotate faithfully, do NOT force it — skip that video's code-sync (video-only section) and
  note it in the report (maps are required for the page's core sections; a video-only section
  is an acceptable fallback for at most 2 scenes, and the section must say why no code block
  is shown: "the animation is purely visual").

VERIFICATION (all must pass)
1. 2 new routes 200; maps emitted (all 12 or the documented exceptions); videos 200;
   highlighting verified (watch AdjacencyMatrixUD + WeightedAdjacencyListD fully).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0.

REPORT
- Routes/maps table; fallback exceptions if any; the demo-graph values documented; checklist.
- Tick TASKBOARD row C8.
`````

### PROMPT 038 — Graphs II: traversals (4 videos)

Plan card(s): C9 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C9

`````text
PROMPT 038 — GRAPHS PART 2: GRAPH TRAVERSALS (BFS/DFS, DIRECTED + UNDIRECTED)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. No pending sidebar span exists for graph
traversals — ADD a "Graph Traversals" entry under the Graphs section pointing at the new
route. Ground truth: Understanding/Graphs/Graphs.ipynb (BFS/DFS on matrix and list graphs).
Scenes (Animations/Graphs.py): UndirectedGraphBFS, UndirectedGraphDFS, DirectedGraphBFS,
DirectedGraphDFS.

TASK
1. Annotate + emit maps (oracle rule; category Graphs): slugs undirected-graph-bfs,
   undirected-graph-dfs, directed-graph-bfs, directed-graph-dfs.
   DISPLAY_CODE: standard BFS (visited set + queue) and DFS (visited set + stack or
   recursion) snippets — mirror what each scene actually animates (the scenes use
   queue/stack visuals; read one construct() to match variable names to the video).
2. NEW ROUTE + PAGE /graph-traversals (template Graphs/graph_traversals.html) — multi-video,
   4 anchored sections (#bfs-undirected #dfs-undirected #bfs-directed #dfs-directed):
   - BFS: level order, the queue invariant, "shortest path in unweighted graphs" property.
   - DFS: stack behavior, visit/finish structure, cycle-sensitivity on directed graphs.
   - Worked examples: the actual visit ORDER each scene animates (read the sources for the
     adjacency and start node; publish the visited sequence per video).
   - Complexity: O(V + E) time, O(V) space for both (matches the notebook implementations);
     note BFS gives shortest paths only in unweighted graphs.
3. Sidebar: add the "Graph Traversals" entry under Graphs.

CONSTRAINTS
- Skill checklist; kebab route; visited sequences must come from the scene sources, not
  invented.

VERIFICATION (all must pass)
1. /graph-traversals 200; 4 maps; videos 200; highlighting verified (watch BFS-undirected +
   DFS-directed fully).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0.

REPORT
- Route/maps table; the four published visit orders; checklist results.
- Tick TASKBOARD row C9.
`````

### PROMPT 039 — Graphs III: shortest paths (3 pages)

Plan card(s): C10 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C10

`````text
PROMPT 039 — GRAPHS PART 3: DIJKSTRA, BELLMAN-FORD, FLOYD-WARSHALL (3 PAGES)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. Pending sidebar spans to reactivate:
data-target="/dijkstra_algorithm" -> /dijkstra-algorithm; "/bellman_ford_algorithm" ->
/bellman-ford-algorithm; "/floyd_warshall_algorithm" -> /floyd-warshall-algorithm.
Ground truth: Understanding/Graphs/Graphs.ipynb — Dijkstra (linear min-scan), Bellman-Ford
(V-1 relaxations + negative-cycle detection), Floyd-Warshall (all-pairs DP). Scenes:
Dijkstra, BellmanFord, FloydWarshall in Animations/Graphs.py. IMPORTANT FACTS:
- The FloydWarshall video now includes the vertex-0 intermediate step (fixed in PROMPTs
  009/012); the page describes the complete algorithm.
- The BellmanFord scene does NOT animate the final negative-cycle check (V-th iteration) —
  the page text MUST cover negative-cycle detection as part of the standard algorithm and
  note that the video covers the relaxation phase (honesty rule; audit docs/Audit/05
  section 3 lists the cycle check as future work for the animation).
- Dijkstra: no negative weights allowed — explain why (grounded in the notebook).

TASK
1. Annotate + emit maps (oracle rule; category Graphs): slugs dijkstra, bellman-ford,
   floyd-warshall.
   DISPLAY_CODE: mirror the scene logic — Dijkstra: dist array + visited + min-scan loop
   (scene uses linear scan, NOT a heap — match it); Bellman-Ford: edge-list V-1 relaxation
   loops + a final cycle-check comment; Floyd-Warshall: the k/i/j triple loop with the
   dist[i][k]+dist[k][j] < dist[i][j] relaxation.
2. THREE new routes + pages (templates Graphs/*.html), each single-video:
   - /dijkstra-algorithm: greedy invariant, the demo graph + final dist values (read the
     scene source for the graph and verify the final distances by running the notebook's
     Dijkstra on the same graph — publish verified numbers), O(V^2) for the linear-scan
     variant shown + O((V+E) log V) with a binary heap as the standard optimization,
     no-negative-weights requirement.
   - /bellman-ford-algorithm: edge relaxation, V-1 rounds + why, negative-cycle detection
     (one more pass — if any edge relaxes, a negative cycle exists) — state that the video
     shows the relaxation rounds; O(V*E); the demo graph + verified final distances (same
     verification approach as above).
   - /floyd-warshall-algorithm: DP formulation over intermediate vertices k, the recurrence,
     the demo graph + the final matrix (verify against the notebook on the same input
     graph — publish the verified matrix), O(V^3) time / O(V^2) space; negative-cycle note
     (negative diagonal).
3. Sidebar: reactivate the 3 spans under Graphs.

CONSTRAINTS
- Every number you publish (distances, matrices) must be re-derived via a throwaway script
  that runs the NOTEBOOK's implementation on the SCENE's input — paste that script's output
  into your report as evidence. Do not eyeball.
- Skill checklists; kebab routes.

VERIFICATION (all must pass)
1. 3 routes 200; 3 maps; videos 200; highlighting verified (watch Dijkstra fully, spot the
   other two).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0.

REPORT
- Routes/maps table; the verified numbers (dist arrays + FW matrix) with the script evidence;
  checklist results.
- Tick TASKBOARD row C10.
`````

### PROMPT 040 — Graphs IV: Prim's, Kruskal's, topological sort

Plan card(s): C11 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C11

`````text
PROMPT 040 — GRAPHS PART 4: PRIM'S, KRUSKAL'S, TOPOLOGICAL SORT (3 PAGES)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. Pending sidebar spans: "/prims_algorithm" and
"/kruskal_algorithm" -> reactivate as /prims-algorithm and /kruskal-algorithm. There is NO
sidebar span for topological sort — ADD a "Topological Sort" entry under Graphs.
Ground truth: Understanding/Graphs/Graphs.ipynb — heap-based Prim's, union-by-rank Kruskal's,
Kahn's topological sort. Scenes: PrimsMCST, KruskalMCST, TopologicalSort in
Animations/Graphs.py. FACTS to honor:
- The PrimsMCST scene animates a linear cut-scan (not a heap) — code shown must match the
  video; mention the heap optimization as text.
- The KruskalMCST scene uses label-propagation union-find (not rank) — code matches the
  video; the notebook's rank version goes in the text as the optimized variant.
- The scene's on-screen footer/labels say "Prim's Algorithm" (fixed from "Prims's" in
  PROMPT 024).

TASK
1. Annotate + emit maps (oracle rule; category Graphs): slugs prims-mcst, kruskal-mcst,
   topological-sort.
2. THREE new routes + pages (templates Graphs/*.html), each single-video:
   - /prims-algorithm: cut property intuition, grow-the-tree step sequence the video shows
     (read the source for the demo graph and the edge acceptance order; the audit verified
     total cost 121 for the demo — re-derive it with a throwaway script running the
     notebook's Prim's on the same graph and publish verified numbers), O(V^2) linear variant
     + O(E log V) heap variant.
   - /kruskal-algorithm: sort edges + cycle check via union-find, the scene's merge order,
     MCST cost re-derived and verified the same way, O(E log E).
   - /topological-sort: DAG requirement, Kahn's algorithm (in-degree queue — the scene uses
     a deque; match it), the scene's node order (read source), O(V+E), application to
     scheduling/prerequisites; note that a directed cycle makes topo order impossible.
3. Sidebar: reactivate 2 spans + add the Topological Sort entry under Graphs.

CONSTRAINTS
- Same verified-numbers rule as PROMPT 039 (throwaway script evidence for the MCST cost and
  topo order; delete the script afterwards).
- Skill checklists; kebab routes.

VERIFICATION (all must pass)
1. 3 routes 200; 3 maps; videos 200; highlighting verified (watch KruskalMCST fully, spot the
   others).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0.

REPORT
- Routes/maps table; verified MCST cost + topo order with script evidence; checklist results.
- Tick TASKBOARD row C11.
`````

### PROMPT 041 — Divide & Conquer section (4 pages)

Plan card(s): C12 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C12

`````text
PROMPT 041 — DIVIDE & CONQUER: COUNT INVERSIONS, CLOSEST PAIR, LCS, MEDIAN OF MEDIANS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. There is NO D&C sidebar section at all today —
CREATE a new sidebar section "Divide & Conquer" (between Stack-Queue and Graphs, or wherever
the sidebar layout reads naturally — look at content.html's section structure and match it)
with 4 entries. Ground truth: Animations/DivideAndConquer.py sources (read each construct()
carefully — these scenes have constraints fixed in PROMPT 010: LCS requires equal-length
strings for the TABLE LAYOUT but the ALGORITHM is general — say the page text correctly
describes the general algorithm). Scenes: CountInversions, ClosestPairPoint,
LongestCommonSubsequence, MedianOfMedians. CAUTION: the master-theorem content on the old
DSA/algorithms page was wrong and got fixed in PROMPT 007 — any recurrence/complexity math on
these pages must be re-derived carefully (T(n) = 2T(n/2) + O(n) => Theta(n log n), etc.).

TASK
1. Annotate + emit maps (oracle rule; category DivideAndConquer — exact static folder from
   PROMPT 030): slugs count-inversions, closest-pair, longest-common-subsequence,
   median-of-medians.
   DISPLAY_CODE: match each scene — merge-count inversion snippet; divide + strip-check
   closest-pair (the fixed strip logic from PROMPT 010: all pairs within the window);
   backward-DP LCS with backtracking (the scene uses a backward table — mirror it); the
   groups-of-5 median recursion.
2. FOUR new routes + pages (templates DivideAndConquer/*.html), each single-video:
   - /count-inversions: merge-sort-with-counting explanation, the demo array + the inversion
     count the scene computes (read source; verify the count with a throwaway
     O(n^2) brute-force on the same array — publish both), recurrence + Theta(n log n).
   - /closest-pair: sort by x, divide, conquer, strip argument (why 7-ish candidates matter —
     the scene animates the strip; describe faithfully), recurrence 2T(n/2)+O(n) =>
     Theta(n log n).
   - /longest-common-subsequence: DP table intuition, the demo strings + LCS the scene finds
     (read source; verify with a throwaway script), O(mn) time/space; note the scene
     animates equal-length demo strings but the algorithm is general.
   - /median-of-medians: why it exists (guaranteed O(n) selection, good pivot), groups-of-5,
     the recurrence T(n) = T(n/5) + T(7n/10) + O(n) => O(n) — state as the standard result.
3. Sidebar: new D&C section + 4 entries.

CONSTRAINTS
- Same verified-numbers rule: any count/LCS you publish must be re-derived by script; paste
  evidence in the report; delete scripts afterwards.
- Skill checklists; kebab routes; recurrence math correct (double-check against standard
  references; when unsure, state less).

VERIFICATION (all must pass)
1. 4 routes 200; 4 maps; videos 200; highlighting verified (watch CountInversions fully, spot
   the rest).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0.

REPORT
- Routes/maps table; verified numbers (inversion count, LCS string) with script evidence;
  the new sidebar section structure; checklist results.
- Tick TASKBOARD row C12.
`````

### PROMPT 042 — Greedy section (2 pages)

Plan card(s): C13 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-highlightmap) · Depends on: 030 · Tick TASKBOARD rows: C13

`````text
PROMPT 042 — GREEDY: INTERVAL SCHEDULING + HUFFMAN ENCODING (2 PAGES)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-highlightmap" skills and follow them. There is NO Greedy sidebar section today — CREATE
one with 2 entries. Ground truth: Animations/Greedy.py. Scenes: IntervalScheduling (labels
fixed in PROMPT 011/012 — ruler ticks align with intervals now), HuffmanEncoding.
HONESTY FACTS (audit docs/Audit/05 section 3): the Huffman animation builds the tree but
never displays the actual binary CODES for symbols — the page text may explain how codes are
read off the tree (leaves = symbols, path = code) but must NOT claim the video shows the
codes; add a plain note "the animation focuses on tree construction".

TASK
1. Annotate + emit maps (oracle rule; category Greedy — exact static folder from PROMPT 030):
   slugs interval-scheduling, huffman-encoding.
   DISPLAY_CODE: IntervalScheduling — sort by finish time + accept loop (the scene's greedy
   rule: accept if s >= last_finish); Huffman — the two-smallest merge loop with
   deterministic (freq, symbol) tie-break (mirror the scene).
2. TWO new routes + pages (templates Greedy/*.html), each single-video:
   - /interval-scheduling: the greedy-exchange argument in plain language (why earliest
     finish time is optimal), the scene's demo intervals + which get selected (read source;
     verify with a throwaway script), O(n log n) sort + O(n) scan.
   - /huffman-encoding: prefix codes, the two-queue merge process the video shows (the demo
     frequencies + merge order from the source), how codes come off the final tree (text),
     O(n log n) with a heap; the tree-vs-codes honesty note above.
3. Sidebar: new Greedy section + 2 entries.

CONSTRAINTS
- Verified-numbers rule for the selected intervals and the merge order (script evidence in
  report).
- Skill checklists; kebab routes.

VERIFICATION (all must pass)
1. 2 routes 200; 2 maps; videos 200; highlighting verified (watch HuffmanEncoding fully).
2. python -m tools.syncmap check -> exit 0.
3. pytest -q green; link checker exit 0.

REPORT
- Routes/maps table; verified demo data with script evidence; checklist results.
- Tick TASKBOARD row C13.
`````

### PROMPT 043 — Navigation sweep: un-hide + footer + home

Plan card(s): C14 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-verify) · Depends on: 031, 032, 033, 034, 035, 036, 037, 038, 039, 040, 041, 042 · Tick TASKBOARD rows: C14

`````text
PROMPT 043 — NAVIGATION SWEEP: EVERY PENDING SPAN + DEAD FOOTER LINK BECOMES REAL

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" skill
(the checklist section) and "dsa-verify". PROMPTs 031-042 created every topic page. Now the
navigation must be made whole: PROMPT 006 hid/converted placeholder nav; this prompt re-wires
everything to the real pages. THE ALLOWLIST GOAL: after this prompt, the link checker is
green with an EMPTY allowlist and --strict also passes.

TASK
1. Sidebar (Website/website/templates/content.html): find every remaining
   class="nav-item-pending" span. Each has data-target="/original_url". Convert each into a
   real link to the PROMPT 031-042 page that covers it (the mapping is deterministic — e.g.
   "/types_of_trees" -> url_for the /types-of-trees view, "/breadth_first_search" ->
   /tree-traversals#bfs, "/dijkstra_algorithm" -> /dijkstra-algorithm, etc.). List the full
   mapping in your report. Remove the "More topics are being added" note IF no pending spans
   remain (if some do — e.g. Hash Tables — keep the note for those, as non-clickable gray
   spans).
2. Footer (base.html ~118-187): the whole block was hidden in PROMPT 006. Un-hide it and
   wire all ~27 anchors to real url_for targets: every algorithm/structure name -> its page
   (Bubble Sort -> /bubble-sort, Trees entries -> /types-of-trees, Graphs entries ->
   /types-of-graphs, Dijkstra -> /dijkstra-algorithm, etc.); Privacy Policy/Terms ->
   leave as pending spans with a note (pages arrive in PROMPT 049); "Our Team"/"Contact Us"
   -> link Contact Us to the GitHub issues URL from the README (external link, fine), Our
   Team -> remove or convert to "About" pointing at /about IF PROMPT 049 already ran — it
   has NOT, so leave About/Team as pending spans too. List every decision.
3. data_structures.html: the spans added in PROMPT 006 for Trees/Hash Tables/Graphs/
   Union-Find: Trees -> /types-of-trees, Graphs -> /types-of-graphs, Union-Find ->
   /union-find; Hash Tables stays a pending span (no page exists — honest).
4. Home page (home.html): wire the 6 "Explore" buttons (PROMPT 006/B8 left them inert — now
   they exist? Check: the audit found them at lines ~115/158/201/244/287/330) -> give each
   its section page via url_for (Sorting -> /sorting-algorithms, Searching ->
   /searching-algorithms, Linked List -> /linked-list, Stack-Queue -> /stack-and-queue,
   Trees -> /types-of-trees, Graphs -> /types-of-graphs). Update the topic cards' text to
   REAL video counts now that sections exist (count pages per topic and write honest numbers
   like "6 animated algorithms" — no ratings).
5. Allowlist: docs/Plan/baseline-broken-links.txt -> empty it (header comment only).
   python tools/link_check.py and python tools/link_check.py --strict both exit 0.
6. Any remaining pending spans MUST be by design (Hash Tables + the legal pages) — enumerate
   them in the report as the "known future" list.

CONSTRAINTS
- url_for everywhere; no new routes in this prompt; no deletions of nav entries.
- The link checker runs the site through the test client — all internal links must resolve.

VERIFICATION (all must pass)
1. python tools/link_check.py --strict -> exit 0, empty allowlist.
2. pytest -q green.
3. Manual nav pass: dev server; walk the sidebar on 5 pages, the footer on 3, and the home
   cards — every clickable link lands somewhere real; pending items visibly gray and
   non-clickable; no console errors.

REPORT
- The span->link mapping table; footer decisions; home card counts; remaining-future list;
  strict checker output.
- Tick TASKBOARD row C14.
`````

### PROMPT 044 — Phase 4 gate

Plan card(s): G4 (`docs/Plan/05-Website-Content.md`) · Agent: dsa-auditor · Depends on: 043 · Tick TASKBOARD rows: G4

`````text
PROMPT 044 — PHASE 4 GATE: AUDIT THE WHOLE CONTENT BUILD

CONTEXT
You are the independent auditor for D:\Git-Projects\DSA-Animations. Read AGENTS.md first. You
NEVER edit files. PROMPTs 030-043 converted ~56 webms, annotated ~50 scenes, and built all
missing topic pages. This gate adversarially verifies the content build before the polish
phase.

TASK
1. Coverage audit: list every Scene class (from tools/syncmap/timelines/manifest.json) and
   check: does it have a webm in static/Videos/, a map in static/sync/ (where the page has a
   code block), and a page that embeds it? Expected exceptions (acceptable): BTree.mp4
   (lost source — no page embed), scenes intentionally video-only (PROMPT 037 fallbacks),
   legacy scenes whose pages use inline maps (pre-existing pages). Everything else must be
   complete. Produce the full table.
2. Route sweep: ALL routes (old space-spellings + kebab aliases + the ~30 new pages) return
   200 via test client. List the full route count.
3. Link checker --strict -> exit 0 with empty allowlist (verify the file really is empty).
4. Sync integrity: python -m tools.syncmap check -> exit 0; then spot-watch 6 videos across
   topics (one Trees, one Graphs, one AVL, one D&C, one Greedy, one LinkedList) against their
   highlighting — confirm the highlighted line numbers match what the video is doing at those
   moments; report any drift.
5. Content accuracy sampling: pick 4 of the new pages at random (at least one Graphs, one
   Trees) and verify EVERY complexity claim and every published number (demo outputs, MCST
   cost, distances, traversal orders) against Understanding/*.ipynb or by running your own
   throwaway scripts on the same inputs. Report per-claim verdicts.
6. Honesty sweep: grep all templates for "the sources", "given sources", ratings patterns
   ("4.", "k reviews"), "coming soon" (only the intentional Hash Tables/legal pendings from
   PROMPT 043 may match — enumerate them and confirm each is intentional).
7. TASKBOARD hygiene: C0-C14 ticked.

REPORT
- The coverage table summary (complete count / exceptions), route count, checker outputs,
  the 6 sync-watch verdicts, the 4-page accuracy verdicts, honesty sweep results.
- Verdict: PHASE 4 PASSED / BLOCKED + blockers.
- Tick TASKBOARD row G4 (only on PASSED).
`````

## Phase 5 — Website Polish

### PROMPT 045 — Responsive design

Plan card(s): W1 (`docs/Plan/06-Website-Polish.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-verify) · Depends on: 044 · Tick TASKBOARD rows: W1

`````text
PROMPT 045 — RESPONSIVE DESIGN: BREAKPOINTS + TOUCH-FRIENDLY CAROUSEL

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-verify" skill.
Facts: Website/website/static/styles.css (808 lines) has ZERO @media queries; home-page
topic cards are fixed ~310px; the topic carousel drag handler (home.html ~542-571) uses
mouse events only (no touch). The site must work at 390px (phone), 768px (tablet), 1440px
(desktop).

TASK
1. styles.css breakpoints (add at the END of the file, conventional structure):
   - <=768px: sidebar becomes stacked collapsible sections that sit ABOVE content (or a
     hamburger toggle — choose the simpler markup change; details/summary elements are
     already used, so leverage them), topic cards grid becomes 1 column (max-width ~420px
     centered), footer stacks, font sizes slightly reduced for headings only.
   - 769-1024px: cards 2 columns, sidebar narrower.
   - >=1025px: current layout (do not change desktop look).
   - Code blocks: overflow-x auto with visible-but-styled scrollbar; tables wrapped in a
     .table-scroll div (add the wrapper in templates ONLY where tables overflow at 390px —
     test and list which pages needed it).
   - The video+code sections must fit: at 390px the video scales to container width (width:
     100%) with the code block below it (if they sit side-by-side today — inspect the
     content.html layout and make the sensible choice; describe it).
2. Carousel: convert the mouse-event drag (home.html ~542-571) to Pointer Events
   (pointerdown/pointermove/pointerup + setPointerCapture) with touch-action: pan-y on the
   scroll container so vertical page scrolling still works on touch. Keep wheel-scrolling
   and the arrows (if any) working.
3. Test at 390px/768px/1440px (browser devtools device mode): home, one content page, the
   AVL multi-video page, and the 2D-arrays page. No horizontal page scrollbars at any width;
   no overlapping text; every control tappable (min ~44px targets for the hamburger/accordion
   if added).

CONSTRAINTS
- Vanilla CSS + JS only; no frameworks; no new dependencies.
- Desktop (>=1025px) visual parity: take a screenshot-level comparison description in your
  report (what you changed vs what stayed).
- No content/structure changes beyond the table wrappers and any accordion markup the
  responsive design requires.

VERIFICATION (all must pass)
1. Devtools width passes at the 3 widths for the 4 pages (report per page per width).
2. Carousel drags with touch emulation AND mouse AND wheel.
3. pytest -q green; link checker --strict exit 0.

REPORT
- Breakpoint summary, carousel rewrite diff summary, per-page-per-width test table.
- Tick TASKBOARD row W1.
`````

### PROMPT 046 — Dark mode toggle

Plan card(s): W2 (`docs/Plan/06-Website-Polish.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-verify) · Depends on: 044 · Tick TASKBOARD rows: W2

`````text
PROMPT 046 — DARK MODE: WIRE THE EXISTING DARK CSS TO A REAL TOGGLE

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-verify" skill.
Facts: styles.css ~73-79 already contains a complete :root[data-theme="dark"] variable set,
but base.html hardcodes <html lang="en" data-theme="light"> and NO toggle exists. Prism and
MathJax color usage may hardcode some colors (audit item 2.5/4 said fonts/colors are
inconsistent) — you must make dark mode fully readable, not just flip variables.

TASK
1. Toggle in the navbar (base.html, near the auth links): a button with sun/moon SVG
   (inline SVG, no icon library) that calls a small JS function.
2. JS (inline in base.html, vanilla):
   - On load: theme = localStorage.getItem("theme") ?? (prefers-color-scheme: dark ?
     "dark" : "light"); apply to document.documentElement.dataset.theme.
   - On click: toggle, persist to localStorage.
   - Apply BEFORE first paint (tiny inline script in <head> right after <html> attributes
     are readable — place it as early as possible to avoid a flash).
3. Prism dark theme: load the Prism "one-dark" (or coy vs okaidia — pick one) dark theme CSS
   alongside the existing light theme; gate them via media-agnostic CSS like
   [data-theme="dark"] .token rules — simplest robust route: add BOTH theme stylesheets and
   scope: keep light styles as-is; add a small override block scoped to [data-theme="dark"]
   for the code block + copy button. Verify code blocks are READABLE in both themes on at
   least 3 pages (binary search, singly linked list, avl-tree).
4. Hardcoded colors sweep: for the main templates (base/content/home + 2 topic pages),
   identify colors that break dark mode (white backgrounds, black text literals) and route
   them through the CSS variables that the dark theme already swaps. styles.css itself:
   fix any rule the dark palette misses (report which).
5. Videos: confirm the video player looks fine on dark (it will — just verify no white halo
   borders).

CONSTRAINTS
- No frameworks; no new dependencies beyond Prism's existing CDN usage (you may add ONE
  stylesheet link to a Prism dark theme CDN or vendor a small override — prefer the override
  block, fewer moving parts).
- Light mode must remain pixel-identical to today (except the new button).

VERIFICATION (all must pass)
1. Toggle works: click -> dark; reload -> stays dark; click -> light; reload -> stays light;
   first visit honors OS preference (emulate in devtools).
2. Readability pass on 3 pages in dark (code blocks, sidebar, footer, video container,
   MathJax formulas — report each element readable yes/no).
3. Light mode spot-compare with today (screenshot-level description).
4. pytest -q green; link checker --strict exit 0.

REPORT
- The override block, the hardcoded-color fixes list, readability table.
- Tick TASKBOARD row W2.
`````

### PROMPT 047 — Fonts + favicon + meta/OG

Plan card(s): W3, W4 (`docs/Plan/06-Website-Polish.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-verify) · Depends on: 044 · Tick TASKBOARD rows: W3, W4

`````text
PROMPT 047 — FONTS, FAVICON, PAGE TITLES, META DESCRIPTIONS, OG TAGS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-verify" skill.
Facts: styles.css references Roboto / "JetBrains Mono" / Arial but NO webfont is loaded
(silent fallbacks today); there is no favicon; most pages have generic <title> and no meta
description; static/images/logo-icon.png (112 KB) exists but is referenced nowhere.
ASK THE USER at the start: "Self-host woff2 files (no external requests) or link Google
Fonts?" — Default if no answer: system font stack (no download, no CDN) — i.e., replace the
Roboto reference with a robust system stack and keep code font as ui-monospace/"JetBrains
Mono" if available locally, else drop to monospace. Honor whatever the user picks.

TASK
1. Fonts per the user's choice:
   - SELF-HOST: download woff2 subsets (latin) for Roboto (400/700) + JetBrains Mono (400)
     into Website/website/static/fonts/, add @font-face rules at the TOP of styles.css,
     update font-family stacks with proper fallbacks.
   - CDN: add preconnect + one Google Fonts <link> in base.html head.
   - SYSTEM STACK: replace font-family: Roboto with
     system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif and
     "JetBrains Mono" with ui-monospace, "Cascadia Code", Consolas, monospace.
   In all cases: computed styles must show the chosen font actually applied (verify via
   devtools or a computed-style probe).
2. Favicon: copy static/images/logo-icon.png to static/images/favicon.png; add <link
   rel="icon"> (+ apple-touch-icon) in base.html. If the PNG is oversized, generate a
   64x64/32x32 variant with Pillow (installed with manim) into static/images/ — keep the
   original untouched.
3. Titles: base.html defines the <title> block default; every page must have a unique title
   "{Page Topic} - DSA Animations" — sweep ALL templates and add/fix the title block where
   missing (list pages fixed; the algorithms.html title was already fixed in PROMPT 007 —
   verify).
4. Meta: add a meta description to every page (1-2 honest sentences about the page's
   content — write them specifically per topic, no boilerplate), and og:title/og:description/
   og:image (use the logo path) on the home page only.
5. No layout regressions from font swaps: spot-check 3 pages; adjust font-size/line-height
   ONLY if a chosen font clearly breaks a layout (report any such adjustment).

CONSTRAINTS
- No font-based functionality changes; keep CSS variable architecture intact.
- Ask-first rule for the font choice; default to system stack if unanswered.
- Descriptions must be honest (no marketing claims — remember PROMPT 007/B8 rules).

VERIFICATION (all must pass)
1. Computed font check on 3 pages (whichever route chosen).
2. Favicon loads (network tab 200; tab shows icon).
3. Title sweep: every route's rendered <title> is unique and correct (iterate routes via
   the test client and assert titles programmatically — add this as a small check inside
   tests/test_routes.py: title != default and unique per route).
4. pytest -q green; link checker --strict exit 0.

REPORT
- Font decision + implementation; pages-with-new-titles count; per-topic description
  samples; test additions.
- Tick TASKBOARD rows W3, W4.
`````

### PROMPT 048 — Site search

Plan card(s): W5 (`docs/Plan/06-Website-Polish.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-verify) · Depends on: 043 · Tick TASKBOARD rows: W5

`````text
PROMPT 048 — CLIENT-SIDE SITE SEARCH (NAVBAR BOX + DROPDOWN RESULTS)

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-verify" skill.
The site now has ~45 content pages — it needs search. Constraints: NO server-side search,
NO new dependencies; the site is a Flask app with static assets, so a build step generating
a static JSON index is the right shape.

TASK
1. tools/build_search_index.py: a script that builds Website/website/static/search-index.json:
   - Start the app via the test client, iterate every route, GET it, and parse the RENDERED
     HTML with stdlib html.parser to extract: page URL, <title>, all <h1>/<h2>/<h3> texts,
     and the meta description.
   - Output schema: [{"url": "/dijkstra-algorithm", "title": ..., "headings": [...],
     "description": ...}, ...] — deterministic (sort by url), compact separators.
   - CLI flag --check: re-run and diff against the committed index; exit 1 if stale (so CI
     or PROMPT 052 can catch a forgotten rebuild). Add a note in AGENTS.md? NO — you may
     not edit AGENTS.md; instead note it in your report that new pages require re-running
     the build (the --check flag enforces it).
   - Add tests/test_search_index.py: index builds, schema valid, --check clean against the
     committed file, and every index URL resolves to 200 via test client.
2. Navbar search (base.html + a small static JS file Website/website/static/js/search.js —
   you may create the js/ folder; keep JS out of inline template code for this feature):
   - Input box (desktop: visible in navbar; <=768px: under the navbar per PROMPT 045's
     responsive rules) with dropdown results list.
   - On input (debounced ~150ms): filter index client-side (fetch the JSON once, cache it);
     match against title, headings, description (case-insensitive substring; highlight the
     matched fragment in the result row); Enter/click navigates via location.href; keyboard
     up/down/enter navigation; Escape closes; clicking outside closes.
   - Show up to 8 results; "No results for X" row when empty; do not run with <2 chars.
3. Rebuild the index and commit-ready: report the file size (should be tens of KB).

CONSTRAINTS
- Vanilla JS, no frameworks/CDNs; keyboard accessible; the search box must not shift layout
  (fixed width, no reflow of navbar items on focus).
- Deterministic index (two builds -> byte-identical; prove with hashes).

VERIFICATION (all must pass)
1. tests/test_search_index.py green (includes --check determinism proof).
2. Manual: search "avl" finds the AVL page (heading match), "dijkstra" finds its page,
   "sort" finds multiple, "zzzz" shows the no-results row; keyboard nav works; mobile width
   usable.
3. pytest -q green; link checker --strict exit 0 (the JSON URL is static — confirm the
   checker tolerates it).

REPORT
- Index size + sample entries; search.js diff summary; manual test table.
- Tick TASKBOARD row W5.
`````

### PROMPT 049 — Home honesty + legal pages

Plan card(s): W6, W7 (`docs/Plan/06-Website-Polish.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-verify) · Depends on: 044 · Tick TASKBOARD rows: W6, W7

`````text
PROMPT 049 — HOME PAGE FINAL PASS + PRIVACY / TERMS / ABOUT PAGES

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-add-page" and
"dsa-verify" skills. Facts: signup.html (~:31-33) promises "Terms of Service and Privacy
Policy" as plain text with no pages behind them; the footer (wired in PROMPT 043) holds
Privacy/Terms/Team as pending spans; home.html cards got honest copy in PROMPTs 007/043 —
this prompt finishes the job and adds the missing pages. HONESTY RULE: these are legal-ish
pages — plain, truthful, short. No invented company, address, or team bios.

TASK
1. THREE new routes + pages (templates auth/legal/ or legal/ — pick a sensible folder):
   - /privacy: what the app stores (account: username, email, hashed password — read
     Website/website/models.py and write EXACTLY what fields exist), that sessions use a
     cookie, that the site is an educational project, contact via GitHub. Nothing more.
   - /terms: use the site as-is, educational content provided "as is", don't abuse accounts,
     contributions welcome via pull requests (mirrors the README). Nothing more.
   - /about: what the project is (Manim animations + this site), links to the repo, how to
     run it locally (mirror the README's steps), credit line consistent with the LICENSE
     (MIT, check the LICENSE file's copyright holder line and mirror it verbatim).
   All three follow the standard template pattern minus video/code blocks (no videos here).
2. Wire them: signup.html text becomes links (url_for) to /privacy and /terms; the footer
   pending spans (Privacy Policy, Terms of Service; Our Team -> About) become real links.
3. Home final pass:
   - Verify every topic card's text matches reality (video counts from PROMPT 043; read
     them and confirm).
   - The "Feature Topics"/feature cards from PROMPT 007: confirm the "Concept-to-Code
     Connection" description is distinct and honest.
   - Any remaining unverifiable/marketing phrase gets the honest rewording (grep for
     superlatives like "best", "revolutionary", "ultimate" — report hits and fixes).
   - The 6 Explore buttons work (PROMPT 043 wired them — click-test each).
4. Rebuild the search index (PROMPT 048's tool) so the new pages are searchable;
   tests/test_search_index.py --check must pass.

CONSTRAINTS
- No fake contact info, no invented entities, no cookie-law overpromises (do not claim a
  consent banner exists).
- Kebab routes; skill checklist adapted (no video sections for legal pages — state that
  in the report as a checklist deviation, do not invent content to satisfy checkboxes).

VERIFICATION (all must pass)
1. 3 new routes 200; signup links resolve; footer pending spans now real links.
2. Honesty grep clean (report the superlative grep before/after).
3. Search index rebuilt; --check clean; pytest -q green; link checker --strict exit 0.

REPORT
- Pages added; field list you documented from models.py; home-pass diff summary; grep
  results.
- Tick TASKBOARD rows W6, W7.
`````

### PROMPT 050 — Auth polish + performance

Plan card(s): W8, W9 (`docs/Plan/06-Website-Polish.md`) · Agent: dsa-page-builder (skills: dsa-add-page, dsa-verify) · Depends on: 045 · Tick TASKBOARD rows: W8, W9

`````text
PROMPT 050 — AUTH POLISH (SUBSCRIBED DECISION) + PAGE PERFORMANCE PASS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-verify" skill.
Facts: signup.html has a "subscribed" checkbox storing a never-used flag (models.py column
`subscribed`, never read after signup — audit docs/Audit/02 item 29); content has NO
@login_required (a project decision: keep it public — DO NOT add login requirements).
Videos currently load eagerly, which is the heaviest page cost. MathJax + Prism load from CDNs
without defer/async. ASK THE USER at the start: (a) keep the `subscribed` column labeled
honestly ("we don't send emails yet — this just saves a preference"), or (b) remove the
checkbox + column (simplest DB: leave the column in place but remove the checkbox — schema
untouched). Default: (b) remove the checkbox from the form ONLY (column stays; zero schema
risk). Honor the user's answer.

TASK
1. Auth polish per the user's decision:
   - If (b): remove the subscribed checkbox from signup.html (keep the models.py column
     untouched — note it as dormant in your report).
   - If (a): relabel the checkbox + add the honest one-line explanation.
   - Also: style check the auth pages (login/signup) for dark-mode + responsive (PROMPTs
     045/046 landed — verify they render right there too; fix small issues).
2. Performance pass (no functionality change):
   - Videos: add loading="none"-equivalent: since these are <video> tags, set
     preload="metadata" on ALL below-the-fold videos and preload="auto" for the FIRST
     video on multi-video pages (search templates for <video and sweep).
   - MathJax/Prism CDN script tags in base.html: add defer (and async where safe — MathJax
     docs recommend a specific pattern; follow its standard defer pattern; Prism needs
     to run before the sync loader runs — verify the load order still works! The
     content.html sync script must still find Prism; if defer ordering breaks it, keep
     Prism synchronous and only defer MathJax — report what you chose and why).
   - Images: loading="lazy" on non-hero <img> tags (grep templates).
   - Nothing else: no bundlers, no code splitting, no image sprites.
3. Verify no visual/functional regressions: the sync highlighting still runs (Prism order!),
   videos still play on click, dark mode still fine.

CONSTRAINTS
- No @login_required anywhere (decision D3 in docs/Plan/00-Overview.md).
- No schema migration this prompt (either option keeps the DB schema untouched).
- Devtools performance: measure home page + one content page before/after (report the
  numbers: transferred bytes, DOMContentLoaded, Load).

VERIFICATION (all must pass)
1. Signup flow works (register/login/logout) with the checkbox change.
2. Sync-highlighting still works on 2 pages (watch briefly) — proof the Prism/defer change
   is safe.
3. Performance report: numbers before/after; network tab shows videos not downloading full
   data on page load (preload="metadata").
4. pytest -q green; link checker --strict exit 0.

REPORT
- The user's (a)/(b) decision and its implementation; defer/ordering decision; perf table.
- Tick TASKBOARD rows W8, W9.
`````

### PROMPT 051 — OPTIONAL: legacy inline-map migration

Plan card(s): W10 (`docs/Plan/06-Website-Polish.md`) · Agent: general (skills: dsa-highlightmap, dsa-verify) · Depends on: 044 · OPTIONAL — skip freely · Tick TASKBOARD rows: W10

`````text
PROMPT 051 — OPTIONAL: MIGRATE LEGACY PAGES FROM HAND-eyeballed INLINE MAPS TO GENERATED MAPS

CONTEXT
Repo: D:\Git-Projects\DSA-Animations. Read AGENTS.md first, then load the "dsa-highlightmap"
and "dsa-verify" skills. The pre-Phase-4 pages (linear_search, binary_search, the 6 sorts,
stack, doubly_linked_list, and singly_linked_list's 4 maps) still carry hand-eyeballed
inline highlightMap JS arrays. This prompt replaces them with machine-generated maps — pure
consistency win; safe to skip if time is short.

TASK
1. For each legacy page: annotate its scene(s) (SyncedScene + DISPLAY_CODE mirroring the
   code the page ALREADY displays — read the template's current code block; code_step
   placement by watching the video and reading the scene), emit the map JSON, and switch
   the page's video container to data-sync (the loader from PROMPT 017 falls back safely).
2. BEFORE deleting any inline array: python -m tools.syncmap check --legacy and compare
   the generated map against the inline one — report per page whether the eyeballed one was
   wrong (expected: some drift) and by how much (max seconds difference at any step).
3. Special case singly_linked_list.html (4 maps + mapVar registry): migrate to 4 data-sync
   slugs; the multi-video loader pattern stays; test the anchors (#length etc.) still work.
4. Exception rule: if any scene was hand-tuned in the old notebook harness
   (utils/createHighlightMap.ipynb) such that generated times clearly MISsync (you watch
   and see >0.5s constant offset — e.g. the video was edited post-render), DO NOT delete
   that page's inline map; report it as a video/map mismatch needing a re-render decision
   (future card).
5. Oracle rule applies to annotations (timelines byte-identical).

VERIFICATION (all must pass)
1. Every migrated page: watch once — highlighting tracks the video at least as well as
   before (report the watch verdict per page).
2. python -m tools.syncmap check -> exit 0 (and --legacy now reports no hand-tuned drift
   for migrated pages).
3. pytest -q green; link checker --strict exit 0.

REPORT
- Migration table (page -> slug -> inline-vs-generated drift stats), the exceptions left
  inline and why.
- Tick TASKBOARD row W10.
`````

### PROMPT 052 — Final audit + DoD sign-off

Plan card(s): G5 (`docs/Plan/06-Website-Polish.md`) · Agent: dsa-auditor · Depends on: all · Tick TASKBOARD rows: G5

`````text
PROMPT 052 — FINAL GATE: FULL RE-AUDIT OF THE REPOSITORY + PROJECT DoD SIGN-OFF

CONTEXT
You are the independent auditor for D:\Git-Projects\DSA-Animations. Read AGENTS.md first.
You may NEVER edit application code; ONE exception: you ARE allowed to append a
"## Post-fix status (2026-09)" addendum section to each of the five docs/Audit/0X-*.md
reports (and nothing else in them). Everything else is read-only.
This is the closing audit of the whole plan (docs/Plan/00-Overview.md). Compare the repo
TODAY against every finding in docs/Audit/01..05-*.md and against the project's Definition of
Done in docs/Plan/00-Overview.md.

TASK
1. Full verification stack:
   - pytest -q (all tests) and python tools/link_check.py --strict (empty allowlist)
   - Route sweep: every route, both spellings, all 200/302
   - python -m tools.syncmap check -> exit 0; search index --check clean
   - ruff check Animations Website tools mp4_to_gif_converter.py -> exit 0
   - Confirm the CI workflow's ruff --exit-zero can be dropped now (report; do not edit).
2. Re-audit against the five original reports, by section:
   - 04-Bugs: EVERY row re-derived; state FIXED/STILL PRESENT for each.
   - 02-Improvements: which of the 40 items landed (P3 refactor, aliases, fonts, etc.).
   - 03-Dead code: the remaining intentional pendings ONLY (enumerate).
   - 05-Gaps: every gap closed or honestly documented (BTree.mp4, Huffman codes,
     Bellman-Ford cycle-check animation, Hash Tables).
   - 01-Implemented: confirm the crown jewels still work (spot-render check via syncmap on
     3 scenes; watch 2 site videos).
3. Website quality sweep: responsive spot at 3 widths, dark mode toggle, search works,
   titles/meta present, footer/sidebar fully wired, honesty greps (sources/ratings/
   superlatives), no console errors on 5 pages.
4. Git hygiene: git status (nothing untracked that should be tracked; no media committed
   beyond what the user approved in PROMPTs 012/028/030); repo size report; note the Git
   LFS migration as the known follow-up.
5. TASKBOARD: every card ticked or explicitly cancelled with reason (R9, W10 optional).
   Verify the Definition of Done checklist in docs/Plan/00-Overview.md item by item.
6. Write the addenda: append "## Post-fix status (2026-09)" to each of docs/Audit/01..05:
   a short table (finding -> status) per report. Keep it factual, with file:line evidence
   for anything still open.

REPORT
- The DoD checklist with a verdict per item.
- The five addenda (state that you wrote them).
- Overall verdict: PROJECT COMPLETE / REMAINING ITEMS (numbered, each with its
  recommended next prompt or follow-up card).
- Tick TASKBOARD row G5 (only on COMPLETE; otherwise list blockers).
`````


