# tools/syncmap — DESIGN (Spike: run a Scene without rendering)

PROMPT 014 · TASKBOARD card T1 · Phase 2 (`docs/Plan/03-Sync-Tool.md`)
Date: 2026-09-28 · Environment: Windows 11, Python 3.13, **manim 0.19.0** (installed at
`C:\Users\paaar\AppData\Local\Programs\Python\Python313\Lib\site-packages\manim`; all citations
below use short paths like `manim/scene/scene.py:1073` relative to that root).

**Verdict up front:**

1. **Recommended mechanism:** inject a ~70-line **`NullRenderer`** through the constructor seam
   `Scene(renderer=...)`. No monkey-patching at all — `Scene.play()` is already a 3-line shim that
   delegates everything to the renderer (`scene.py:1124-1126`), and `wait`/`pause`/`wait_until`
   all funnel into `play` (`scene.py:1168, 1192, 1206`), so replacing the renderer replaces the
   entire time engine with one interception point.
2. **All 3 representative scenes run headless**, byte-identical per-event durations vs manim's own
   skip path (details in §5).
3. **Critical finding:** raw run_time sums ≠ video time. Each `play()` call contributes a
   *frame-quantized* chunk (ceil rule), each static `wait()` contributes an *int-truncated* chunk
   (floor rule). Measured drift: +33 ms in just 5 events at 15 fps; over Dijkstra's 243 play calls
   this can reach seconds. The recorder must therefore keep **two clocks** (§4): a raw timeline
   (the byte-comparable refactor oracle) and a frame-quantized timeline (what the website maps
   must use).

---

## 1. What we are replacing

### 1.1 The manual harness

`utils/createHighlightMap.ipynb` re-simulates each scene's `play`/`wait` timings **by hand** —
pure-Python `play(rt)`/`wait(d)` accumulators plus a `log(line, label)` that appends
`{time: round(time_elapsed, 3), lines: str(line), label?}` (notebook cells 1–2). The hand-copied
run_times are re-derived from reading the scene source; whenever a scene's timings change, the
notebook and the templates drift independently. `tools/syncmap` productizes exactly this loop —
but driven by the scene's real `construct()`.

### 1.2 The JS consumers (formats to keep byte-compatible)

**Single-video pages** — `Website/website/templates/content.html:104-127`:

```js
const highlightMap = [
    { time: 0.0, lines: "11" },      // lines is a STRING (Prism data-line attr)
    { time: 1.0, lines: "1" },
];
// DOMContentLoaded: setInterval(100ms) → reverse-scan highlightMap for the last
// entry with time <= video.currentTime → codeBlock.setAttribute("data-line", lines)
// → Prism.highlightElement(...)
```

Consumer reads only `.time` (number, seconds) and `.lines` (string; Prism accepts `"6"`,
`"6-7"`, `"6,7"`). Reverse scan = last-wins, so the map must be sorted ascending.

**Multi-video pages** — `Website/website/templates/LinkedList/singly_linked_list.html:532-660`:
four named globals (`createHighlightMap`, `lengthHighlightMap`, `insertHighlightMap`,
`deleteHighlightMap`) bound via an array of `{videoId, codeBlockId, mapVar}` triplets; maps are
looked up as `window[mapVar]` (line 647); entries carry an optional `label` field that this
consumer ignores; the scan loop (lines 656-660) is identical to content.html.

So the emitted website map must be an array of `{time, lines}` (+ optional `label`), ascending by
`time`, `lines` a string. `data-line` attribute usage in existing templates: single integers only.

### 1.3 The plan's target formats

From `docs/Plan/03-Sync-Tool.md` (lines 20-22): snapshot = `tools/syncmap/timelines/<Scene>.json`
with `{scene, module, manim_version, source_sha256, events:[{t, type: play|wait|code_step,
lines?, key?, run_time}]}` — **byte-comparable** (the Phase 3 refactor oracle); website map =
`Website/website/static/sync/<slug>.json` with `{video, code[], map:[{time, lines}]}`. §7 refines
both.

---

## 2. Manim 0.19 internals (what the recorder must reproduce)

### 2.1 Scene lifecycle

- `Scene.__init__(renderer=None, camera_class=Camera, ...)` — `manim/scene/scene.py:103-157`.
  If `renderer is None` it builds a `CairoRenderer(camera_class=..., skip_animations=...)`
  (lines 143-147); **otherwise it uses the injected renderer verbatim** and calls
  `self.renderer.init_scene(self)` (line 150). This is the officially designed injection seam.
- `Scene.render()` — `scene.py:226-264`: calls `setup()` → `construct()` (catching
  `EndSceneEarlyException`/`RerunSceneException`) → `tear_down()` →
  `self.renderer.scene_finished(self)` (line 247), which drains the file writer
  (`cairo_renderer.py:266-280` → `SceneFileWriter.finish()` → ffmpeg muxing). **The recorder must
  NOT call `Scene.render()`**; it drives `setup()`/`construct()`/`tear_down()` directly.
