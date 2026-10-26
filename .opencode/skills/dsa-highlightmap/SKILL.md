---
name: dsa-highlightmap
description: Use when creating or verifying time-synced code highlighting for website pages — generating highlightMap JSON from Manim scenes with tools/syncmap, annotating a scene with SyncedScene/DISPLAY_CODE/code_step, checking map drift, or wiring a page to a sync JSON.
---

# DSA Highlightmap — precise video↔code sync maps

## The problem this solves

Website pages show a video + code block; JS highlights code lines as the video plays. Today the `highlightMap` arrays are hand-eyeballed inline JS in each template — they drift whenever scene timings change. The `tools/syncmap` tool (Plan Phase 2) replaces them with machine-generated maps. Phase-4 pages ship each video with code in **four languages (C, C++, Java, Python)**, each precisely synced via one combined map JSON built from language-agnostic semantic step keys (see PROMPT 030A).

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
| `map <Module> <Scene> --slug tree-bfs --category Trees` | Auto-loads `tools/syncmap/langs/<slug>.json` (the four language definitions — error if missing) and emits the **combined** `Website/website/static/sync/<slug>.json`: `{"video": "Videos/<Category>/<Scene>.webm", "default": "python", "langs": {"python": {"code": [...], "map": [{"time":…, "lines":…}]}, "c": {...}, "cpp": {...}, "java": {...}}}`. Map times are shared (one video timeline); only `lines` differ per language, deduped consecutively per language. `--category` required; `--fps` defaults to 15 |
| `check [--modules a,b] [--legacy]` | Recompute live scenes, compare against committed timelines & maps; exit 1 on drift, 0 with un-snapshotted-scene warnings. For combined maps every language is re-derived and compared — drift messages name the offending language. `--modules` scopes the re-record pass (fast per-module checks); `--legacy` also flags drifting hand-eyeballed inline maps (informational) |

## Annotating a scene (the convention)

`Animations/synced.py` provides:

```python
class SyncedScene(Scene):
    DISPLAY_CODE: ClassVar[list[str]] = []  # Python reference implementation
    def code_step(self, key: str) -> None: ...   # no-op when rendering
```

A web-bound scene:

1. subclasses `SyncedScene`
2. sets `DISPLAY_CODE` — the **Python reference implementation** shown on the page
3. calls `self.code_step("<semantic-key>")` immediately before each `self.play(...)` that demonstrates that algorithm step (keys are short slugs like `"partition-loop"`, `"swap"`, `"recurse"` — language-agnostic, since line numbers differ per language)
4. gets a language library at `tools/syncmap/langs/<slug>.json` (authored by the page agent):
   `{"python": {"code": [...lines...], "steps": {"partition-loop": "4-8", ...}}, "c": {...}, "cpp": {...}, "java": {...}}`
   — `steps` maps each semantic key to a Prism `data-line` string (`"2"`, `"3-5"`, `"1,4"`) **in that language's code**

The recorder runs `construct()` headless via an injected `NullRenderer` (no patching, no ffmpeg, no cairo), accumulating exact run_times and capturing `code_step(key)` events → the maps. Map times are frame-quantized at the render fps (default 15) to match the real webm exactly. No video rendering needed to compute times. The `map` command **validates**: every key the scene emits must exist in all four `steps` maps, and every line ref must be valid — violations fail loudly naming scene, slug, language, and key.

## Wiring a page to a JSON map

The video container gets `data-sync="{{ url_for('static', filename='sync/<slug>.json') }}"`; the loader in `content.html` fetches the combined JSON and renders **language tabs (Python / C / C++ / Java, default Python, choice persisted in `localStorage`)**. Switching tabs swaps the `<code class="language-<x>">` content + class, re-runs Prism, and swaps the active map. When the code block has `data-from-sync` (or its `<code>` is empty), content comes from the JSON's per-language `code`. On fetch failure or with no `data-sync`, the page falls back to its inline `highlightMap` untouched; legacy inline maps keep working. Multi-video pages repeat this per video section (one slug + one tab set each). The page must load Prism grammars for all four languages (`prism-python`, `prism-c`, `prism-cpp`, `prism-java` — same CDN/version as the existing Prism include).

## Rules

- Every `code_step` key must exist in **all four** language `steps` maps (the `map` command enforces this).
- One scene = one map slug; multi-video pages use several slugs.
- Annotating a fresh scene ADDS `code_step` events — re-snapshot and commit the updated timeline; the play/wait event stream and total duration must match baseline (see Pacing below).
- After ANY timing change to a synced scene, run `check` and regenerate the page's map.
- Never hand-edit inline legacy maps to "fix" drift — regenerate or leave them for the optional W10 migration.

## Pacing (making videos breathable)

Fast side-by-side highlighting is hard to follow — pacing edits are **explicitly allowed** on web-bound scenes: add `self.wait(...)` pauses between dense step bursts, or raise individual `run_time`s so each highlighted step stays on screen. Rules: never change WHAT the animation demonstrates (only its timing); document each pacing edit with before/after durations; re-run `snapshot --scene` for every paced scene and commit the updated timeline as expected-drift; regenerate its map(s); re-render at `-ql` and reconvert the webm. Report the total video-duration change per scene.
