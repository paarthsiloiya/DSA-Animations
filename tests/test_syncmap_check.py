"""syncmap check: clean pass, injected drift detection, un-snapshotted warning (plan card T6).

Map drift (C0M): per-language re-derivation with messages naming the offending
language.
"""

import importlib
import json
import shutil
from pathlib import Path

from tools.syncmap.cli import main, parse_inline_maps

MODULE = "tests.syncmap_drift_fixture"
FIXTURE_MODULE = "tests.syncmap_cli_fixtures"
FIXTURE_FILE = Path(__file__).resolve().parent / "syncmap_drift_fixture.py"

LANGS = {
    "python": {"code": ["def f(x):", "    return x + 1", "    # tail"], "steps": {"enter": "1", "call": "2"}},
    "c": {"code": ["int f(int x)", "{", "    return x + 1;", "}"], "steps": {"enter": "1", "call": "3"}},
    "cpp": {"code": ["int f(int x)", "{", "    return x + 1;", "}"], "steps": {"enter": "1", "call": "3"}},
    "java": {"code": ["static int f(int x)", "{", "    return x + 1;", "}"], "steps": {"enter": "1", "call": "3"}},
}


def _snapshot(timelines_dir: Path) -> int:
    return main(["snapshot", "--scene", MODULE, "DriftScene", "--out", str(timelines_dir)])


def _check(timelines_dir: Path) -> int:
    return main(["check", "--timelines", str(timelines_dir), "--modules", MODULE])


def _map_fixture(tmp_path: Path) -> Path:
    langs_dir = tmp_path / "langs"
    langs_dir.mkdir(parents=True, exist_ok=True)
    (langs_dir / "fx.json").write_text(json.dumps(LANGS), encoding="utf-8")
    assert (
        main(
            [
                "map",
                FIXTURE_MODULE,
                "FixtureSyncedScene",
                "--slug",
                "fx",
                "--category",
                "TestCat",
                "--out",
                str(tmp_path / "sync"),
                "--langs",
                str(langs_dir),
            ]
        )
        == 0
    )
    return tmp_path / "sync" / "fx.json"


def _check_maps(tmp_path: Path) -> int:
    empty_timelines = tmp_path / "timelines"
    empty_timelines.mkdir(exist_ok=True)
    return main(
        [
            "check",
            "--timelines",
            str(empty_timelines),
            "--sync",
            str(tmp_path / "sync"),
            "--langs",
            str(tmp_path / "langs"),
            "--modules",
            FIXTURE_MODULE,
        ]
    )


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


def test_committed_combined_map_matching_live_is_clean(tmp_path, capsys):
    assert _map_fixture(tmp_path).is_file()
    assert _check_maps(tmp_path) == 0
    out = capsys.readouterr().out
    assert "maps:      checked 1, clean 1, drifted 0" in out
    assert "DRIFT" not in out
    assert "OK: no drift" in out


def test_drift_in_one_language_names_that_language(tmp_path, capsys):
    map_path = _map_fixture(tmp_path)
    data = json.loads(map_path.read_text(encoding="utf-8"))
    committed_java = data["langs"]["java"]["map"]
    assert len(committed_java) == 3
    data["langs"]["java"]["map"] = committed_java[:2]  # simulate a stale, shorter java map
    map_path.write_text(json.dumps(data), encoding="utf-8")

    assert _check_maps(tmp_path) == 1
    out = capsys.readouterr().out
    assert "DRIFT map fx: language 'java' differs (2 committed vs 3 live)" in out
    assert "language 'python'" not in out
    assert "language 'c'" not in out
    assert "language 'cpp'" not in out
    assert "FAIL: drift found" in out


def test_check_reports_missing_langs_file_for_committed_map(tmp_path, capsys):
    assert _map_fixture(tmp_path).is_file()
    (tmp_path / "langs" / "fx.json").unlink()
    assert _check_maps(tmp_path) == 1
    out = capsys.readouterr().out
    assert "DRIFT map fx: cannot re-derive" in out
    assert "langs file missing" in out