- `Scene.camera` property → `self.renderer.camera` (`scene.py:159-161`);
  `Scene.time` property → `self.renderer.time` (`scene.py:163-166`). Both are renderer-owned.

### 2.2 Time-advancing entry points (the complete list)

| Entry point | What it does | Time contribution |
|---|---|---|
| `Scene.play(*anims, **kwargs)` | `scene.py:1073-1138`. Pure shim: `start_time = self.time` → `self.renderer.play(self, *args, **kwargs)` (line 1125) → measures elapsed for subcaptions only. | whatever `renderer.play` advances |
| `Scene.wait(duration=1.0, stop_condition=None, frozen_frame=None)` | `scene.py:1140-1174`. Validates duration, then `self.play(Wait(run_time=duration, ...))` (line 1168). | delegates to `play` |
| `Scene.pause(duration=1.0)` | `scene.py:1176-1192`. Alias for `wait(frozen_frame=True)`. | delegates |
| `Scene.wait_until(cond, max_time=60)` | `scene.py:1194-1206`. `wait(max_time, stop_condition=cond)`. | delegates; **early-exit possible** |
| `Scene.add_sound(file, time_offset=0, ...)` | `scene.py:1587-1632`. **No time.** If `renderer.skip_animations` it returns immediately (line 1629-1630); else appends to `renderer.file_writer.subcaptions`/sound list at `self.time + time_offset`. | zero |
| `Scene.next_section(...)` | `scene.py:315-325`. File-writer sections only. | zero |
| `Scene.add/remove/bring_to_front/...` | `scene.py:451+` | zero |
| `interactive_embed()` / `embed()` | `scene.py:1336+, 1486+` | n/a — must never run in a recorder |

Because everything funnels into `renderer.play`, intercepting the renderer covers 100% of time
advancement with a single hook.

### 2.3 How `play` resolves run_time (real path)

`CairoRenderer.play` — `manim/renderer/cairo_renderer.py:60-118`:

1. `scene.compile_animation_data(*args, **kwargs)` (line 71) — `scene.py:1208-1254`:
   - `compile_animations` (scene.py:881-923) flattens args via `flatten_iterable_parameters`,
     builds each animation with `prepare_animation` (animation.py:543-581; converts
     `.animate` builders via `anim.build()`), then **setattrs every play-kwarg onto every
     animation** (scene.py:919-921) — this is how `play(..., run_time=2)` reaches animations, and
     it also means `play(a, b, run_time=3)` sets `run_time=3` on *both* `a` and `b`.
   - `add_mobjects_from_animations` (scene.py:1236-1237, 491-501) — adds every *non-introducer*
     animated mobject to the scene. **Required bookkeeping**: without it, later
     `scene.replace()` calls raise.
   - `self.duration = self.get_run_time(self.animations)` (scene.py:1244) —
     `get_run_time` (scene.py:1054-1071) = **`max(anim.run_time for anim in animations)`**, then
     `validate_run_time` (scene.py:1025-1052): **raises** on `run_time <= 0`, **clamps**
     `run_time < 1/fps` up to `1/fps` with a warning (scene.py:1043-1050). The clamp is
     fps-dependent — see §4.3.
   - Single-Wait short-circuit (scene.py:1245-1252): if the only animation is a `Wait` with no
     stop-condition/updaters, marks it static and **returns `None` early — but only after
     `self.duration` was set** (line 1244), so the duration is always available.
2. If `renderer.skip_animations`: `self.time += scene.duration` (cairo_renderer.py:76) —
   **this is the exact time rule the recorder mirrors.** Otherwise hashing/caching
   (lines 78-94), `file_writer.add_partial_movie_file` (96), `begin_animation(not skip)` (103).
3. `scene.begin_animations()` (line 104) — scene.py:1256-1268: per animation `_setup_scene`
   (adds introducers, animation.py:249-266) and `begin()` (snapshot starting mobject, suspend
   updaters, `interpolate(0)` — animation.py:202-219); plus a Cairo-only moving/static split.
4. `save_static_frame_data` (line 107) — the one place skip mode still burns cairo:
   `update_frame(ignore_skipping=True)` → `camera.capture_mobjects` (cairo_renderer.py:214-239,
   120-157). Avoided entirely by the NullRenderer.
5. Frozen static-wait path (lines 109-113): `update_frame` + `freeze_current_frame(duration)` →
   `add_frame(..., num_frames=int(duration/dt))` (cairo_renderer.py:192-204). Else
   `scene.play_internal()` (line 115) — scene.py:1278-1309: builds the frame loop, calls
   `renderer.render` per frame, then per animation `finish()` (`interpolate(1)` — applies end
   state) + `clean_up_from_scene` (removers; `Transform.replace_mobject_with_target_in_scene` →
   `scene.replace` — transform.py:212-215, **raises ValueError if the mobject was never added**,
   scene.py:579-580), then `update_mobjects(0)` (scene.py:1305-1306) and
   `renderer.static_image = None` (1307).

### 2.4 Wait and animation defaults

