"""syncmap map emission: line-spec validation, quantization, dedupe, CLI + Flask wiring (T5)."""

import json
import sys
from pathlib import Path

import pytest

from tools.syncmap.cli import main
from tools.syncmap.emit import MapEmissionError, build_map, validate_lines

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE = "tests.syncmap_cli_fixtures"


def test_validate_lines_accepts_real_specs():
    validate_lines("1", ["a"])
    validate_lines("1-2", ["a", "b"])
    validate_lines("1,3", ["a", "b", "c"])
    validate_lines(" 2 - 3 ", ["a", "b", "c"])


@pytest.mark.parametrize(
    "spec",
    ["0", "3", "2-1", "abc", "", "  ", "1;2", "1.5"],
)
def test_validate_lines_rejects_bad_specs(spec):
    with pytest.raises(MapEmissionError):
        validate_lines(spec, ["a", "b"])


def test_build_map_quantizes_to_frame_grid_and_sentinels():
    events = [
        {"t": 0.0, "type": "wait", "run_time": 0.7, "frozen": True},
        {"t": 0.7, "type": "code_step", "lines": "1", "key": "a"},
        {"t": 0.7, "type": "play", "run_time": 0.7},
        {"t": 1.4, "type": "code_step", "lines": "2", "key": "b"},
        {"t": 1.4, "type": "wait", "run_time": 1.0, "frozen": True},
    ]
    assert build_map(events, ["l1", "l2"], fps=15) == [
        {"time": 0.6667, "lines": "1"},
        {"time": 1.4, "lines": "2"},
        {"time": 2.4, "lines": "2"},
    ]


def test_build_map_dedupes_consecutive_identical_lines():
    events = [
        {"t": 0.0, "type": "code_step", "lines": "1", "key": ""},
        {"t": 0.0, "type": "code_step", "lines": "1", "key": "dup"},
        {"t": 0.0, "type": "play", "run_time": 1.0},
        {"t": 1.0, "type": "code_step", "lines": "2", "key": ""},
        {"t": 1.0, "type": "code_step", "lines": "2", "key": "dup"},
        {"t": 1.0, "type": "code_step", "lines": "1", "key": "back"},
        {"t": 1.0, "type": "play", "run_time": 1.0},
    ]
    assert build_map(events, ["a", "b"], fps=15) == [
        {"time": 0.0, "lines": "1"},
        {"time": 1.0, "lines": "2"},
        {"time": 1.0, "lines": "1"},
    ]


def test_map_cli_emits_valid_shape(tmp_path):
    code = main(
        [
            "map",
            MODULE,
            "FixtureSyncedScene",
            "--slug",
            "fx",
            "--category",
            "TestCat",
            "--out",
            str(tmp_path),
        ]
    )
    assert code == 0
    data = json.loads((tmp_path / "fx.json").read_text(encoding="utf-8"))
    assert set(data) == {"video", "code", "map"}
    assert data["video"] == "Videos/TestCat/FixtureSyncedScene.webm"
    assert data["code"] == ["def f(x):", "    return x + 1"]
    assert data["map"] == [
        {"time": 0.0, "lines": "1"},
        {"time": 1.0, "lines": "2"},
        {"time": 2.4667, "lines": "2"},
    ]


def test_map_cli_dedupes_on_real_scene(tmp_path):
    code = main(
        [
            "map",
            MODULE,
            "FixtureDedupeScene",
            "--slug",
            "dedupe",
            "--category",
            "TestCat",
            "--out",
            str(tmp_path),
        ]
    )
    assert code == 0
    data = json.loads((tmp_path / "dedupe.json").read_text(encoding="utf-8"))
    assert data["map"] == [
        {"time": 0.0, "lines": "1"},
        {"time": 1.0, "lines": "3"},
        {"time": 1.0, "lines": "1"},
    ]


def test_map_cli_fails_loudly_on_out_of_range_lines(tmp_path, capsys):
    code = main(
        [
            "map",
            MODULE,
            "FixtureOutOfRangeScene",
            "--slug",
            "bad",
            "--category",
            "TestCat",
            "--out",
            str(tmp_path),
        ]
    )
    assert code == 1
    assert "out of range" in capsys.readouterr().err
    assert not (tmp_path / "bad.json").exists()


def test_map_cli_rejects_non_synced_scene(tmp_path, capsys):
    code = main(
        [
            "map",
            MODULE,
            "FixtureScene",
            "--slug",
            "plain",
            "--category",
            "TestCat",
            "--out",
            str(tmp_path),
        ]
    )
    assert code == 1
    assert "not a SyncedScene" in capsys.readouterr().err
    assert not (tmp_path / "plain.json").exists()


def test_data_sync_page_serves_map_via_test_client():
    from flask import render_template_string

    website_dir = REPO_ROOT / "Website"
    if str(website_dir) not in sys.path:
        sys.path.insert(0, str(website_dir))
    from website import create_app

    page_template = (
        '{% extends "content.html" %} {% block title %} Sync Fixture {% endblock %}'
        "{% block main_content %}"
        '<div class="video-container" data-sync="/sync-fixture/map.json">'
        '<video id="code-video" controls></video>'
        "</div>"
        '<pre id="code-block" data-from-sync class="line-numbers language-python">'
        "<code></code></pre>"
        "{% endblock %} {% block scripts %}{% endblock %}"
    )
    payload = {
        "video": "Videos/TestCat/Fixture.webm",
        "code": ["def f():", "    pass"],
        "map": [{"time": 0.0, "lines": "1"}],
    }
    app = create_app()

    @app.route("/sync-fixture/page")
    def sync_fixture_page():
        return render_template_string(page_template, user=None)

    @app.route("/sync-fixture/map.json")
    def sync_fixture_map():
        return app.response_class(json.dumps(payload), mimetype="application/json")

    client = app.test_client()
    page = client.get("/sync-fixture/page")
    assert page.status_code == 200
    html = page.get_data(as_text=True)
    assert 'data-sync="/sync-fixture/map.json"' in html
    assert 'id="code-video"' in html and 'id="code-block"' in html

    map_response = client.get("/sync-fixture/map.json")
    assert map_response.status_code == 200
    assert map_response.get_json() == payload
