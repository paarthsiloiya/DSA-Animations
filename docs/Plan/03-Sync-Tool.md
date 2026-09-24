# 03 — Phase 2: Sync Tool (highlightMap generator)

**Objective (Goal G2):** a Python tool that "parses" an animation class and emits the exact timestamp→line mapping **and** the code to display — no more eyeballed JS. Doubles as the refactor oracle (Phase 3) and the page-building engine (Phase 4).

## Design

**Core idea:** Manim's `Scene.play()`/`wait()` fully determine the video timeline. A recorder runs `construct()` with patched `play`/`wait` that (a) accumulate exact run_times (default 1s per play, `run_time=` kwarg, `wait(duration)`), (b) record a `code_step(lines)` event at the current timestamp. No rendering, no video — seconds per scene, not minutes.

**Convention** (in `Animations/synced.py`, created by T3):

```python
class SyncedScene(Scene):
    DISPLAY_CODE: list[str] = []            # the code the page shows — single source of truth
    def code_step(self, lines: str, key: str = "") -> None:
        pass                                 # no-op during real rendering; captured by recorder
```

**Time model (T2 spike must confirm against manim 0.19):** `play()` default `run_time=1`; `wait(d)`; `Succession`/`LaggedStart` sum their parts (or expose total); `lag_ratio` doesn't change total duration; `AnimationGroup(run_time=...)` overrides.

**Formats:**
- Timeline snapshot: `tools/syncmap/timelines/<Scene>.json` — `{scene, module, manim_version, source_sha256, events: [{t, type: "play"|"wait"|"code_step", lines?, key?, run_time}]}`. **Byte-comparable** — that's the refactor oracle.
- Website map: `Website/website/static/sync/<slug>.json` — `{video: "Videos/<Cat>/<Scene>.webm", code: ["…"], map: [{time, lines}]}` — consumed by the `content.html` loader.

Cards:

### T1 — Spike: recorder feasibility
Agent: explore · Depends: — · Size: M
**Do:** Research task (no product code): how manim 0.19's `Scene.render/construct/play/wait` resolve run_times (incl. `Succession`, `LaggedStart`, nested `AnimationGroup`); read `utils/createHighlightMap.ipynb` (the manual harness this productizes) and `Website/website/templates/content.html:104-137` + `singly_linked_list.html:532-660` (consumer formats). Deliver `tools/syncmap/DESIGN.md`: patched-method inventory, time model, edge cases, risks.
**Done when:** DESIGN.md written; time model confirmed (cite manim source lines).

### T2 — Recorder core + tests
Agent: general · Depends: T1 · Size: L
**Do:** `tools/syncmap/recorder.py`: import scene class by module path, patch `play`/`wait` (+ any T1 findings), run `construct()`, emit event list. Unit tests with synthetic scenes asserting exact cumulative times (e.g. `play(x)`→1.0, `wait(2)`→3.0, `play(x, run_time=0.5)`→3.5) and `code_step` capture ordering.
**Verify:** `pytest` green; recorder runs a real scene (`TreeBFS`) in <10s and its total duration matches a manual sum from the source.
**Done when:** deterministic, tested.

### T3 — `SyncedScene` convention module
Agent: general · Depends: — · Size: S
**Do:** `Animations/synced.py` with `SyncedScene` (code above). Zero impact on rendering (pure no-op). Recorder detects it via `isinstance`.
**Verify:** render one plain scene unaffected; recorder sees a non-SyncedScene and warns (no code_events).
**Done when:** merged.

### T4 — Snapshot CLI
Agent: general · Depends: T2, T3 · Size: M
**Do:** `python -m tools.syncmap snapshot --scene Animations.Trees TreeBFS` / `--all --batch 10` → timelines + `manifest.json` (scene→module→sha). Non-SyncedScenes snapshot fine too (they just have no `code_step` events) — **all 72 scenes are snapshotted; they're the refactor oracle**.
**Verify:** snapshot `--all` completes; re-running yields byte-identical files.
**Done when:** deterministic across two runs.

### T5 — Map emit + website loader
Agent: general · Depends: T4 · Size: M
**Do:** `python -m tools.syncmap map <Module> <Scene> --slug <slug>` → emits website JSON (code from `DISPLAY_CODE`, map from `code_step` events; validate lines exist in code). Upgrade `content.html` loader: if the video container has `data-sync`, fetch the JSON and use it (code block content can also be rendered from `code`), else fall back to the existing inline-map behavior. Multi-video pages unchanged.
**Verify:** hand-annotate one small scene (e.g. `LinearSearch`), emit, wire a scratch page, watch highlighting vs video — precise.
**Done when:** one real page syncs from JSON.

### T6 — Drift check
Agent: general · Depends: T4, T5 · Size: M
**Do:** `python -m tools.syncmap check [--legacy]`: recompute live timelines/maps, diff against committed files; `--legacy` also parses inline template maps of old pages and reports suspected drift (informational). Non-zero exit on real drift.
**Verify:** mutate a `run_time` in a scene → `check` flags it; revert.
**Done when:** detects injected drift.

### T7 — Baseline snapshots (the oracle)
Agent: general · Depends: T4, **after all Phase 1 manim fixes** · Size: M
**Do:** `snapshot --all` over the post-P1 codebase; commit timelines + manifest. **These are the behavior-preservation baselines for Phase 3.**
**Done when:** all 72 scenes snapshotted, deterministic.

### T8 — Tool docs + skill sync
Agent: general · Depends: T2–T6 · Size: S
**Do:** `tools/syncmap/README.md` (usage, time model, conventions) + update the `dsa-highlightmap` skill if CLI details drifted from the design.
**Done when:** docs match reality.

### Phase 2 exit gate (dsa-auditor)

- [ ] All 72 scenes snapshotted deterministically; committed
- [ ] `map` emits valid JSON consumed by a real page with visibly-precise highlighting
- [ ] `check` catches injected drift
- [ ] `pytest` + link checker green