- `DEFAULT_ANIMATION_RUN_TIME = 1.0` (`manim/animation/animation.py:28`);
  `Animation.__init__(run_time=DEFAULT_ANIMATION_RUN_TIME)` (animation.py:131-147); the
  `run_time` setter rejects negatives (animation.py:175-186).
- `DEFAULT_WAIT_TIME = 1.0` (`manim/constants.py:182`) — the default of both `Scene.wait`
  (scene.py:1142) and `pause` (scene.py:1176).
- `Wait(Animation)` — animation.py:584-638: stores `duration = run_time`, `is_static_wait` from
  `frozen_frame`; `begin/finish/clean_up/interpolate` are all no-ops (lines 625-638).

### 2.5 Composition (nested) run_times — confirmed without rendering

`manim/animation/composition.py`:

- `AnimationGroup.__init__` computes `self.run_time = self.init_run_time(run_time)` at
  construction (lines 55-79) — **pure Python, no renderer needed**.
- `init_run_time` (121-142): `max_end_time = max(anims_with_timings["end"])`;
  returns `max_end_time` if `run_time is None`, else the explicit `run_time` (line 142).
- `build_animations_with_timings` (144-158): `start[i] = lag_ratio * sum(run_times[:i])`,
  `end[i] = start[i] + run_times[i]`.
- `Succession` (194-232): `lag_ratio=1` → total = **sum** of sub-run_times.
- `LaggedStart` (293-344): `lag_ratio=0.05` default → total = `max_i(0.05·Σ prev + rt_i)`.
- `LaggedStartMap` (347-403): default `run_time=2` explicit override.
- **lag_ratio never inflates an explicit `run_time`** — `play(..., lag_ratio=k)` kwargs are
  setattr'd per-animation (scene.py:919-921) and only matter to groups via `init_run_time`.
  Verified empirically in §5.3.

---

## 3. Recorder mechanism

### 3.1 Options considered

**Option A — inject a fake/null renderer (`Scene(renderer=NullRenderer())`).**
The renderer is a constructor parameter intended for substitution (scene.py:103-110, 143-150).
The fake's `play()` reuses the *real* `Scene` machinery for everything except drawing:
`compile_animation_data` → `duration`, `begin_animations`, one `update_to_time(duration)` state
step, the `finish()/clean_up_from_scene()` tail, then `self.time += duration` — mirroring
`CairoRenderer.play`'s skip path (cairo_renderer.py:76) and `play_internal`'s tail
(scene.py:1302-1307) with zero pixel work.

**Option B — monkey-patch `Scene.play`/`Scene.wait` on the class or instance.**
Rejected: (a) instantiating the scene still auto-creates a real `CairoRenderer` +
`SceneFileWriter` (scene.py:143-147), which creates media directories
(`scene_file_writer.py:108-125, 127-202`) unless `config.dry_run` is also flipped — so B needs
*a second* patch or config side effect; (b) the patch duplicates exactly the logic Option A
writes once, with worse failure modes (patch ordering, leakage across a 72-scene `--all` run,
interference with parallel test runs); (c) `wait`/`pause`/`wait_until` must each be considered
even though they delegate to `play` — a fact the patch author must re-verify.

**Option A′ — real `CairoRenderer` + `config.dry_run=True` + `skip_animations=True`.**
Manim's own skip mode. Works headless and (per §5.2) produces byte-identical durations — but it
still renders one static cairo frame per `play()` (`save_static_frame_data` →
`update_frame(ignore_skipping=True)` → `camera.capture_mobjects`, cairo_renderer.py:107,
214-239), constructs the full `SceneFileWriter`, and drags in hashing/section bookkeeping.
Costly and fragile for zero benefit; **keep it as the cross-validation oracle in unit tests**
(a test asserts NullRenderer == CairoRenderer(dry_run) on synthetic scenes).

### 3.2 RECOMMENDATION: Option A (NullRenderer injection)

Minimal duck-type surface, derived from every `self.renderer.*` touchpoint in `scene.py`:

| Member | Used by | NullRenderer provides |
|---|---|---|
| `init_scene(scene)` | scene.py:150 | builds `self.camera = scene.camera_class()` (supports `MovingCameraScene` subclasses; none in repo today) |
| `camera` | scene.py:159-161, 448, 664, 867, 873 | real `Camera()`-family instance (needs `.use_z_index`, `.frame_rate`; no pixels ever drawn) |
| `time` (rw float) | scene.py:163-166, 1124, 1126 | accumulated timeline — **the recorder's clock** |
| `num_plays` (rw int) | scene.py:251, cairo_renderer.py:118 | counter, incremented per play |
| `skip_animations = True` | scene.py:1629-1630, 1305 | makes `add_sound` a no-op; keeps `play_internal` parity |
| `static_image` (rw) | scene.py:1307 | writable `None` |
| `file_writer` | scene.py:325, 1580-1585, 1632 | stub: `subcaptions=[]`, no-op `next_section`, no-op `add_sound` |
| `play(scene, *args, **kwargs)` | scene.py:1125 | the recorder core (§3.3) |
| `render(scene, t, moving)` | scene.py:1297 | no-op safety net (not on the NullRenderer path) |
| `scene_finished(scene)` / `clear_screen()` | scene.py:242-247 | no-ops (recorder never calls `Scene.render()`, but stay safe if a `construct()` does) |
| `window` | scene.py:1328, 1420, 1483 | absent; `interactive_embed` must never run — recorder raises if it sees it |

