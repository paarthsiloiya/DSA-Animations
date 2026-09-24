# DSA-Animations — Agent Guide

Manim-based Data Structures & Algorithms animations (72 Scene classes in `Animations/`) plus a Flask web app ("AlgoViz" in `Website/website/`) that serves theory pages with time-synced code highlighting. Python 3.11+, Manim 0.19, Flask 3.x. Windows host — but CI/deploy target is Linux.

## Read this first

- `docs/Audit/01..05-*.md` — full code audit (implemented / improvable / dead code / bugs / gaps). **Consult the relevant report before touching code.**
- `docs/Plan/00-Overview.md` — goals, phase map, decision log.
- `docs/Plan/TASKBOARD.md` — live task cards; update it when work completes.
- `Understanding/*.ipynb` — ground-truth algorithm implementations. Site-content complexity claims must match these.

## Project map

| Path | What it is |
|---|---|
| `Animations/*.py` | Manim scenes, one file per topic; `env_config.py` = shared colors/fonts |
| `Animations/media/` | Rendered videos (git-tracked, ~432 MB) — never edit by hand |
| `Website/website/` | Flask app: `__init__.py` (factory), `views.py` (22 routes), `auth.py` (3 routes), `models.py`, `templates/`, `static/` |
| `gifs/` | Converted GIFs (~986 MB, git-tracked) |
| `Understanding/` | Jupyter notebooks (Trees, AVLTrees, Graphs) — correctness ground truth |
| `utils/` | Dev notes + legacy `createHighlightMap.ipynb` harness |
| `tools/` | Added by the plan: `link_check.py`, `convert_webm.py`, `syncmap/` |
| `docs/Audit/`, `docs/Plan/` | Audit reports & implementation plan |

## Commands

| Task | Command |
|---|---|
| Run website | `cd Website; python main.py` → http://127.0.0.1:5000 |
| Render a scene | `cd Animations; manim <File>.py <Scene> -ql` (`-ql` = 480p15, the web standard; `manim.cfg` default is 720p30) |
| Convert mp4 → webm for site | `python tools/convert_webm.py <Category> --dry-run` (Phase 0+) |
| Run tests | `pytest` (Phase 0+) |
| Link checker | `python tools/link_check.py` (Phase 0+) |
| Sync-map tool | `python -m tools.syncmap snapshot\|map\|check …` (Phase 2+) |

## Conventions

- **Routes:** new routes are kebab-case (`/binary-search-tree`). **Never delete existing routes** — attach legacy aliases by stacking extra `@views.route(...)` decorators on the same view function.
- **Templates:** always `url_for(...)`, never hardcoded paths. Static video dir is exactly `Videos/` (capital V — Linux deploys are case-sensitive; CI runs on Linux).
- **Flask:** `SECRET_KEY` from env `DSA_SECRET_KEY` (dev fallback allowed); DB via `app.instance_path`, never cwd.
- **Manim:** shared visual helpers live in `Animations/common.py` (Phase 3+). Web-bound scenes subclass `SyncedScene` and declare `DISPLAY_CODE` (Phase 2+). No debug prints, no commented-out code.
- **Content accuracy:** every complexity claim must be verifiable against `Understanding/*.ipynb` or a standard reference. No AI meta-text ("the sources say…") in user-visible content.
- **Style:** ruff, line-length 100, config in `pyproject.toml`. Python 3.11 typing (`str | int`).

## Safety rails

- **Do not commit media >1 MB without explicit user approval** — the repo already carries ~1 GiB of videos/gifs. Git LFS migration is a plan item.
- Renders take minutes each: only re-render scenes you changed; batch re-renders per the plan's RB cards.
- Windows host, Linux deploy: use `pathlib`, exact-case static paths, no `\` separators in code.
- Never modify `Animations/media/` or `gifs/` by hand — regenerate only via manim / converter scripts.
- **`docs/Plan/PROMPTS.md` is the user's read-only prompt library — agents must NEVER create, edit, rename, move, or delete it.** If a task seems to require changing it, stop and tell the user.
- Before/after any behavior-preserving refactor, run the timeline snapshot check (Phase 2+) — timelines must be byte-identical unless the task card says the output should change.

## Definition of done (every task)

1. `pytest` green (or N/A with reason)
2. Link checker green
3. Affected scene/page verified (route 200, video 200, sync map loads)
4. `docs/Plan/TASKBOARD.md` updated
5. Concise report of what changed, with verification evidence
