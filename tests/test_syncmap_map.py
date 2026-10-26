"""syncmap map emission: langs validation, per-language dedupe, combined JSON (C0M)."""

import json
import sys
from pathlib import Path

import pytest

from tools.syncmap.cli import main
from tools.syncmap.emit import (
    LANGS,
    MapEmissionError,
    build_combined_map,
    validate_langs,
    validate_lines,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE = "tests.syncmap_cli_fixtures"


def make_langs(**overrides):
    """A valid four-language library: every key resolves in every language."""
    langs = {
        "python": {"code": ["def f(x):", "    return x + 1", "    # tail"], "steps": {}},
        "c": {"code": ["int f(int x)", "{", "    return x + 1;", "}"], "steps": {}},
        "cpp": {"code": ["int f(int x)", "{", "    return x + 1;", "}"], "steps": {}},
        "java": {
            "code": ["static int f(int x)", "{", "    return x + 1;", "}"],
            "steps": {},
        },
    }
    for lang, steps in overrides.items():
        langs[lang] = {"code": list(langs[lang]["code"]), "steps": dict(steps)}
    return langs


def write_langs_file(langs_dir: Path, slug: str, langs: dict) -> Path:
    langs_dir.mkdir(parents=True, exist_ok=True)
    path = langs_dir / f"{slug}.json"
    path.write_text(json.dumps(langs), encoding="utf-8")
    return path


STANDARD_STEPS = {
    "python": {"enter": "1", "call": "2"},
    "c": {"enter": "1", "call": "3"},
    "cpp": {"enter": "1", "call": "3"},
    "java": {"enter": "1", "call": "3"},
}


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


def test_build_combined_map_shares_times_and_dedupes_per_language():
    events = [
        {"t": 0.0, "type": "code_step", "key": "a"},
        {"t": 0.0, "type": "code_step", "key": "a"},
        {"t": 0.0, "type": "play", "run_time": 1.0},
        {"t": 1.0, "type": "code_step", "key": "b"},
        {"t": 1.0, "type": "code_step", "key": "b"},
        {"t": 1.0, "type": "code_step", "key": "a"},
        {"t": 1.0, "type": "play", "run_time": 1.0},
    ]
    # python maps a and b to the SAME line: the whole sequence collapses to one entry.
    # java maps them to different lines: three entries, shared quantized times.
    langs = make_langs(python={"enter": "1", "call": "2"})
    langs["python"]["steps"] = {"a": "1", "b": "1"}
    langs["c"]["steps"] = {"a": "1", "b": "2"}
    langs["cpp"]["steps"] = {"a": "1", "b": "2"}
    langs["java"]["steps"] = {"a": "1", "b": "2"}
    maps = build_combined_map(events, langs, fps=15)
    assert maps["python"] == [{"time": 0.0, "lines": "1"}]
    assert maps["java"] == [
        {"time": 0.0, "lines": "1"},
        {"time": 1.0, "lines": "2"},
        {"time": 1.0, "lines": "1"},
    ]
    for lang in ("c", "cpp"):
        assert [entry["time"] for entry in maps[lang]] == [0.0, 1.0, 1.0]


def test_build_combined_map_sentinels_per_language():
    events = [
        {"t": 0.0, "type": "code_step", "key": "a"},
        {"t": 0.0, "type": "play", "run_time": 0.7},
        {"t": 0.7, "type": "code_step", "key": "b"},
        {"t": 0.7, "type": "wait", "run_time": 1.0, "frozen": True},
    ]
    langs = make_langs()
    langs["python"]["steps"] = {"a": "1", "b": "1"}
    langs["c"]["steps"] = {"a": "1", "b": "2"}
    langs["cpp"]["steps"] = {"a": "1", "b": "2"}
    langs["java"]["steps"] = {"a": "1", "b": "2"}
    maps = build_combined_map(events, langs, fps=15)
    # python never leaves line 1: no sentinel needed.
    assert maps["python"] == [{"time": 0.0, "lines": "1"}]
    # other languages end on line 2: a sentinel at the video's end
    # (11 play frames + 15 frozen frames = 26 frames / 15 fps).
    for lang in ("c", "cpp", "java"):
        assert maps[lang] == [
            {"time": 0.0, "lines": "1"},
            {"time": 0.7333, "lines": "2"},
            {"time": 1.7333, "lines": "2"},
        ]


def test_validate_langs_rejects_empty_key():
    with pytest.raises(MapEmissionError, match="empty key"):
        validate_langs(make_langs(**STANDARD_STEPS), [""], "FixtureSyncedScene", "fx")


def test_validate_langs_missing_key_names_language_and_key():
    langs = make_langs(**STANDARD_STEPS)
    del langs["java"]["steps"]["call"]
    with pytest.raises(MapEmissionError) as excinfo:
        validate_langs(langs, ["enter", "call"], "FixtureSyncedScene", "fx")
    message = str(excinfo.value)
    assert "FixtureSyncedScene" in message
    assert "'fx'" in message
    assert "language 'java'" in message
    assert "no step 'call'" in message


def test_validate_langs_out_of_range_names_language():
    langs = make_langs(**STANDARD_STEPS)
    langs["c"]["steps"]["call"] = "3-9"
    with pytest.raises(MapEmissionError) as excinfo:
        validate_langs(langs, ["enter", "call"], "FixtureSyncedScene", "fx")
    assert "language 'c'" in str(excinfo.value)
    assert "out of range" in str(excinfo.value)


def test_validate_langs_empty_code_names_language():
    langs = make_langs(**STANDARD_STEPS)
    langs["cpp"]["code"] = []
    with pytest.raises(MapEmissionError) as excinfo:
        validate_langs(langs, ["enter", "call"], "FixtureSyncedScene", "fx")
    assert "language 'cpp'" in str(excinfo.value)
    assert "empty code list" in str(excinfo.value)


def test_validate_langs_missing_language_names_schema():
    langs = make_langs(**STANDARD_STEPS)
    del langs["java"]
    with pytest.raises(MapEmissionError) as excinfo:
        validate_langs(langs, ["enter", "call"], "FixtureSyncedScene", "fx")
    message = str(excinfo.value)
    assert "language 'java' missing" in message
    assert '"python"' in message and '"java"' in message


def _map_cli(tmp_path: Path, slug: str, scene: str, langs: dict | None):
    langs_dir = tmp_path / "langs"
    if langs is not None:
        write_langs_file(langs_dir, slug, langs)
    return main(
        [
            "map",
            MODULE,
            scene,
            "--slug",
            slug,
            "--category",
            "TestCat",
            "--out",
            str(tmp_path / "sync"),
            "--langs",
            str(langs_dir),
        ]
    )


def test_map_cli_missing_langs_file_names_path_and_schema(tmp_path, capsys):
    code = _map_cli(tmp_path, "fx", "FixtureSyncedScene", None)
    assert code == 1
    err = capsys.readouterr().err
    assert "FixtureSyncedScene (slug 'fx')" in err
    assert "langs file missing" in err
    assert '"python": {"code"' in err  # schema hint in the error
    assert not (tmp_path / "sync" / "fx.json").exists()


def test_map_cli_emits_combined_shape_with_default(tmp_path):
    code = _map_cli(tmp_path, "fx", "FixtureSyncedScene", make_langs(**STANDARD_STEPS))
    assert code == 0
    data = json.loads((tmp_path / "sync" / "fx.json").read_text(encoding="utf-8"))
    assert set(data) == {"video", "default", "langs"}
    assert data["video"] == "Videos/TestCat/FixtureSyncedScene.webm"
    assert data["default"] == "python"
    assert set(data["langs"]) == set(LANGS)
    for lang in LANGS:
        assert set(data["langs"][lang]) == {"code", "map"}
    assert data["langs"]["python"]["code"] == ["def f(x):", "    return x + 1", "    # tail"]
    assert data["langs"]["python"]["map"] == [
        {"time": 0.0, "lines": "1"},
        {"time": 1.0, "lines": "2"},
        {"time": 2.4667, "lines": "2"},
    ]
    assert data["langs"]["c"]["map"] == [
        {"time": 0.0, "lines": "1"},
        {"time": 1.0, "lines": "3"},
        {"time": 2.4667, "lines": "3"},
    ]
    assert [e["time"] for e in data["langs"]["java"]["map"]] == [0.0, 1.0, 2.4667]


def test_map_cli_per_language_consecutive_dedupe(tmp_path):
    langs = make_langs()
    langs["python"]["steps"] = {"a": "1", "b": "3"}
    langs["c"]["steps"] = {"a": "1", "b": "1"}
    langs["cpp"]["steps"] = {"a": "1", "b": "1"}
    langs["java"]["steps"] = {"a": "1", "b": "3"}
    code = _map_cli(tmp_path, "dedupe", "FixtureDedupeScene", langs)
    assert code == 0
    data = json.loads((tmp_path / "sync" / "dedupe.json").read_text(encoding="utf-8"))
    # keys fired a,a,b,b,a: python keeps three distinct-line entries...
    assert data["langs"]["python"]["map"] == [
        {"time": 0.0, "lines": "1"},
        {"time": 1.0, "lines": "3"},
        {"time": 1.0, "lines": "1"},
    ]
    # ...while c collapses the whole sequence because every key maps to line 1.
    assert data["langs"]["c"]["map"] == [{"time": 0.0, "lines": "1"}]


def test_map_cli_fails_loudly_on_out_of_range_lines(tmp_path, capsys):
    langs = make_langs()
    langs["python"]["steps"] = {"done": "1"}
    langs["c"]["steps"] = {"done": "1"}
    langs["cpp"]["steps"] = {"done": "1"}
    langs["java"]["steps"] = {"done": "9"}
    code = _map_cli(tmp_path, "bad", "FixtureOutOfRangeScene", langs)
    assert code == 1
    err = capsys.readouterr().err
    assert "FixtureOutOfRangeScene (slug 'bad')" in err
    assert "language 'java'" in err
    assert "out of range" in err
    assert not (tmp_path / "sync" / "bad.json").exists()


def test_map_cli_rejects_non_synced_scene(tmp_path, capsys):
    code = _map_cli(tmp_path, "plain", "FixtureScene", make_langs(**STANDARD_STEPS))
    assert code == 1
    assert "not a SyncedScene" in capsys.readouterr().err
    assert not (tmp_path / "sync" / "plain.json").exists()


def test_data_sync_page_serves_combined_map_via_test_client():
    from flask import render_template_string

    website_dir = REPO_ROOT / "Website"
    if str(website_dir) not in sys.path:
        sys.path.insert(0, str(website_dir))
    from website import create_app

    page_template = (
        '{% extends "content.html" %} {% block title %} Sync Fixture {% endblock %}'
        "{% block main_content %}"
        '<div class="visualization-container" data-sync="/sync-fixture/map.json">'
        '<video id="code-video" controls></video>'
        "</div>"
        '<pre id="code-block" data-from-sync class="line-numbers language-python">'
        "<code></code></pre>"
        "{% endblock %} {% block scripts %}{% endblock %}"
    )
    payload = {
        "video": "Videos/TestCat/Fixture.webm",
        "default": "python",
        "langs": {
            lang: {"code": ["def f():", "    pass"], "map": [{"time": 0.0, "lines": "1"}]}
            for lang in LANGS
        },
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