`renderer.camera.frame_rate` must equal the render fps (§4.3).

### 3.3 `NullRenderer.play` — exact algorithm

```python
def play(self, scene, *args, **kwargs):
    scene.compile_animation_data(*args, **kwargs)   # raises on empty play; sets scene.duration
    duration = scene.duration                       # scene.py:1244 — set before the Wait branch
    frozen = scene.is_current_animation_frozen_frame()   # scene.py:1270-1276
    if frozen and scene.animations[0].stop_condition is not None:
        raise NotImplementedError("stop_condition waits cannot be recorded (§4.4)")
    scene.begin_animations()                         # scene.py:1256: _setup_scene + begin()
    if not frozen:
        scene.update_to_time(duration)               # scene.py:1528: single-step state advance,
                                                     # identical to skip mode's times=[run_time]
                                                     # (scene.py:1010-1011)
    for anim in scene.animations:
        anim.finish()                                # interpolate(1): apply end state
        anim.clean_up_from_scene(scene)              # removers; Transform -> scene.replace
    scene.update_mobjects(0)                         # scene.py:1305-1306 parity
    self.time += duration                            # cairo_renderer.py:76 parity
    self.num_plays += 1                              # cairo_renderer.py:118 parity
    record_event(type="wait" if frozen else "play", run_time=duration, frozen=frozen)
```

**Nothing else must be patched.** `wait`/`pause`/`wait_until` all reach `renderer.play`
(scene.py:1168, 1192, 1206); `add_sound` self-guards on `skip_animations` (scene.py:1629);
`next_section`/subcaptions land on the stub. Cairo is never entered: the only draw paths
(`update_frame`/`render`/`get_frame`) live inside `CairoRenderer`, which is never constructed.

### 3.4 Why the state bookkeeping (begin/finish/clean_up) is not optional

Scenes in this repo depend on post-play scene state:

- `ReplacementTransform` cleanup calls `scene.replace(old, new)` — **ValueError if the old
  mobject was never added** (transform.py:212-215, scene.py:579-580). Dijkstra and TreeBFS would
  crash within ~10 play calls without `add_mobjects_from_animations` + `clean_up_from_scene`.
- Geometry reads drive placement: `distMob[2]` after transforms (Graphs.py:1510),
  `queue_text.move_to(queue_text)` chains (Trees.py:288-324). Applying end state via
  `finish()`/`update_to_time` keeps those reads correct; only *timing* would survive without
  it, and construct would still crash on `scene.replace`.
- Mobjects never being *drawn* is irrelevant — `Text`/Pango, geometry (`.get_center()`,
  `.next_to()`), `Graph` layouts are all computed at construction, headless-safe (§5.1).

---

## 4. Time model (exact rules)

### 4.1 Raw timeline (the oracle clock)

Cumulative time before event *i*: `t_0 = 0`, `t_{i+1} = t_i + d_i` where `d_i` is the play call's
resolved duration:

| Call | Duration `d` | Rule (source) |
|---|---|---|
| `play(anim, ...)` no run_time | `anim.run_time` | animation.py:135 (`Animation`, default 1.0) |
| `play(a1, a2, ...)` | `max(run_times)` | scene.py:1069 |
| `play(..., run_time=r)` | `r` (setattr on every animation) | scene.py:919-921 |
| `play(AnimationGroup(g...))` | `max_end_time` = `max_i(start_i + rt_i)` | composition.py:141-142 |
| `play(AnimationGroup(..., run_time=r))` | `r` overrides | composition.py:142 |
| `play(Succession(a1..an))` | `Σ rt_i` (lag_ratio=1) | composition.py:231-232 |
| `play(LaggedStart(a1..an, lag_ratio=k))` | `max_i(k·Σ_{j<i} rt_j + rt_i)` | composition.py:155-158 |
| `play(LaggedStartMap(A, mob))` | 2.0 unless overridden | composition.py:390 |
| `wait(d)` / `pause(d)` | `d` (validated) | scene.py:1167, 1191 |
| `wait()` / `pause()` | 1.0 | constants.py:182 |
| `play(Wait(run_time=d))` directly | `d` | animation.py:609 |
| `add_sound(...)`, `add`/`remove`, `next_section` | 0 | scene.py:1587-1632, 451+ |

Validation at record time (`validate_run_time`, scene.py:1025-1052): `d <= 0` raises;
`d < 1/fps` is **clamped to `1/fps`** — e.g. `wait(0.05)` (AVLTree.py:1563,1565) records as
`1/15 s` at the web fps.

No implicit waits exist: `setup`/`construct`/`tear_down` add no time, and there is no
trailing pause — the raw end of a scene is the last play's duration.

