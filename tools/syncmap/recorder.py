"""Headless recorder: run a Scene's construct() without rendering and record its timeline.

Implements the NullRenderer mechanism from tools/syncmap/DESIGN.md (§3): the
renderer is injected through the ``Scene(renderer=...)`` constructor seam, so
nothing is monkey-patched. ``Scene.play`` is a shim that delegates everything to
``renderer.play`` (manim/scene/scene.py:1124-1126) and ``wait``/``pause``/
``wait_until`` funnel into ``play`` (scene.py:1168, 1192, 1206) — one
interception point covers the entire time engine.

Time model (DESIGN.md §4): every play call contributes its resolved run_time
(``max`` over animations; play kwargs are setattr'd onto each animation,
scene.py:919-921); frozen static waits are flagged so the map emitter can apply
the floor quantization rule later. Times are rounded to ``PRECISION`` decimals
so identical sources yield identical event lists across runs and platforms.
"""

from __future__ import annotations

import importlib
import sys
import traceback
import warnings
from pathlib import Path

import manim
from manim import config
from manim.animation.animation import Wait

PRECISION = 9
REPO_ROOT = Path(__file__).resolve().parents[2]
ANIMATIONS_DIR = REPO_ROOT / "Animations"
DEFAULT_TEXT_DIR = ANIMATIONS_DIR / "media" / "texts"
DEFAULT_TEX_DIR = ANIMATIONS_DIR / "media" / "Tex"


class _NullFileWriter:
    """Absorbs file-writer calls Scene can make during construct()."""

    def __init__(self):
        self.subcaptions = []

    def next_section(self, *args, **kwargs):
        pass

    def add_sound(self, *args, **kwargs):
        pass


class NullRenderer:
    """Minimal renderer that records time instead of drawing (DESIGN.md §3.2).

    Duck-types the exact ``self.renderer.*`` surface Scene touches; all state
    bookkeeping (compile, begin, finish, clean_up) reuses real, unpatched Scene
    machinery so scene-visible state advances exactly like a real render, and
    durations match manim's own skip path byte-for-byte (T1 spike, §5.2).
    """

    skip_animations = True

    def __init__(self, on_event=None):
        self.camera = None
        self.time = 0.0
        self.num_plays = 0
        self.static_image = None
        self.file_writer = _NullFileWriter()
        self._on_event = on_event

    def init_scene(self, scene):
        self.camera = scene.camera_class()

    def render(self, scene, t, moving_mobjects):
        pass

    def scene_finished(self, scene):
        pass

    def clear_screen(self):
        pass

    def play(self, scene, *args, **kwargs):
        """Record one play() call: resolve duration, advance state, advance the clock."""
        scene.compile_animation_data(*args, **kwargs)
        duration = scene.duration
        wait_call = len(scene.animations) == 1 and isinstance(scene.animations[0], Wait)
        frozen = scene.is_current_animation_frozen_frame()
        if any(getattr(a, "stop_condition", None) is not None for a in scene.animations):
            raise NotImplementedError(
                "wait(stop_condition=...)/wait_until() cannot be recorded: the real render "
                "exits its frame loop early (DESIGN.md §4.4)"
            )
        scene.begin_animations()
        if not frozen:
            scene.update_to_time(duration)
        for animation in scene.animations:
            animation.finish()
            animation.clean_up_from_scene(scene)
        scene.update_mobjects(0)
        if self._on_event is not None:
            event = {
                "t": round(self.time, PRECISION),
                "type": "wait" if wait_call else "play",
                "run_time": round(duration, PRECISION),
            }
            if wait_call:
                event["frozen"] = frozen
            self._on_event(event)
        self.time += duration
        self.num_plays += 1


def _ensure_on_path(directory: Path) -> None:
    s = str(directory)
    if s not in sys.path:
        sys.path.insert(0, s)


