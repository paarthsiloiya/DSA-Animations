# 01 — Phase 0: Foundation

**Objective:** safety net before touching anything — pinned deps, test/lint scaffolding, link checker, webm converter, CI.
**Preconditions:** none. **Parallelizable:** F1–F5 are independent; F6 after F2–F4.

Cards:

### F1 — Root `requirements.txt` (pinned)
Agent: general · Depends: — · Size: S
**Do:** Create root `requirements.txt` pinning the verified versions: `manim==0.19.0`, `flask==3.0.3`, `flask-sqlalchemy==3.1.1`, `flask-login==0.6.3`, `moviepy>=2.0,<3.0`, `tqdm>=4.64`, plus `ruff` and `pytest` (or a `-dev` extra). Keep `requirements_converter.txt` but fix its moviepy floor (see B16).
**Verify:** `pip install -r requirements.txt` in a fresh venv; `python -c "import manim, flask, moviepy"` OK.
**Done when:** file exists, imports verified.

### F2 — `pyproject.toml` (ruff + pytest config)
Agent: general · Depends: F1 · Size: S
**Do:** Add `pyproject.toml`: `[tool.ruff] line-length = 100`, target-version py311, exclude `media/`, `gifs/`, `.kilo/`, `Understanding/` (notebooks), `utils/createHighlightMap.ipynb`. Add `[tool.pytest.ini_options]` with `testpaths = ["tests"]`.
**Verify:** `ruff check Animations Website tools mp4_to_gif_converter.py` runs (failures listed are the P3 backlog — config only must be valid).
**Done when:** both tools run without config errors.

### F3 — `tools/link_check.py` + broken-link baseline
Agent: general · Skill: dsa-verify · Depends: F2 · Size: M
**Do:** Script that: imports the Flask app via test client, walks `app.url_map`; parses every template (`templates/**/*.html`) for `href="..."` (skip `#anchors`, `http(s)://`, `mailto:`), Jinja `url_for(...)` occurrences, and `data-sync`/`src=` static refs; resolves each against routes + static files (case-sensitive!); exits 1 on unknown links. Known-broken baseline goes to `docs/Plan/baseline-broken-links.txt` (one entry per line, format `template:line -> target`) and the checker allowlists exact matches, reporting "N known-broken (allowlisted), 0 new". Add `tests/test_links.py` wrapping it.
**Verify:** Run it — should list exactly the audit's broken set (18 sidebar/`/rotation`, 8 relative in `data_structures.html`, `algorithms.html:268`, `linked_list.html:124`, 27 footer no-href) and pass with allowlist.
**Done when:** test green; allowlist matches audit `docs/Audit/04-Bugs.md §1`.

### F4 — `tests/test_routes.py` (route smoke)
Agent: general · Depends: F2 · Size: S
**Do:** pytest that creates the app (fixture, temp instance path so no DB pollution), asserts 200 for all 25 current routes (302 acceptable for `/logout`).
**Verify:** `pytest -q` green.
**Done when:** all current routes asserted.

### F5 — `tools/convert_webm.py`
Agent: general · Skill: dsa-render · Depends: — · Size: M
**Do:** Mirror the gif converter's UX: scan `Animations/media/videos/<Category>/480p15/*.mp4`, convert with ffmpeg to `Website/website/static/Videos/<Category>/<Scene>.webm`. First probe an existing webm (`ffprobe` on `static/Videos/SortingAlgorithms/BubbleSort.webm`) and reuse its codec/CRF settings. Support `--category`, `--scene`, `--dry-run`, `--force`; skip existing by default; use `pathlib`.
**Verify:** `--dry-run` lists expected files; convert one scene and confirm it plays in the browser.
**Done when:** dry-run output sane; one real conversion verified.

### F6 — CI workflow (GitHub Actions)
Agent: general · Depends: F2, F3, F4 · Size: S
**Do:** `.github/workflows/ci.yml` on ubuntu: install pinned deps, run `ruff check` (allow existing backlog via `continue-on-error` until P3, or scoped paths), `pytest` (includes link checker — this catches Windows→Linux casing bugs like `videos/` vs `Videos/`). No manim rendering in CI.
**Verify:** Workflow file valid (actionlint or YAML parse); passes locally-equivalent steps.
**Done when:** CI would be green on `main` today (with allowlisted links).

### Phase 0 exit gate

- [ ] Fresh-clone setup works from `requirements.txt`
- [ ] `pytest` runs (routes + links green with baseline allowlist)
- [ ] `tools/convert_webm.py` dry-run clean
- [ ] CI workflow defined
- [ ] TASKBOARD updated; commit