### 4.2 Video timeline (frame quantization — REQUIRED for web maps)

The rendered video does not contain `d` seconds per play call; it contains whole frames:

- **Frozen static waits** (single `Wait`, `is_static_wait=True`): `freeze_current_frame` adds
  `int(duration / dt)` frames, `dt = 1 / camera.frame_rate` — **floor rule**
  (cairo_renderer.py:192-204, 186).
- **Everything else** (plays, dynamic waits): `play_internal` iterates
  `np.arange(0, duration, 1/fps)`, one `add_frame` per step — **arange/ceil rule**
  (scene.py:1013-1014, 1294-1297; cairo_renderer.py:175-190).

So the quantized timeline at target fps F is:

```python
frames += int(d / (1 / F))          if frozen          # floor
frames += np.arange(0, d, 1 / F).size if not frozen    # ceil (exact arange semantics)
video_time = frames / F
```

**Empirical proof** (§5.4): at 15 fps, `play(1.0)`→15 f, `wait(0.7)`→10 f (0.6667 s, −33 ms),
`play(0.7)`→11 f (0.7333 s, +33 ms), dynamic `wait(0.5)`→8 f (+33 ms), `wait(1.0)`→15 f.
Raw sum 3.9 s → video 59 frames = 3.9333 s. Per-event drift is bounded by ±1 frame but
**accumulates** — hand-maps that "look right" were eyeballed against the quantized video; a
raw-sum map would drift by up to seconds over Dijkstra's 243 plays. Consequence for this tool:

