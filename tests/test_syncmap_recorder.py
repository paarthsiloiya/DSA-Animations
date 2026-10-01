"""syncmap recorder: exact timeline capture from headless Scene runs (plan card T2).

Synthetic scenes only — no repo animation file is recorded here. The time model
asserted is the one verified in tools/syncmap/DESIGN.md §4/§5.
"""

import subprocess
import sys
from pathlib import Path

import pytest
from manim import Circle, Create, LaggedStart, Scene, Square, Succession, Uncreate

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "Animations"))

from synced import SyncedScene

from tools.syncmap.recorder import record_scene


class PlainPlays(SyncedScene):
    def construct(self):
        square = Square()
        self.play(Create(square))
        self.play(Uncreate(square))


class WaitTwo(SyncedScene):
    def construct(self):
        self.wait(2)


class MixedTimings(SyncedScene):
    def construct(self):
        square = Square()
        self.play(Create(square), run_time=0.5)
        self.code_step("3-5", key="loop")
        self.wait(1)
        self.code_step("6")


class CodeStepFirst(SyncedScene):
    def construct(self):
        self.code_step("1")
        self.play(Create(Square()))
        self.code_step("2")


class CompositionTotals(SyncedScene):
    def construct(self):
        a, b, c = Square(), Square(), Circle()
        self.play(Succession(Create(a), Create(b)))
        self.play(LaggedStart(Create(a), Create(b), Create(c)))


class EmptyConstruct(SyncedScene):
    def construct(self):
        pass


class SubFramePlay(SyncedScene):
    def construct(self):
        self.play(Create(Square()), run_time=0.05)


class Boom(SyncedScene):
    def construct(self):
        self.play(Create(Square()))
        raise RuntimeError("boom")


class PlayNoAnims(SyncedScene):
    def construct(self):
        self.play()


class PlainScene(Scene):
    def construct(self):
        self.play(Create(Square()))


def record(scene_name):
    return record_scene(__name__, scene_name)


def plays(result):
    return [e for e in result["events"] if e["type"] != "code_step"]


def test_play_default_run_time_and_cumulative_t():
    result = record("PlainPlays")
    events = result["events"]
    assert result["error"] is None
    assert len(events) == 2
    assert events[0] == {"t": 0.0, "type": "play", "run_time": 1.0}
    assert events[1] == {"t": 1.0, "type": "play", "run_time": 1.0}
    assert result["duration"] == 2.0
    assert result["num_plays"] == 2


def test_wait_advances_clock():
    result = record("WaitTwo")
    assert result["events"] == [{"t": 0.0, "type": "wait", "run_time": 2.0, "frozen": True}]
    assert result["duration"] == 2.0


def test_explicit_run_time_and_code_step_ordering():
    result = record("MixedTimings")
    assert result["events"] == [
        {"t": 0.0, "type": "play", "run_time": 0.5},
        {"t": 0.5, "type": "code_step", "lines": "3-5", "key": "loop"},
        {"t": 0.5, "type": "wait", "run_time": 1.0, "frozen": True},
        {"t": 1.5, "type": "code_step", "lines": "6", "key": ""},
    ]
    assert result["duration"] == 1.5


def test_code_step_before_any_play_records_at_zero():
    result = record("CodeStepFirst")
    assert result["events"] == [
        {"t": 0.0, "type": "code_step", "lines": "1", "key": ""},
        {"t": 0.0, "type": "play", "run_time": 1.0},
        {"t": 1.0, "type": "code_step", "lines": "2", "key": ""},
    ]
    assert result["duration"] == 1.0


def test_succession_sums_and_lagged_start_maxes():
    result = record("CompositionTotals")
    run_times = [e["run_time"] for e in result["events"]]
    assert run_times == [2.0, 1.1]
    assert result["duration"] == 3.1


def test_determinism_two_runs_identical():
    first = record("PlainPlays")
    second = record("PlainPlays")
    assert first == second


def test_empty_construct_yields_zero_events():
    result = record("EmptyConstruct")
    assert result["events"] == []
    assert result["duration"] == 0.0
    assert result["error"] is None


def test_sub_frame_run_time_clamped_to_one_frame():
    result = record("SubFramePlay")
    assert result["events"] == [
        {"t": 0.0, "type": "play", "run_time": round(1 / 15, 9)},
    ]


def test_construct_error_captured_with_partial_events():
    result = record("Boom")
    assert result["error"] == "RuntimeError: boom"
    assert "boom" in result["traceback"]
    assert [e["run_time"] for e in result["events"]] == [1.0]


def test_play_with_no_animations_captured_as_error():
    result = record("PlayNoAnims")
    assert "no animations" in result["error"]
    assert result["events"] == []


def test_non_synced_scene_records_but_warns():
    with pytest.warns(UserWarning, match="does not subclass SyncedScene"):
        result = record("PlainScene")
    assert result["error"] is None
    assert [e["type"] for e in result["events"]] == ["play"]


def test_importing_synced_module_is_silent():
    script = "import sys; sys.path.insert(0, 'Animations'); import synced; print('IMPORTED')"
    proc = subprocess.run(
        [sys.executable, "-c", script], cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    assert proc.returncode == 0
    assert proc.stdout.strip() == "IMPORTED"


def test_cross_validation_with_cairo_skip_path(monkeypatch):
    from manim import config
    from manim.renderer.cairo_renderer import CairoRenderer

    monkeypatch.setattr(config, "dry_run", True)
    monkeypatch.setattr(config, "write_to_movie", False)
    monkeypatch.setattr(config, "progress_bar", "none")

    durations = []
    original_play = CairoRenderer.play

    def spy(self, scene, *args, **kwargs):
        original_play(self, scene, *args, **kwargs)
        durations.append(scene.duration)

    monkeypatch.setattr(CairoRenderer, "play", spy)

    scene = PlainPlays(renderer=CairoRenderer(skip_animations=True))
    scene.setup()
    scene.construct()
    scene.tear_down()

    result = record("PlainPlays")
    assert [e["run_time"] for e in plays(result)] == [round(d, 9) for d in durations]
