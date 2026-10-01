---
name: dsa-highlightmap
description: Use when creating or verifying time-synced code highlighting for website pages — generating highlightMap JSON from Manim scenes with tools/syncmap, annotating a scene with SyncedScene/DISPLAY_CODE/code_step, checking map drift, or wiring a page to a sync JSON.
---

# DSA Highlightmap — precise video↔code sync maps

## The problem this solves

Website pages show a video + code block; JS highlights code lines as the video plays. Today the `highlightMap` arrays are hand-eyeballed inline JS in each template — they drift whenever scene timings change. The `tools/syncmap` tool (Plan Phase 2) replaces them with machine-generated maps.

## Existing machinery

- `Website/website/templates/content.html` (sync JS, ~lines 103-170) — reads the global `highlightMap` OR fetches a `data-sync` JSON, sets `data-line` on the Prism code block, re-highlights; falls back to the inline map when the fetch fails or `data-sync` is absent.
- Map shape: `[{ "time": 1.5, "lines": "3-5" }, …]` — `lines` is a Prism `data-line` string (`"2"`, `"3-5"`, `"1,4"`).
- Multi-video pages use named maps (`createHighlightMap`, …) with a `mapVar` registry — see `singly_linked_list.html:532-660`.

## The tool (after Phase 2)

```
python -m tools.syncmap <command>
```

| Command | Effect |
|---|---|
| `snapshot --scene Animations.Trees TreeBFS` | Write a timeline JSON (event log with cumulative times) → `tools/syncmap/timelines/<Scene>.json` |
| `snapshot --all` | All scenes — used as the refactor oracle; run in batches |
| `map <Module> <Scene> --slug tree-bfs --category Trees` | Emit `Website/website/static/sync/<slug>.json`: `{"video": "Videos/<Category>/<Scene>.webm", "code": [...lines], "map": [{"time":…, "lines":…}]}` — `--category` is required; `--fps` defaults to 15 (the web render standard) |
| `check [--modules a,b] [--legacy]` | Recompute live scenes, compare against committed timelines & maps; exit 1 on drift, 0 with un-snapshotted-scene warnings. `--modules` scopes the re-record pass (fast per-module checks); `--legacy` also flags drifting hand-eyeballed inline maps (informational) |

## Annotating a scene (the convention)

`Animations/synced.py` provides:

```python
class SyncedScene(Scene):
    DISPLAY_CODE: ClassVar[list[str]] = []  # exact code the page displays
    def code_step(self, lines: str, key: str = "") -> None: ...   # no-op when rendering
```

A web-bound scene:

1. subclasses `SyncedScene`
2. sets `DISPLAY_CODE` — the **single source of truth**; the page renders its code block FROM this
3. calls `self.code_step("3-5")` immediately before each `self.play(...)` that demonstrates those lines

The recorder runs `construct()` headless via an injected `NullRenderer` (no patching, no ffmpeg, no cairo), accumulating exact run_times and capturing `code_step` events → the map. Map times are frame-quantized at the render fps (default 15) to match the real webm exactly. No video rendering needed to compute times.

## Wiring a page to a JSON map

The video container gets `data-sync="{{ url_for('static', filename='sync/<slug>.json') }}"`; the loader in `content.html` fetches it, uses its `map`, and — when the code block has `data-from-sync` (or its `<code>` is empty) — fills the code content from the JSON's `code`. On fetch failure or with no `data-sync`, the page falls back to its inline `highlightMap` untouched; legacy inline maps keep working.

## Rules

- `code_step` lines must exist in `DISPLAY_CODE` (validate before emitting).
- One scene = one map slug; multi-video pages use several slugs.
- After ANY timing change to a synced scene, run `check` and regenerate the page's map.
- Never hand-edit inline legacy maps to "fix" drift — regenerate or leave them for the optional W10 migration.