- **Timeline snapshots store raw `t`** (fps-agnostic, byte-comparable oracle).
- **Website maps store frame-quantized `time`** computed at `--fps` (default 15, the web
  standard; `manim.cfg` says 30 — that's the *render-profile* default, `-ql` overrides to 15).

### 4.3 fps coupling

`validate_run_time`'s clamp (§4.1) and both quantization rules depend on fps. The recorder must
run with `config.frame_rate = 15` (and `Camera` built under that config) so recorded durations
are exactly what a `-ql` render produces. The `map` command re-quantizes with the same F.

### 4.4 Special cases

- `wait(stop_condition=...)` / `wait_until(...)`: the real render **breaks the frame loop early**
  (scene.py:1298-1300) — video length depends on runtime conditions the recorder cannot know.
  Recorder behavior: raise `NotImplementedError`. Current repo usage: **zero** (grep over
  `Animations/*.py`).
- `add_sound`: contributes no time (scene.py:1587-1632); NullRenderer no-ops it (no repo usage).
- `pause()` is always frozen (scene.py:1192) → floor rule.
- Scene-internal `time.sleep` / wall-clock waits: none exist in `Animations/` (grep); if one
  appeared it would freeze real rendering but not advance the recorder clock — flagged by the
  T7 snapshot-vs-video duration spot-checks.
- There is no `Scene.clock` attribute in manim 0.19 — the only clock is `renderer.time`
  (scene.py:163-166), which the NullRenderer owns.

---

## 5. Empirical results (throwaway scripts, deleted after use)

All runs on this host (Python 3.13, manim 0.19.0), scripts executed from a temp directory
outside the repo; `git status` verified clean afterwards.

### 5.1 Headless `construct()` of the 3 representative scenes (NullRenderer)

| Scene | Module | Result | Raw total | play calls | Wall time |
|---|---|---|---|---|---|
| `LinearSearch` | SearchingAlgorithms.py:36 | **OK** | 9.5 s | 25 | 5.0 s (cold fonts) |
| `TreeBFS` | Trees.py:234 | **OK** | 73.9 s | 152 | 12.8 s |
| `Dijkstra` | Graphs.py:1442 | **OK** | 118.9 s | 243 | 32.1 s |

No scene needed a real render pass: `Text` (Pango), `Graph`/`DiGraph` (networkx layouts),
`ReplacementTransform` chains, `.get_center()`/`.next_to()` geometry reads all completed
headless. T2's "<10 s for TreeBFS" target is realistic once the `media/texts` SVG cache is warm
(§6 R5).

### 5.2 Cross-validation vs manim's own skip mode

`LinearSearch` run twice — once with `NullRenderer`, once with the real
`CairoRenderer(skip_animations=True)` under `config.dry_run=True, write_to_movie=False`:

- totals identical (9.5 s / 25 plays both);
- **per-event durations: 25/25 exactly equal** (`events == events → True`).

Conclusion: the NullRenderer's time model is byte-equivalent to upstream manim's skip path —
the recommended mechanism is validated against manim itself, not just against theory. Keep this
comparison as a permanent unit-test oracle (§8, PROMPT 015).

### 5.3 Composition run_time probes (NullRenderer, one `play()` each)

| Animation | Recorded `run_time` | Formula check |
|---|---|---|
| `AnimationGroup(Create×3)` (Create=1 s each) | 1.000000 | `max(1,1,1)` ✓ |
| `AnimationGroup(Create×3, run_time=5)` | 5.000000 | explicit override ✓ |
| `Succession(Create×3)` | 3.000000 | `Σ = 3` ✓ |
| `LaggedStart(Create×3)` (lag 0.05) | 1.100000 | `max(1, 1.05, 1.1)` ✓ |
| `LaggedStart(Create×3, lag_ratio=0.25)` | 1.500000 | `max(1, 1.25, 1.5)` ✓ |
| `wait()` default | 1.000000 | constants.py:182 ✓ |
| `play(a, b, run_time=3)` | 3.000000 | setattr-override ✓ |

Groups expose their totals at construction (composition.py:79) — **no rendering required**,
and `lag_ratio` alone never stretches an explicit or default total (§2.5).

### 5.4 Frame-quantization probe (real `-ql` render at 480p15, temp media dir)

Scene: `play(Create)` → `wait(0.7)` → `play(Transform, run_time=0.7)` → dynamic `wait(0.5)`
(ValueTracker with a dt-updater in scene) → `wait()`. Partial movie files counted with PyAV:

| # | Call | Rule | Frames | Video time | Raw | Δ |
|---|---|---|---|---|---|---|
| A | `play` default 1.0 | arange | 15 | 1.0000 | 1.0 | 0 |
| B | `wait(0.7)` static | floor `int(0.7·15)` | 10 | 0.6667 | 0.7 | −0.0333 |
| C | `play(0.7)` | arange | 11 | 0.7333 | 0.7 | +0.0333 |
| D | `wait(0.5)` dynamic | arange | 8 | 0.5333 | 0.5 | +0.0333 |
| E | `wait(1.0)` static | floor | 15 | 1.0000 | 1.0 | 0 |
| — | **total** | | **59** | **3.9333** | **3.9** | **+0.0333** |

Final mp4 = 59 frames / 3.9333 s. Both §4.2 rules confirmed exactly.

### 5.5 Failures encountered and workarounds (already folded into the design)

- None of the three scenes failed headless — the *predicted* failure modes were avoided by the
  NullRenderer's built-in bookkeeping (§3.4): skipping `add_mobjects_from_animations` /
  `clean_up_from_scene` would have raised `ValueError: Could not find … in scene` from
  `Transform.clean_up_from_scene` within the first `ReplacementTransform` (Trees.py:289).
- Side effect observed: every distinct `Text` string/font/color combination writes a cached SVG
  into `config.get_dir("text_dir")` — `media/texts/` — via `Text._text2svg`
  (text_mobject.py:824-847). 130+ SVGs appeared in the temp cwd during the 3-scene run. It is a
  **content-addressed, idempotent cache** (hash-named, reused across runs), but the recorder
  should point it at the repo's existing `Animations/media/texts` (warm) or a scratch dir
  (hermetic) rather than scatter files wherever cwd happens to be.
- The real-renderer variant needed `config.dry_run=True` + `write_to_movie=False` to avoid
  creating `media/` directory trees (scene_file_writer.py:127-202 early-returns on dry_run) —
  further evidence for preferring NullRenderer (no file writer at all).

---

## 6. Risks & edge cases (ranked)

**R1 — Frame-quantization drift (design-level, resolved).** Raw sums misalign with rendered
video (§4.2, §5.4). Resolved by the two-clock model; the `map` command must quantize. *Residual
risk:* the mp4→webm conversion (tools/convert_webm.py, moviepy) must preserve frame timing —
already assumed by the current hand-maps; T7 spot-checks it (compare map totals vs PyAV duration
of the committed webms).

**R2 — Updater-driven state divergence.** The NullRenderer advances state in ONE time step
(`update_to_time(duration)`), exactly like manim's skip mode, while a real render takes
N steps; dt-integrating updaters (time-based `add_updater(lambda m, dt: ...)`) can end at
slightly different positions. Timing is unaffected **unless a scene branches on updater-driven
geometry**. Repo inventory: `LinkedList.py` (dynamic bezier/arrowhead updaters, e.g. lines
192-196), `Arrays.py` (ValueTracker-driven pointers, lines 214-221), `Trees.py` `UnionFind`
(edge updaters, line 2101), `AVLTree.py` (balance-factor updaters) — most are position lambdas
`(m)` (not time-based), and no scene keys control flow on updater output today. Mitigation: T7
baseline + duration spot-checks vs real renders for the updater-heavy files; document any scene
whose recorded total disagrees with its committed video.

**R3 — `Text`/Pango + LaTeX at construction time.** `Text` layout (and the `media/texts` SVG
cache) and `MathTex` (LaTeX→SVG; used by Arrays.py:314+, Trees.py:1105+, Graphs.py:1773+) all
execute during `construct()`. The recorder host therefore needs the same fonts + LaTeX stack
as the render host — *construction* failure is a loud crash (snapshot fails, no silent drift),
and missing fonts change geometry only, never run_times. `wait(0.05)`-style sub-frame calls
(AVLTree.py:1563) are clamped at 15 fps — recorder must set `config.frame_rate=15` (§4.3).

**R4 — Import side effects & determinism across `--all`.** `Trees.py` runs `random.seed(32)` at
import; any scene using `random` *without* seeding would leak state between scenes in one
process. Snapshot CLI must isolate runs (subprocess per module, or documented single-process
order) so the 72 snapshots are reproducible and order-independent.

**R5 — `media/texts` cache pollution.** (§5.5) Recorder pins `config.text_dir` to the repo's
existing `Animations/media/texts` (warm cache, gitignored churn risk low — files are
hash-named) or a scratch dir in `--all` mode. Never write relative to an accidental cwd.

**R6 — Unsupported constructs.** `wait_until`/`stop_condition` (early exit, unknowable — raise),
`interactive_embed`/`embed` (raise), `add_sound` (no-op, zero time), `Scene.render()` (never
called — bypasses `scene_finished`/ffmpeg). All currently unused in `Animations/`; the recorder
fails loudly rather than emitting a wrong map.

**R7 — Wait-frozen detection.** The floor-vs-ceil rule hinges on `is_static_wait`, decided by
`Scene.should_update_mobjects` (scene.py:382-407) from live updater state at play time. The
NullRenderer inherits that logic verbatim (it calls the real `compile_animation_data`), so
classification can't diverge from a real render. Frozen-ness is recorded per event so `map` can
re-quantize at any fps without re-running scenes.

---

## 7. JSON schemas

### 7.1 Timeline snapshot — `tools/syncmap/timelines/<Scene>.json` (oracle)

Byte-comparable: fixed key order, no timestamps, no paths outside the repo, floats rounded to
6 decimals, LF endings. `source_sha256` lets `check` flag stale snapshots vs edited scenes.

```json
{
  "schema": "syncmap/timeline@1",
  "scene": "LinearSearch",
  "module": "Animations/SearchingAlgorithms.py",
  "manim_version": "0.19.0",
  "source_sha256": "<sha256 of module file at snapshot time>",
  "duration": 9.5,
  "events": [
    { "t": 0.0,  "type": "wait",      "run_time": 1.0, "frozen": true },
    { "t": 1.0,  "type": "play",      "run_time": 0.4 },
    { "t": 1.4,  "type": "code_step", "lines": "5", "key": "check_0" },
    { "t": 1.4,  "type": "play",      "run_time": 0.2 }
  ]
}
```

- `t` = raw cumulative seconds at event start (§4.1); `code_step` consumes no time.
- `frozen` present on `wait` events only (drives §4.2 floor rule at map time).
- `lines` = Prism `data-line` string ("6" / "6-7" / "6,7"); `key` optional human token.
- `code_step` events appear only for `SyncedScene` subclasses (§8, PROMPT 015); plain scenes
  snapshot as pure play/wait timelines (still the refactor oracle).

### 7.2 Website map — `Website/website/static/sync/<slug>.json` (consumer)

Exactly the shape the existing loaders scan (§1.2), plus the code to display:

```json
{
  "video": "Videos/SearchingAlgorithms/LinearSearch.webm",
  "code": [
    "def linear_search(arr, target):",
    "    for i, v in enumerate(arr):",
    "        if v == target:",
    "            return i",
    "    return -1"
  ],
  "map": [
    { "time": 0.0,    "lines": "5" },
    { "time": 1.0667, "lines": "1" },
    { "time": 1.6,    "lines": "2" }
  ]
}
```

- `map[].time` = **frame-quantized** seconds at fps 15, rounded to 4 decimals, ascending,
  last-wins reverse scan (content.html:114-119).
- `map[].lines` = string, matches `data-line`.
- `code` = `SyncedScene.DISPLAY_CODE` (list of source lines, `""` for blanks) — emitted lines
  are validated to exist in `code` (1-based, no zero/negative).
- Consecutive duplicates (`lines` unchanged) are collapsed by the emitter (harmless either way).
- Multi-video pages: one JSON per video, slug-suffixed
  (`singly-linked-list-create.json`, `...-length.json`, ...) mirroring the
  `highlightPairs` binding in singly_linked_list.html:620-642.
- Loader upgrade (T5): if the video container has `data-sync="/static/sync/<slug>.json"`,
  `content.html` fetches it and builds the same `highlightMap` structure (with inline
  `highlightMap` fallback untouched) — one code path, two sources.

---

## 8. Build plan for PROMPTS 015–019

Mapping to `docs/Plan/03-Sync-Tool.md` cards: 015 = T2+T3, 016 = T4, 017 = T5, 018 = T6+T8,
019 = T7.

### PROMPT 015 — Recorder core + SyncedScene (T2, T3)

1. `tools/syncmap/recorder.py`:
   - `NullRenderer` per §3.2/§3.3 (≈70 lines, no file writer, no cairo).
   - `record(module_path, scene_name) -> dict` — sys.path setup so `from env_config import *`
     resolves (cwd `Animations/` or path injection); set `config.frame_rate=15`,
     `config.progress_bar="none"`, pin `config.get_dir("text_dir")` (§6 R5); import module by
     path, locate `Scene` subclass, instantiate `cls(renderer=NullRenderer())`; drive
     `setup()/construct()/tear_down()` directly (**never `Scene.render()`**); return §7.1 dict.
2. `Animations/synced.py` — `SyncedScene(Scene)` with `DISPLAY_CODE: list[str]` and
   `code_step(lines: str, key: str = "")` that forwards to an injected
   `self._syncmap_recorder` hook if present, else no-op (zero impact on real renders). The
   recorder sets the hook before `construct()`; detection via `isinstance` (T3 spec).
3. Unit tests (`tests/test_syncmap_recorder.py`) with synthetic scenes:
   - cumulative raw times: `play(x)`→1.0; `wait(2)`→3.0; `play(x, run_time=0.5)`→3.5;
   - all §5.3 composition cases + `lag_ratio` non-effect;
   - clamp: `play(run_time=0.05)` at fps 15 → 1/15 (warning tolerated);
   - `play()` with no animations raises (scene.py:1233);
   - `code_step` ordering: event `t` lands between surrounding plays; hook absent → no-op;
   - **cross-validation oracle**: NullRenderer event list == `CairoRenderer(skip_animations,
     dry_run)` event list on the same synthetic scenes (§5.2 pattern).
   - Verify: recorder runs `TreeBFS` warm in <10 s; one plain scene renders unaffected.

### PROMPT 016 — Snapshot CLI (T4)

1. `python -m tools.syncmap snapshot --scene <Module> <Scene>` / `--all [--batch N]` →
   `tools/syncmap/timelines/<Scene>.json` + `manifest.json`
   (`scene → module → source_sha256 → n_events → duration`).
2. Determinism: fixed JSON key order, `round(x, 6)`, LF, no timestamps; **re-run must be
   byte-identical** (that's the oracle contract). `--all` isolates per-module runs (subprocess)
   for import side effects (§6 R4); one failing scene logs and doesn't kill the batch.
3. Non-SyncedScenes snapshot fine (play/wait only, no code_step) — all 72 scenes are in scope.
4. Verify: `snapshot --all` completes; two consecutive runs byte-identical.

### PROMPT 017 — Map emit + website loader (T5)

1. `python -m tools.syncmap map <Module> <Scene> --slug linear-search [--fps 15]` →
   `Website/website/static/sync/<slug>.json` (§7.2): quantize (§4.2 rules from the snapshot's
   `frozen` flags), take `code` from `DISPLAY_CODE`, validate `lines` exist in `code`.
2. `content.html` loader: `data-sync` fetch path + inline fallback (§7.2).
3. Proof (card spec): hand-annotate a small SyncedScene (`LinearSearch`), emit, wire the page,
   watch highlighting vs video — must be precise at 15 fps boundaries.
4. Verify: route 200, video 200, JSON fetch 200 in dev server; link checker green.

### PROMPT 018 — Drift check + docs (T6, T8)

1. `python -m tools.syncmap check [--legacy]`: re-snapshot live, byte-diff against committed
   timelines + manifest (non-zero exit on drift); `check --legacy` additionally parses inline
   template maps and reports suspected drift (informational only).
2. `tools/syncmap/README.md`: usage, the two-clock time model (§4), SyncedScene convention,
   unsupported constructs (§4.4); sync the `dsa-highlightmap` skill if CLI drifts.
3. Verify: mutate a `run_time` in a scene → `check` flags; revert → green.

### PROMPT 019 — Baseline snapshots (T7)

1. `snapshot --all` over the post-Phase-1 codebase; commit timelines + manifest.
   **These are the Phase 3 behavior-preservation oracle (G3 gate).**
2. Spot-check updater-heavy scenes (Arrays.py, LinkedList.py, Trees.py, AVLTree.py): recorded
   totals vs committed webm durations (PyAV) — catches R2 empirically.
3. Verify: all 72 scenes deterministic; spot-check report in the PR description.

---

## Appendix A — NullRenderer interface cheat-sheet

```python
class NullRenderer:                       # injected via Scene(renderer=...)
    skip_animations = True                 # scene.py:1629 (add_sound guard), 1305
    def __init__(self): self.time = 0.0; self.num_plays = 0; self.static_image = None
                                        # + file_writer stub: subcaptions=[], next_section(), add_sound()
    def init_scene(self, scene):           # scene.py:150
        self.camera = scene.camera_class() # real Camera; .use_z_index needed (scene.py:448,664)
    def play(self, scene, *args, **kwargs) # §3.3 — compile → duration → begin/update/finish
                                            # → time += duration (cairo_renderer.py:76 parity)
    def render(self, *a): pass             # never hit; safety net
    def scene_finished(self, scene): pass  # only reachable via Scene.render(), which we avoid
    def clear_screen(self): pass           # only on RerunSceneException (scene.py:242)
```

Everything else — `compile_animation_data`, `compile_animations`, `get_run_time`,
`validate_run_time`, `begin_animations`, `update_to_time`, `update_mobjects`,
`should_update_mobjects`, `add_mobjects_from_animations` — is inherited, real, unpatched
`Scene` machinery.
