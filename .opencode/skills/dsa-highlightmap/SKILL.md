---
name: dsa-highlightmap
description: Use when creating or verifying time-synced code highlighting for website pages — generating highlightMap JSON from Manim scenes with tools/syncmap, annotating a scene with SyncedScene/DISPLAY_CODE/code_step, checking map drift, or wiring a page to a sync JSON.
---

# DSA Highlightmap — precise video↔code sync maps

## The problem this solves

Website pages show a video + code block; JS highlights code lines as the video plays. Today the `highlightMap` arrays are hand-eyeballed inline JS in each template — they drift whenever scene timings change. The `tools/syncmap` tool (Plan Phase 2) replaces them with machine-generated maps.

## Existing machinery

- `Website/website/templates/content.html:104-137` — sync JS: reads global `highlightMap`, sets `data-line` on the Prism code block, re-highlights.
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
| `map <Module> <Scene> --slug tree-bfs` | Emit `Website/website/static/sync/<slug>.json`: `{"video": "Videos/<Cat>/<Scene>.webm", "code": [...lines], "map": [{"time":…, "lines":…}]}` |
| `check` | Recompute live scenes, compare against committed maps & timelines; non-zero exit on drift |

## Annotating a scene (the convention)

`Animations/synced.py` provides:

```python
class SyncedScene(Scene):
    DISPLAY_CODE: list[str] = []            # exact code the page displays
    def code_step(self, lines: str, key: str = "") -> None: ...   # no-op when rendering
```

A web-bound scene:

1. subclasses `SyncedScene`
2. sets `DISPLAY_CODE` — the **single source of truth**; the page renders its code block FROM this
3. calls `self.code_step("3-5")` immediately before each `self.play(...)` that demonstrates those lines

The recorder patches `play`/`wait` to accumulate exact run_times and captures `code_step` events → the map. No video rendering needed to compute times.

## Wiring a page to a JSON map

The video container gets `data-sync="{{ url_for('static', filename='sync/<slug>.json') }}"`; the loader in `content.html` fetches it and overrides any inline map. Legacy inline maps keep working untouched.

## Rules

- `code_step` lines must exist in `DISPLAY_CODE` (validate before emitting).
- One scene = one map slug; multi-video pages use several slugs.
- After ANY timing change to a synced scene, run `check` and regenerate the page's map.
- Never hand-edit inline legacy maps to "fix" drift — regenerate or leave them for the optional W10 migration.
