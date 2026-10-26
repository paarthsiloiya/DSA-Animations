# tools/syncmap — machine-precise video↔code sync maps (four languages)

The website's topic pages show a Manim video next to a Prism-highlighted code block.
Until now the `highlightMap` arrays mapping video timestamps to code lines were
**hand-eyeballed inline JS** in each template — they silently drift whenever a scene's
animation timings change. `tools/syncmap` replaces them with machine-generated maps
derived by running the scene's `construct()` **without rendering**, and doubles as the
**behavior-preservation oracle** for the Phase 3 refactor (timelines must stay
byte-identical when behavior is preserved).

Since C0M every synced page ships its video with code in **four languages** — Python,
C, C++, Java — all precisely synced to the same webm. Line numbers differ per language,
so scenes annotate **semantic step keys** and a per-slug language library resolves each
key to that language's line numbers.

Design contract and time-model details: [`DESIGN.md`](DESIGN.md) (read it before
changing the recorder).

## The annotation convention (`Animations/synced.py`)

```python
class SyncedScene(Scene):
    DISPLAY_CODE: ClassVar[list[str]] = []   # Python reference implementation the page shows

    def code_step(self, key: str) -> None:
        """No-op while rendering. The syncmap recorder captures the key's timestamp."""
```

A web-bound scene:

1. subclasses `SyncedScene`
2. sets `DISPLAY_CODE` — the Python reference implementation (the page's default tab)
3. calls `self.code_step("partition-loop")` immediately before each `self.play(...)` that
   demonstrates that step — a short, language-agnostic slug (`"init"`, `"partition-loop"`,
   `"swap"`, `"recurse"`), because line numbers differ per language

Importing `Animations/synced.py` has zero side effects; `code_step` is a no-op during
real renders, so annotations never change a scene's timeline.

## The language library — `tools/syncmap/langs/<slug>.json`

One file per map slug; the `map` command auto-loads it. Schema:

```json
{"python": {"code": ["...lines..."], "steps": {"partition-loop": "4-8", "...": "..."}},
 "c":    {"code": ["..."], "steps": {"...": "..."}},
 "cpp":  {"code": ["..."], "steps": {"...": "..."}},
 "java": {"code": ["..."], "steps": {"...": "..."}}}
```

- `code` — the exact code listing that language's tab displays (non-empty, all four
  languages required).
- `steps` — every semantic key the scene emits, mapped to a Prism `data-line` string
  (`"6"`, `"3-5"`, `"6,9-11"`) **in that language's own code**.

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
 "source_sha256": "...", "events": [{"t": 0.0, "type": "wait", "run_time": 1.0, "frozen": true},
 {"t": 1.0, "type": "code_step", "key": "loop"}, ...]}
```

`--all` also writes `timelines/manifest.json` (`{scenes, generated, errors}`).
Timeline files are deterministic: `sort_keys`, compact separators, LF, no timestamps —
identical code yields byte-identical files (that is the oracle contract). `source_sha256`
intentionally changes when a scene file is edited; the *events* are the behavior record.
`code_step` events carry only `{"t", "type", "key"}` — line numbers live in the langs
library, so timelines stay language-agnostic.
Options: `--scene MODULE SCENE` | `--all`, `--batch N`, `--modules a,b` (scope `--all`),
`--out DIR`.

### map — emit the combined JSON a page consumes

```
python -m tools.syncmap map Animations.SearchingAlgorithms LinearSearch --slug linear-search --category SearchingAlgorithms
```

Records the scene, frame-quantizes each `code_step`, auto-loads
`tools/syncmap/langs/<slug>.json`, validates it against the emitted keys, and writes
`Website/website/static/sync/<slug>.json`:

```json
{"video": "Videos/SearchingAlgorithms/LinearSearch.webm",
 "default": "python",
 "langs": {"python": {"code": ["def search(arr, N, x):", "..."],
                       "map": [{"time": 1.0, "lines": "1"}, {"time": 1.4, "lines": "2"}]},
           "c": {...}, "cpp": {...}, "java": {...}}}
