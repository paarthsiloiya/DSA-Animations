"""Combined four-language map emission (C0M v2).

The website map must match the *video* timeline, not the raw run_time sums, so
every map time is frame-quantized per DESIGN.md §4.2:

- frozen static waits contribute ``int(duration / (1/fps))`` frames (floor rule,
  mirrors ``CairoRenderer.freeze_current_frame``),
- everything else contributes ``np.arange(0, duration, 1/fps).size`` frames
  (arange rule, mirrors ``Scene.play_internal``'s frame loop).

``code_step`` events carry semantic step keys (language-agnostic slugs). Each
language's line numbers live in ``tools/syncmap/langs/<slug>.json``; the emitted
combined JSON shares one frame-quantized time sequence across all four
languages, and only the ``lines`` values (and their per-language consecutive
dedupe) differ. A final sentinel at the video's end is appended per language
when that language's last step differs from its first (lines reused from the
last step — dedupe, no invention).
"""

from __future__ import annotations

import re

import numpy as np

_LINE_SPEC_RE = re.compile(r"^\d+(\s*-\s*\d+)?(\s*,\s*\d+(\s*-\s*\d+)?)*$")

LANGS = ("python", "c", "cpp", "java")

LANGS_SCHEMA_HINT = (
    '{"python": {"code": ["...lines..."], "steps": {"<key>": "4-8"}}, '
    '"c": {"code": [...], "steps": {...}}, "cpp": {...}, "java": {...}}'
)


class MapEmissionError(ValueError):
    """Raised when a map cannot be emitted faithfully (bad lines spec, empty scene, ...)."""


def parse_line_spec(lines: str) -> list[tuple[int, int]]:
    """Parse a Prism ``data-line`` spec ("6", "3-5", "6,9-11") into inclusive (start, end) pairs."""
    if not isinstance(lines, str) or not lines.strip():
        raise MapEmissionError(f'invalid lines spec {lines!r}: expected "6", "3-5" or "6,9-11"')
    if not _LINE_SPEC_RE.match(lines.strip()):
        raise MapEmissionError(f'invalid lines spec {lines!r}: expected "6", "3-5" or "6,9-11"')
    pairs = []
    for part in lines.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = (int(token.strip()) for token in part.split("-", 1))
        else:
            start = end = int(part)
        pairs.append((start, end))
    return pairs


def validate_lines(lines: str, code: list[str]) -> None:
    """Fail loudly unless every number in ``lines`` references a real line of ``code``."""
    n_lines = len(code)
    for start, end in parse_line_spec(lines):
        if start < 1 or end < start or end > n_lines:
            raise MapEmissionError(
                f'lines {lines!r} out of range: must reference lines 1..{n_lines} of the code list'
            )


def quantized_code_steps(events: list[dict], fps: int = 15) -> tuple[list[tuple[str, float]], int]:
    """Frame-quantized ``(key, time)`` pairs for code_step events, plus total video frames.

    No validation and no dedupe: this is also the raw material for the informational
    legacy-map comparison, where hand-written step values must not raise.
    """
    steps: list[tuple[str, float]] = []
    frames = 0
    step = 1 / fps
    for event in events:
        if event["type"] == "code_step":
            steps.append((event["key"], round(frames / fps, 4)))
        elif event.get("frozen"):
            frames += int(event["run_time"] / step)
        else:
            frames += np.arange(0, event["run_time"], step).size
    return steps, frames


def validate_langs(langs: dict, emitted_keys: list[str], scene: str, slug: str) -> None:
    """Fail loudly unless every language can resolve every emitted key to real lines.

    Errors name the scene, slug, language and key so a bad langs file is
    immediately actionable. No partial emission can happen past this gate.
    """
    if not isinstance(langs, dict):
        raise MapEmissionError(
            f"{scene} (slug {slug!r}): langs file must be an object: {LANGS_SCHEMA_HINT}"
        )
    if "" in emitted_keys:
        raise MapEmissionError(
            f"{scene} (slug {slug!r}): code_step was called with an empty key — "
            f"every code_step needs a semantic key (e.g. 'partition-loop')"
        )
    for lang in LANGS:
        entry = langs.get(lang)
        if not isinstance(entry, dict):
            raise MapEmissionError(
                f"{scene} (slug {slug!r}): language {lang!r} missing from langs file; "
                f"expected schema: {LANGS_SCHEMA_HINT}"
            )
        code = entry.get("code")
        if not isinstance(code, list) or not code:
            raise MapEmissionError(
                f"{scene} (slug {slug!r}): language {lang!r} has an empty code list"
            )
        steps = entry.get("steps")
        if not isinstance(steps, dict):
            raise MapEmissionError(
                f"{scene} (slug {slug!r}): language {lang!r} has no steps object; "
                f"expected schema: {LANGS_SCHEMA_HINT}"
            )
        for key in emitted_keys:
            if key not in steps:
                raise MapEmissionError(
                    f"{scene} (slug {slug!r}): language {lang!r} has no step {key!r} "
                    f"(key emitted by code_step but absent from this language's steps)"
                )
        for key, lines in steps.items():
            try:
                validate_lines(lines, code)
            except MapEmissionError as e:
                raise MapEmissionError(
                    f"{scene} (slug {slug!r}): language {lang!r} step {key!r}: {e}"
                ) from e


def build_lang_map(steps: list[tuple[str, float]], frames: int, lang: dict, fps: int) -> list[dict]:
    """One language's ``[{time, lines}]``: keys resolved to lines, consecutive dedupe, sentinel."""
    entries: list[dict] = []
    for key, time in steps:
        lines = lang["steps"][key]
        if not entries or entries[-1]["lines"] != lines:
            entries.append({"time": time, "lines": lines})
    if (
        entries
        and entries[-1]["lines"] != entries[0]["lines"]
        and frames / fps > entries[-1]["time"]
    ):
        entries.append({"time": round(frames / fps, 4), "lines": entries[-1]["lines"]})
    return entries


def build_combined_map(
    events: list[dict], langs: dict, fps: int = 15
) -> dict[str, list[dict]]:
    """Per-language maps sharing one frame-quantized time sequence.

    Times are identical across languages; only ``lines`` (and their per-language
    consecutive dedupe) differ.
    """
    steps, frames = quantized_code_steps(events, fps)
    return {lang: build_lang_map(steps, frames, langs[lang], fps) for lang in LANGS}


def build_combined_payload(
    result: dict,
    scene_cls: type,
    category: str,
    langs: dict,
    slug: str,
    fps: int = 15,
) -> dict:
    """Assemble the combined four-language website map JSON for a recorded SyncedScene."""
    scene = result["scene"]
    emitted_keys = [event["key"] for event in result["events"] if event["type"] == "code_step"]
    if not emitted_keys:
        raise MapEmissionError(
            f"{scene} recorded no code_step events: call code_step(key) in construct()"
        )
    validate_langs(langs, emitted_keys, scene, slug)
    maps = build_combined_map(result["events"], langs, fps)
    return {
        "video": f"Videos/{category}/{scene}.webm",
        "default": "python",
        "langs": {
            lang: {"code": list(langs[lang]["code"]), "map": maps[lang]} for lang in LANGS
        },
    }