def _resolve_module_file(module_path: str) -> Path | None:
    """Map a module reference to a .py file, or return None if it is a dotted name."""
    candidate = Path(module_path)
    if candidate.suffix == ".py" and candidate.exists():
        return candidate
    parts = module_path.split(".")
    if len(parts) <= 2 and parts[0] == "Animations":
        file = ANIMATIONS_DIR / f"{parts[-1]}.py"
        if file.exists():
            return file
    if len(parts) == 1:
        file = ANIMATIONS_DIR / f"{parts[0]}.py"
        if file.exists():
            return file
    return None


def import_scene_module(module_path: str):
    """Import by dotted name first (cache-aware), then by file path."""
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError:
        pass
    file = _resolve_module_file(module_path)
    if file is None:
        raise ModuleNotFoundError(f"cannot resolve module {module_path!r}")
    _ensure_on_path(file.parent)
    return importlib.import_module(file.stem)


def _prepare_config(text_dir: Path | str) -> None:
    """Pin global manim config so recording matches a -ql render (DESIGN.md §4.3, §6 R5)."""
    config.frame_rate = 15
    config.progress_bar = "none"
    Path(text_dir).mkdir(parents=True, exist_ok=True)
    config.text_dir = str(text_dir)
    DEFAULT_TEX_DIR.mkdir(parents=True, exist_ok=True)
    config.tex_dir = str(DEFAULT_TEX_DIR)


def record_scene(
    module_path: str,
    scene_name: str,
    *,
    text_dir: Path | str | None = None,
) -> dict:
    """Run ``scene_name.construct()`` headless and return its timeline result.

    Returns ``{scene, module, manim_version, duration, num_plays, events, error,
    traceback}``. ``events`` holds ``{t, type: play|wait|code_step, run_time?,
    frozen?, lines?, key?}`` dicts with cumulative start times rounded to
    ``PRECISION`` decimals. If ``construct()`` raises, ``error``/``traceback``
    are filled in and the events recorded so far are still returned.

    ``text_dir`` defaults to the repo's gitignored ``Animations/media/texts``
    SVG cache so Pango ``Text`` layout stays warm and leaves no files outside
    it (DESIGN.md §6 R5); the LaTeX cache (``Animations/media/Tex``) is pinned
    the same way so headless ``MathTex`` construction works from any cwd.
    """
    _prepare_config(Path(text_dir) if text_dir is not None else DEFAULT_TEXT_DIR)
    _ensure_on_path(ANIMATIONS_DIR)
    module = import_scene_module(module_path)
    from synced import SyncedScene

    scene_cls = getattr(module, scene_name, None)
    if not (isinstance(scene_cls, type) and issubclass(scene_cls, manim.Scene)):
        raise TypeError(f"{module_path!r} has no Scene subclass named {scene_name!r}")

    events: list[dict] = []
    renderer = NullRenderer(on_event=events.append)

    def code_hook(lines, key):
        events.append(
            {
                "t": round(renderer.time, PRECISION),
                "type": "code_step",
                "lines": str(lines),
                "key": str(key or ""),
            }
        )

    scene = scene_cls(renderer=renderer)
    if isinstance(scene, SyncedScene):
        scene._syncmap_recorder = code_hook
    else:
        warnings.warn(
            f"{scene_name} does not subclass SyncedScene: recording plays/waits only "
            f"(no code_step annotations)",
            UserWarning,
            stacklevel=2,
        )

    error = None
    tb = None
    try:
        scene.setup()
        scene.construct()
        scene.tear_down()
    except Exception as e:  # noqa: BLE001 — capturing any scene failure is the feature
        error = f"{type(e).__name__}: {e}"
        tb = traceback.format_exc()

    return {
        "scene": scene_name,
        "module": module_path,
        "manim_version": manim.__version__,
        "duration": round(renderer.time, PRECISION),
        "num_plays": renderer.num_plays,
        "events": events,
        "error": error,
        "traceback": tb,
    }
