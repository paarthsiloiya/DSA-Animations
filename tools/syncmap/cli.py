"""snapshot CLI: record Scene timelines into byte-comparable JSON files (plan card T4).

The timelines under ``tools/syncmap/timelines/`` are the behavior-preservation
oracle for the Phase 3 refactor: identical code must yield byte-identical
files. Determinism rules (DESIGN.md §7.1): ``sort_keys=True``,
``separators=(",", ":")``, LF endings, trailing newline, no timestamps, no
environment-dependent values anywhere in timeline files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import traceback
from pathlib import Path

import manim
from manim import Scene

from .emit import MapEmissionError, build_payload, quantized_code_steps
from .recorder import ANIMATIONS_DIR, import_scene_module, record_scene

REPO_ROOT = Path(__file__).resolve().parents[2]
TIMELINES_DIR = Path(__file__).resolve().parent / "timelines"
STATIC_SYNC_DIR = REPO_ROOT / "Website" / "website" / "static" / "sync"
EXCLUDED_ANIMATION_MODULES = {"env_config.py", "synced.py", "__init__.py"}


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(_serialize_json(payload))


def _serialize_json(payload) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def _record_cached(cache: dict, module_dotted: str, scene_name: str) -> dict:
    key = (module_dotted, scene_name)
    if key not in cache:
        cache[key] = record_scene(module_dotted, scene_name)
    return cache[key]


def _synced_scene_base() -> type:
    if str(ANIMATIONS_DIR) not in sys.path:
        sys.path.insert(0, str(ANIMATIONS_DIR))
    from synced import SyncedScene

    return SyncedScene


def _source_sha256(module) -> str:
    return hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()


def default_scene_modules() -> list[str]:
    """Every scene module in Animations/, as dotted names (files are imported exactly as named)."""
    stems = sorted(
        path.stem for path in ANIMATIONS_DIR.glob("*.py") if path.name not in EXCLUDED_ANIMATION_MODULES
    )
    return [f"Animations.{stem}" for stem in stems]


def scene_classes(module) -> list[type]:
    """Scene subclasses defined in ``module`` (definition order), skipping imported bases."""
    found = []
    for obj in vars(module).values():
        if (
            isinstance(obj, type)
            and issubclass(obj, Scene)
            and obj is not Scene
            and obj.__module__ == module.__name__
        ):
            found.append(obj)
    return found


def _timeline_payload(result: dict, source_sha256: str) -> dict:
    return {
        "scene": result["scene"],
        "module": result["module"],
        "manim_version": result["manim_version"],
        "source_sha256": source_sha256,
        "events": result["events"],
    }


def snapshot_one(module_dotted: str, scene_name: str, out_dir: Path) -> int:
    """Record a single scene and write ``<out_dir>/<Scene>.json``. Returns exit code."""
    result = record_scene(module_dotted, scene_name)
    if result["error"] is not None:
        print(f"error recording {scene_name}: {result['error']}", file=sys.stderr)
        return 1
    module = import_scene_module(module_dotted)
    path = out_dir / f"{scene_name}.json"
    _write_json(path, _timeline_payload(result, _source_sha256(module)))
    print(f"wrote {path} ({len(result['events'])} events, {result['duration']}s)")
    return 0


def snapshot_all(modules: list[str], out_dir: Path, batch: int) -> dict:
    """Record every scene across ``modules``; write timelines + manifest. Never aborts."""
    out_dir.mkdir(parents=True, exist_ok=True)
    targets: list[tuple[str, type, str]] = []
    errors: list[dict] = []

    for module_dotted in modules:
        try:
            module = import_scene_module(module_dotted)
            sha = _source_sha256(module)
            for cls in scene_classes(module):
                targets.append((module_dotted, cls, sha))
        except Exception as e:  # noqa: BLE001 — a broken module must not kill the batch
            errors.append(
                {
                    "module": module_dotted,
                    "scene": None,
                    "error": f"{type(e).__name__}: {e}",
                    "traceback": traceback.format_exc(),
                }
            )

    scenes: dict[str, str] = {}
    written = 0
    for i, (module_dotted, cls, sha) in enumerate(targets, start=1):
        scene_name = cls.__name__
        if scene_name in scenes:
            errors.append(
                {
                    "module": module_dotted,
                    "scene": scene_name,
                    "error": "duplicate scene name (already written this run)",
                    "traceback": None,
                }
            )
            continue
        try:
            result = record_scene(module_dotted, scene_name)
        except Exception as e:  # noqa: BLE001 — per-scene isolation for the batch
            errors.append(
                {
                    "module": module_dotted,
                    "scene": scene_name,
                    "error": f"{type(e).__name__}: {e}",
                    "traceback": traceback.format_exc(),
                }
            )
            continue
        if result["error"] is not None:
            errors.append(
                {
                    "module": module_dotted,
                    "scene": scene_name,
                    "error": result["error"],
                    "traceback": result["traceback"],
                }
            )
        else:
            _write_json(out_dir / f"{scene_name}.json", _timeline_payload(result, sha))
            scenes[scene_name] = module_dotted
            written += 1
        if i % batch == 0 or i == len(targets):
            print(f"[{i}/{len(targets)}] {written} timelines, {len(errors)} errors so far")

    manifest = {
        "scenes": scenes,
        "generated": {
            "manim_version": manim.__version__,
            "scenes": len(scenes),
            "errors": len(errors),
        },
        "errors": errors,
    }
    _write_json(out_dir / "manifest.json", manifest)
    return manifest


def map_scene(
    module_dotted: str, scene_name: str, slug: str, category: str, fps: int, out_dir: Path
) -> int:
    """Emit the website sync JSON for a SyncedScene. Returns exit code."""
    synced_base = _synced_scene_base()
    module = import_scene_module(module_dotted)
    scene_cls = getattr(module, scene_name, None)
    if not (isinstance(scene_cls, type) and issubclass(scene_cls, synced_base)):
        print(
            f"error: {module_dotted}.{scene_name} is not a SyncedScene; add "
            f"'from synced import SyncedScene', subclass it, declare DISPLAY_CODE, and call "
            f"code_step(...) where the demonstrated code line changes",
            file=sys.stderr,
        )
        return 1
    result = record_scene(module_dotted, scene_name)
    if result["error"] is not None:
        print(f"error recording {scene_name}: {result['error']}", file=sys.stderr)
        return 1
    payload = build_payload(result, scene_cls, category, fps)
    path = out_dir / f"{slug}.json"
    _write_json(path, payload)
    print(f"wrote {path} ({len(payload['map'])} map entries)")
    return 0


def _first_event_diff(committed: list, live: list) -> str:
    for i, (a, b) in enumerate(zip(committed, live)):
        if a != b:
            return (
                f"first differing event #{i}: "
                f"committed {json.dumps(a, sort_keys=True)} "
                f"live {json.dumps(b, sort_keys=True)}"
            )
    shorter = min(len(committed), len(live))
    extra = committed[shorter:] or live[shorter:]
    side = "committed" if committed[shorter:] else "live"
    return f"event count {len(committed)} -> {len(live)} (first {side}-only event: {json.dumps(extra[0], sort_keys=True)})"


def check_timelines(
    timelines_dir: Path, record_cache: dict, scope: set[str] | None
) -> tuple[list, list]:
    """Re-record every in-scope committed timeline and byte-compare the re-serialized JSON."""
    clean, drifted = [], []
    for path in sorted(timelines_dir.glob("*.json")):
        if path.name == "manifest.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        scene, module = data["scene"], data["module"]
        if scope is not None and module not in scope:
            continue
        result = _record_cached(record_cache, module, scene)
        if result["error"] is not None:
            drifted.append(scene)
            print(f"DRIFT timeline {scene}: live recording failed: {result['error']}")
            continue
        module_obj = import_scene_module(module)
        live = _serialize_json(_timeline_payload(result, _source_sha256(module_obj)))
        if live == path.read_text(encoding="utf-8"):
            clean.append(scene)
            continue
        drifted.append(scene)
        if data["events"] == result["events"]:
            print(
                f"DRIFT timeline {scene}: source changed but events identical "
                f"(stale source_sha256) — regenerate with 'snapshot'"
            )
        else:
            print(f"DRIFT timeline {scene}: {_first_event_diff(data['events'], result['events'])}")
    return clean, drifted


def check_maps(
    sync_dir: Path, lookup: dict, record_cache: dict, scope: set[str] | None
) -> tuple[list, list]:
    """Re-derive every committed map (in memory only) and byte-compare it."""
    clean, drifted = [], []
    for path in sorted(sync_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        match = re.match(r"Videos/([^/]+)/(.+)\.webm$", data.get("video", ""))
        if not match:
            drifted.append(path.stem)
            print(f"DRIFT map {path.stem}: malformed video field {data.get('video')!r}")
            continue
        category, scene = match.group(1), match.group(2)
        if scene not in lookup:
            if scope is None:
                drifted.append(path.stem)
                print(f"DRIFT map {path.stem}: scene {scene!r} not found in enumerated modules")
            continue
        module, scene_cls = lookup[scene]
        result = _record_cached(record_cache, module, scene)
        if result["error"] is not None:
            drifted.append(path.stem)
            print(f"DRIFT map {path.stem}: live recording of {scene} failed: {result['error']}")
            continue
        try:
            live = _serialize_json(build_payload(result, scene_cls, category))
        except MapEmissionError as e:
            drifted.append(path.stem)
            print(f"DRIFT map {path.stem}: cannot re-derive ({e})")
            continue
        if live == path.read_text(encoding="utf-8"):
            clean.append(path.stem)
            continue
        drifted.append(path.stem)
        if data.get("map") == json.loads(live)["map"]:
            print(f"DRIFT map {path.stem}: code/video changed but map identical — regenerate")
        else:
            print(
                f"DRIFT map {path.stem}: map entries differ "
                f"({len(data.get('map', []))} committed vs "
                f"{len(json.loads(live)['map'])} live)"
            )
    return clean, drifted


_INLINE_MAP_RE = re.compile(
    r"(?:const\s+|let\s+|var\s+)?(\w*[Hh]ighlightMap)\s*=\s*\[(.*?)\]", re.DOTALL
)
_MAP_ENTRY_RE = re.compile(r"\{\s*time:\s*([0-9]+(?:\.[0-9]+)?)\s*,\s*lines:\s*\"([^\"]*)\"")
_VIDEO_ID_RE = re.compile(
    r"<video[^>]*id=\"([^\"]+)\"[^>]*>.*?Videos/[^/\"]+/([^\".]+)\.webm", re.DOTALL
)
_HIGHLIGHT_PAIRS_RE = re.compile(
    r"videoId:\s*\"([^\"]+)\",\s*codeBlockId:\s*\"[^\"]+\",\s*mapVar:\s*\"([^\"]+)\""
)


def parse_inline_maps(template_text: str) -> dict[str, list[tuple[float, str]]]:
    """Extract every inline JS map: ``{map_var: [(time, lines), ...]}``."""
    maps = {}
    for match in _INLINE_MAP_RE.finditer(template_text):
        entries = [
            (float(time), lines) for time, lines in _MAP_ENTRY_RE.findall(match.group(2))
        ]
        if entries:
            maps[match.group(1)] = entries
    return maps


def check_legacy(templates_dir: Path, lookup: dict, record_cache: dict) -> dict:
    """Informational: compare hand-eyeballed inline maps against live code_step times."""
    stats = {"pages": 0, "comparable": 0, "not_comparable": 0, "warnings": 0}
    synced_base = _synced_scene_base()
    for path in sorted(templates_dir.rglob("*.html")):
        maps = parse_inline_maps(path.read_text(encoding="utf-8"))
        if not maps:
            continue
        stats["pages"] += 1
        videos = dict(_VIDEO_ID_RE.findall(path.read_text(encoding="utf-8")))
        pairs = _HIGHLIGHT_PAIRS_RE.findall(path.read_text(encoding="utf-8"))
        if len(videos) == 1:
            scene = next(iter(videos.values()))
            bindings = [(map_var, scene) for map_var in maps]
        elif pairs:
            bindings = [
                (map_var, videos.get(video_id))
                for video_id, map_var in pairs
                if map_var in maps
            ]
        else:
            bindings = [(map_var, None) for map_var in maps]

        for map_var, scene in bindings:
            if scene not in lookup or not issubclass(lookup[scene][1], synced_base):
                stats["not_comparable"] += 1
                continue
            module, _ = lookup[scene]
            result = _record_cached(record_cache, module, scene)
            steps, _frames = quantized_code_steps(result["events"])
            if not steps:
                stats["not_comparable"] += 1
                continue
            stats["comparable"] += 1
            machine = {}
            for lines, t in steps:
                machine.setdefault(lines, []).append(t)
            for inline_time, lines in maps[map_var]:
                live_times = machine.get(lines)
                if not live_times:
                    continue
                if min(abs(inline_time - t) for t in live_times) > 1.0:
                    stats["warnings"] += 1
                    print(
                        f"legacy warning: {path.name} {map_var}: lines {lines!r} at "
                        f"t={inline_time} but live code_step says {live_times} (>1.0s apart)"
                    )
    return stats


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tools.syncmap", description="Record Manim scene timelines without rendering."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot", help="record scene timelines as deterministic JSON")
    group = snap.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--scene",
        nargs=2,
        metavar=("MODULE", "SCENE"),
        help="dotted module path and scene class, e.g. Animations.Trees TreeBFS",
    )
    group.add_argument("--all", action="store_true", help="snapshot every scene in every module")
    snap.add_argument("--batch", type=int, default=10, help="progress line every N scenes (--all)")
    snap.add_argument(
        "--modules",
        help="comma-separated dotted modules to enumerate instead of all of Animations/ (--all)",
    )
    snap.add_argument(
        "--out",
        default=None,
        help=f"output directory (default: {TIMELINES_DIR})",
    )
    mp = sub.add_parser("map", help="emit the website sync JSON for a SyncedScene")
    mp.add_argument("module", help="dotted module path, e.g. Animations.SearchingAlgorithms")
    mp.add_argument("scene", help="scene class name")
    mp.add_argument("--slug", required=True, help="map filename slug, e.g. linear-search")
    mp.add_argument("--category", required=True, help="video category, e.g. SearchingAlgorithms")
    mp.add_argument("--fps", type=int, default=15, help="render fps the webm was produced at")
    mp.add_argument("--out", default=None, help=f"output directory (default: {STATIC_SYNC_DIR})")
    chk = sub.add_parser("check", help="detect drift between live scenes and committed artifacts")
    chk.add_argument(
        "--legacy",
        action="store_true",
        help="also report hand-eyeballed inline template maps that drift (informational)",
    )
    chk.add_argument(
        "--timelines",
        default=None,
        help=f"committed timelines directory (default: {TIMELINES_DIR})",
    )
    chk.add_argument(
        "--sync", default=None, help=f"committed maps directory (default: {STATIC_SYNC_DIR})"
    )
    chk.add_argument(
        "--modules",
        help="comma-separated dotted modules to scope the check to (default: all of Animations/)",
    )
    return parser


def run_check(
    modules: list[str],
    timelines_dir: Path,
    sync_dir: Path,
    templates_dir: Path,
    legacy: bool,
    scope: set[str] | None = None,
) -> int:
    """Re-derive live timelines/maps and compare with committed ones. 0 = no drift."""
    record_cache: dict = {}
    lookup: dict[str, tuple[str, type]] = {}
    for module_dotted in modules:
        try:
            module = import_scene_module(module_dotted)
        except Exception as e:  # noqa: BLE001 — enumeration must not kill the check
            print(f"warning: cannot enumerate {module_dotted}: {type(e).__name__}: {e}")
            continue
        for cls in scene_classes(module):
            lookup.setdefault(cls.__name__, (module_dotted, cls))

    clean_t, drifted_t = check_timelines(timelines_dir, record_cache, scope)

    committed = {
        path.stem for path in timelines_dir.glob("*.json") if path.name != "manifest.json"
    }
    missing = sorted(set(lookup) - committed)
    if missing:
        print(
            f"warning: {len(missing)} scene(s) have no committed timeline "
            f"(run 'snapshot --all'):"
        )
        for name in missing:
            print(f"  - {name}")

    clean_m, drifted_m = (
        check_maps(sync_dir, lookup, record_cache, scope) if sync_dir.is_dir() else ([], [])
    )

    if legacy:
        legacy_stats = check_legacy(templates_dir, lookup, record_cache)
    else:
        legacy_stats = None

    print()
    print(f"timelines: checked {len(clean_t) + len(drifted_t)}, clean {len(clean_t)}, drifted {len(drifted_t)}")
    print(f"maps:      checked {len(clean_m) + len(drifted_m)}, clean {len(clean_m)}, drifted {len(drifted_m)}")
    if legacy_stats is not None:
        print(
            f"legacy:    {legacy_stats['pages']} pages with inline maps, "
            f"{legacy_stats['comparable']} comparable, {legacy_stats['not_comparable']} not "
            f"comparable, {legacy_stats['warnings']} warning(s)"
        )
    if drifted_t or drifted_m:
        print("FAIL: drift found (regenerate with snapshot/map, then re-run check)")
        return 1
    print("OK: no drift")
    return 0


def main(argv: list[str] | None = None) -> int:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    args = build_parser().parse_args(argv)
    if args.command == "check":
        timelines_dir = Path(args.timelines) if args.timelines else TIMELINES_DIR
        sync_dir = Path(args.sync) if args.sync else STATIC_SYNC_DIR
        templates_dir = REPO_ROOT / "Website" / "website" / "templates"
        if args.modules:
            modules = [m.strip() for m in args.modules.split(",") if m.strip()]
            scope = set(modules)
        else:
            modules = default_scene_modules()
            scope = None
        return run_check(modules, timelines_dir, sync_dir, templates_dir, args.legacy, scope)
    if args.command == "map":
        out_dir = Path(args.out) if args.out else STATIC_SYNC_DIR
        try:
            return map_scene(args.module, args.scene, args.slug, args.category, args.fps, out_dir)
        except MapEmissionError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        except Exception as e:  # noqa: BLE001 — CLI boundary: report, never crash
            print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
            return 1
    out_dir = Path(args.out) if args.out else TIMELINES_DIR
    if args.all:
        modules = (
            [m.strip() for m in args.modules.split(",") if m.strip()]
            if args.modules
            else default_scene_modules()
        )
        manifest = snapshot_all(modules, out_dir, max(args.batch, 1))
        print(
            f"manifest: {out_dir / 'manifest.json'} "
            f"({len(manifest['scenes'])} scenes, {len(manifest['errors'])} errors)"
        )
        for error in manifest["errors"]:
            print(f"  error: {error['scene'] or error['module']}: {error['error']}")
        return 0
    try:
        return snapshot_one(args.scene[0], args.scene[1], out_dir)
    except Exception as e:  # noqa: BLE001 — CLI boundary: report, never crash with a traceback
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