```

- **Map times are shared** across languages: one frame-quantized video timeline; only
  `lines` differ per language.
- Consecutive identical `lines` are deduped **per language** (one language may collapse
  a step another language keeps separate), and the end-of-video sentinel is applied
  per language.
- The command **fails loudly** (exit 1, nothing written) when: the langs file is missing
  (the error includes the expected schema), a language section is missing, any emitted
  key is absent from any language's `steps`, any `steps` line ref is out of range for
  that language's `code`, or any `code` list is empty. Errors name the scene, slug,
  language and key.

Options: `--fps` (default 15 — the web render standard), `--out DIR`, `--langs DIR`
(default `tools/syncmap/langs`).

### check — drift gate

```
python -m tools.syncmap check [--legacy]
```

- **timelines**: every committed timeline is re-recorded and byte-compared; mismatches
  report the first differing event (or "source changed, events identical — regenerate").
- **maps**: every committed `sync/*.json` is re-derived **per language** in memory
  (requiring the matching `langs/<slug>.json`) and byte-compared. Drift messages name the
  offending language, e.g.
  `DRIFT map quick-sort: language 'java' differs (14 committed vs 13 live)` — a stale
  single translation is immediately visible.
- Scenes without a committed timeline are listed as a warning (exit stays 0).
- `--legacy` additionally parses the hand-eyeballed inline template maps. With semantic
  keys the events no longer carry line numbers, so inline line-number maps are no longer
  directly comparable — the legacy pass remains informational and reports old-format
  scenes as not comparable until their pages are migrated to `data-sync`.
- Options: `--timelines DIR` / `--sync DIR` / `--langs DIR` point at non-default
  committed dirs (the drift tests use these for throwaway copies); `--modules a,b`
  scopes the check to the given dotted modules — timelines and maps belonging to other
  modules are skipped, so a post-refactor per-module check runs in seconds instead of
  re-recording all 72 scenes.

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

## How a page consumes a combined map (loader v2)

`Website/website/templates/content.html` wires every `[data-sync]` section on the page.
Canonical section markup:

```html
<div class="visualization-container"
     data-sync="{{ url_for('static', filename='sync/<slug>.json') }}">
    <div class="code-block">
        <button class="copy-btn" onclick="copyToClipboard(this)">Copy</button>
        <pre class="line-numbers line-highlight" data-from-sync>
            <code class="language-python"></code></pre>
    </div>
    <div class="video-container">
        <video controls><source src="..." type="video/webm" /></video>
    </div>
</div>
```

On `DOMContentLoaded` the loader fetches each section's JSON, inserts a Python/C/C++/Java
tab bar above the code block, fills the code from the JSON's active language (always when
the `<pre>` has `data-from-sync`, when its `<code>` is empty, or on any tab click), and
starts a 100 ms tracker that sets `data-line` from the active language's map.

- **Language tabs**: default is the JSON's `"default"` (python); the choice is page-wide
  (switching one section switches all) and persists in `localStorage` under
  `"algoviz-code-lang"`. Switching swaps the `<code>` content **and** its
  `language-<x>` class, re-runs Prism, and swaps the active map.
- **Multi-video pages**: one `data-sync` wrapper per video+code section, each with its
  own slug — the same shape the legacy `singly_linked_list.html` registry covered with
  `(videoId, codeBlockId, mapVar)` triples, minus the boilerplate: the loader discovers
  sections automatically, so no per-page script is needed.
- **Fetch failure** falls back to inline maps: the section's `data-map-var` names an
  inline JS array (`window[mapVar]`), or — for legacy single-video pages — the global
  `highlightMap`. Sections without either keep their authored code, un-highlighted.
- **No `data-sync` anywhere** (legacy pages): the old single-video inline-map behavior
  is preserved untouched.
