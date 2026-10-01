# tools/syncmap — machine-precise video↔code sync maps

The website's topic pages show a Manim video next to a Prism-highlighted code block.
Until now the `highlightMap` arrays mapping video timestamps to code lines were
**hand-eyeballed inline JS** in each template — they silently drift whenever a scene's
animation timings change. `tools/syncmap` replaces them with machine-generated maps
derived by running the scene's `construct()` **without rendering**, and doubles as the
**behavior-preservation oracle** for the Phase 3 refactor (timelines must stay
byte-identical when behavior is preserved).

Design contract and time-model details: [`DESIGN.md`](DESIGN.md) (read it before
changing the recorder).

## The annotation convention (`Animations/synced.py`)

```python
class SyncedScene(Scene):
    DISPLAY_CODE: ClassVar[list[str]] = []   # exact code the page displays

    def code_step(self, lines: str, key: str = "") -> None:
        """No-op while rendering. The syncmap recorder captures the current timestamp."""
```

A web-bound scene:

1. subclasses `SyncedScene`
2. sets `DISPLAY_CODE` — the single source of truth; the page renders its code block from it
3. calls `self.code_step("3-5")` immediately before each `self.play(...)` that demonstrates
   those lines (1-based line numbers, Prism `data-line` syntax: `"6"`, `"3-5"`, `"6,9"`)

Importing `Animations/synced.py` has zero side effects; `code_step` is a no-op during
real renders, so annotations never change a scene's timeline.

## CLI

All commands run from the repo root: `python -m tools.syncmap <command>`.

### snapshot — record a scene's timeline (the refactor oracle)

```
python -m tools.syncmap snapshot --scene Animations.SearchingAlgorithms LinearSearch
python -m tools.syncmap snapshot --all --batch 10
```

Runs `construct()` headless (a `NullRenderer` injected through the `Scene(renderer=...)`
seam — no patching, no ffmpeg, no cairo) and writes
`tools/syncmap/timelines/<Scene>.json`:

```json
{"scene": "...", "module": "Animations.SearchingAlgorithms", "manim_version": "0.19.0",
 "source_sha256": "...", "events": [{"t": 0.0, "type": "wait", "run_time": 1.0, "frozen": true}, ...]}
```

`--all` also writes `timelines/manifest.json` (`{scenes, generated, errors}`).
Timeline files are deterministic: `sort_keys`, compact separators, LF, no timestamps —
identical code yields byte-identical files (that is the oracle contract). `source_sha256`
intentionally changes when a scene file is edited; the *events* are the behavior record.
Options: `--scene MODULE SCENE` | `--all`, `--batch N`, `--modules a,b` (scope `--all`),
`--out DIR`.

### map — emit the JSON a page consumes

```
python -m tools.syncmap map Animations.SearchingAlgorithms LinearSearch --slug linear-search --category SearchingAlgorithms
```

Records the scene, frame-quantizes each `code_step`, dedupes consecutive identical lines,
validates every `lines` reference against `DISPLAY_CODE`, and writes
`Website/website/static/sync/<slug>.json`:

```json
{"video": "Videos/SearchingAlgorithms/LinearSearch.webm",
 "code": ["def search(arr, N, x):", "..."],
 "map": [{"time": 1.0667, "lines": "1"}, {"time": 1.4, "lines": "2"}]}
```

Options: `--fps` (default 15 — the web render standard), `--out DIR`.

### check — drift gate

```
python -m tools.syncmap check [--legacy]
```

- **timelines**: every committed timeline is re-recorded and byte-compared; mismatches
  report the first differing event (or "source changed, events identical — regenerate").
- **maps**: every committed `sync/*.json` is re-derived in memory and byte-compared.
- Scenes without a committed timeline are listed as a warning (exit stays 0).
- `--legacy` additionally parses the hand-eyeballed inline template maps and warns when
  one is >1.0 s away from the corresponding live `code_step` time (informational only —
  legacy maps are eyeballed, exact comparison is impossible by design).
- Options: `--timelines DIR` / `--sync DIR` point at non-default committed dirs (the drift
  test uses these for throwaway copies); `--modules a,b` scopes the check to the given
  dotted modules — timelines and maps belonging to other modules are skipped, so a
  post-refactor per-module check runs in seconds instead of re-recording all 72 scenes.

Exit code: **0 = no drift, 1 = drift found.** Run `check` after any timing change to a
synced scene and regenerate with `snapshot`/`map`. Never hand-edit legacy inline maps to
"fix" drift — regenerate them or leave them for the optional W10 migration.

## The time model in five lines

1. Every `play()` call contributes its resolved `run_time` (`max` over its animations;
   `play(..., run_time=r)` overrides; default 1 s).
2. `wait(d)`/`pause()` contribute `d` (default 1 s); `Succession` sums its parts,
   `LaggedStart` staggers starts (`lag_ratio` never inflates an explicit total).
3. The **video** is frame-quantized: frozen static waits contribute `int(d*fps)` frames
   (floor), everything else `np.arange(0, d, 1/fps)` frames (ceil) — raw run_time sums
   drift from the real video, so map times use this quantized clock.
4. The recorder runs at fps 15 (the web `-ql` standard) so sub-frame durations clamp
   exactly like a real render.
5. Full derivation, source citations, and the frame-quantization proof: `DESIGN.md` §4.

## How a page consumes a map

`Website/website/templates/content.html` loader: give the element holding
`<video id="code-video">` a `data-sync="{{ url_for('static', filename='sync/<slug>.json') }}"`
attribute. On `DOMContentLoaded` the loader fetches the JSON, uses its `map` as the
highlight map, and — if the `#code-block` element has `data-from-sync` (or its `<code>`
is empty) — fills the code block with the JSON's `code` before Prism-highlighting. On
fetch failure, or with no `data-sync`, the page falls back to its inline
`highlightMap` untouched; pages with neither simply don't highlight. Multi-video pages
keep using their named-map registry (see `singly_linked_list.html`).
