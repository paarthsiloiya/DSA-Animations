"""syncmap snapshot CLI: schema, byte-determinism, manifest error path (plan card T4)."""

import hashlib
import json
from pathlib import Path

import tests.syncmap_cli_fixtures as fixtures
from tools.syncmap.cli import main

MODULE = "tests.syncmap_cli_fixtures"


def test_snapshot_single_scene_writes_valid_json(tmp_path):
    out = tmp_path / "timelines"
    code = main(["snapshot", "--scene", MODULE, "FixtureScene", "--out", str(out)])
    assert code == 0
    data = json.loads((out / "FixtureScene.json").read_text(encoding="utf-8"))
    assert set(data) == {"scene", "module", "manim_version", "source_sha256", "events"}
    assert data["scene"] == "FixtureScene"
    assert data["module"] == MODULE
    expected_sha = hashlib.sha256(Path(fixtures.__file__).read_bytes()).hexdigest()
    assert data["source_sha256"] == expected_sha
    assert [e["run_time"] for e in data["events"]] == [1.0, 0.5]
    assert data["events"][1]["frozen"] is True


def test_snapshot_is_byte_deterministic(tmp_path):
    first = tmp_path / "a"
    second = tmp_path / "b"
    assert main(["snapshot", "--scene", MODULE, "FixtureScene", "--out", str(first)]) == 0
    assert main(["snapshot", "--scene", MODULE, "FixtureScene", "--out", str(second)]) == 0
    left = (first / "FixtureScene.json").read_bytes()
    right = (second / "FixtureScene.json").read_bytes()
    assert left == right


def test_all_mode_records_errors_in_manifest(tmp_path):
    out = tmp_path / "timelines"
    code = main(["snapshot", "--all", "--modules", MODULE, "--out", str(out)])
    assert code == 0
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["scenes"] == {
        "FixtureScene": MODULE,
        "FixtureSyncedScene": MODULE,
        "FixtureDedupeScene": MODULE,
        "FixtureOutOfRangeScene": MODULE,
    }
    assert [e["scene"] for e in manifest["errors"]] == ["FixtureBoom"]
    assert "fixture boom" in manifest["errors"][0]["error"]
    assert manifest["errors"][0]["traceback"]
    assert (out / "FixtureScene.json").exists()
    assert not (out / "FixtureBoom.json").exists()


def test_scene_mode_error_exits_nonzero_and_writes_nothing(tmp_path):
    out = tmp_path / "timelines"
    code = main(["snapshot", "--scene", MODULE, "FixtureBoom", "--out", str(out)])
    assert code == 1
    assert not (out / "FixtureBoom.json").exists()
    assert not (out / "manifest.json").exists()
