"""syncmap check: clean pass, injected drift detection, un-snapshotted warning (plan card T6)."""

import importlib
import shutil
from pathlib import Path

from tools.syncmap.cli import main, parse_inline_maps

MODULE = "tests.syncmap_drift_fixture"
FIXTURE_FILE = Path(__file__).resolve().parent / "syncmap_drift_fixture.py"


def _snapshot(timelines_dir: Path) -> int:
    return main(["snapshot", "--scene", MODULE, "DriftScene", "--out", str(timelines_dir)])


def _check(timelines_dir: Path) -> int:
    return main(["check", "--timelines", str(timelines_dir), "--modules", MODULE])


def test_committed_timeline_matching_live_is_clean(tmp_path, capsys):
    assert _snapshot(tmp_path) == 0
    assert _check(tmp_path) == 0
    out = capsys.readouterr().out
    assert "timelines: checked 1, clean 1, drifted 0" in out
    assert "DRIFT" not in out
    assert "OK: no drift" in out


def test_injected_drift_is_flagged_then_clean_after_revert(tmp_path, capsys):
    import tests.syncmap_drift_fixture as drift_mod

    assert _snapshot(tmp_path) == 0
    assert _check(tmp_path) == 0

    original = FIXTURE_FILE.read_bytes()
    assert b"self.wait(1)" in original
    FIXTURE_FILE.write_bytes(original.replace(b"self.wait(1)", b"self.wait(2.5)"))
    try:
        importlib.reload(drift_mod)
        capsys.readouterr()
        assert _check(tmp_path) == 1
        out = capsys.readouterr().out
        assert "DRIFT timeline DriftScene" in out
        assert "first differing event #1" in out
        assert "FAIL: drift found" in out
    finally:
        FIXTURE_FILE.write_bytes(original)
        importlib.reload(drift_mod)

    assert _check(tmp_path) == 0
    assert "OK: no drift" in capsys.readouterr().out


def test_missing_timelines_warn_but_exit_zero(tmp_path, capsys):
    empty = tmp_path / "none"
    empty.mkdir()
    assert _check(empty) == 0
    out = capsys.readouterr().out
    assert "no committed timeline" in out
    assert "  - DriftScene" in out
    assert "timelines: checked 0, clean 0, drifted 0" in out


def test_parse_inline_maps_extracts_entries():
    text = """
    const highlightMap = [
        { time: 0.0, lines: "11" },
        { time: 1.5, lines: "3-5" },
    ];
    createHighlightMap = [
        { time: 0.0, lines: "6", label: "x" },
    ];
    const highlightPairs = [
        { videoId: "code-video-create", codeBlockId: "b", mapVar: "createHighlightMap" },
    ];
    """
    maps = parse_inline_maps(text)
    assert set(maps) == {"highlightMap", "createHighlightMap"}
    assert maps["highlightMap"] == [(0.0, "11"), (1.5, "3-5")]
    assert maps["createHighlightMap"] == [(0.0, "6")]


def test_modules_scope_skips_other_modules_timelines(tmp_path, capsys):
    committed = (
        Path(__file__).resolve().parents[1] / "tools" / "syncmap" / "timelines" / "BinarySearch.json"
    )
    assert _snapshot(tmp_path) == 0
    shutil.copy(committed, tmp_path / "BinarySearch.json")
    assert _check(tmp_path) == 0
    out = capsys.readouterr().out
    assert "timelines: checked 1, clean 1, drifted 0" in out
    assert "BinarySearch" not in out
