"""Map emission: recorder events + DISPLAY_CODE -> website sync JSON (plan card T5).

The website map must match the *video* timeline, not the raw run_time sums, so
every map time is frame-quantized per DESIGN.md §4.2:

- frozen static waits contribute ``int(duration / (1/fps))`` frames (floor rule,
  mirrors ``CairoRenderer.freeze_current_frame``),
- everything else contributes ``np.arange(0, duration, 1/fps).size`` frames
  (arange rule, mirrors ``Scene.play_internal``'s frame loop).

``code_step`` events consume no frames; their map time is the video time at the
moment they fired. Map entries are deduped on consecutive identical ``lines``,
and a final sentinel at the video's end is appended when the last code_step
differs from the first (lines reused from the last step — dedupe, no invention).
"""

from __future__ import annotations

import re

import numpy as np

_LINE_SPEC_RE = re.compile(r"^\d+(\s*-\s*\d+)?(\s*,\s*\d+(\s*-\s*\d+)?)*$")


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
                f'lines {lines!r} out of range: must reference lines 1..{n_lines} of DISPLAY_CODE'
            )


def quantized_code_steps(events: list[dict], fps: int = 15) -> tuple[list[tuple[str, float]], int]:
    """Frame-quantized ``(lines, time)`` pairs for code_step events, plus total video frames.

    No validation and no dedupe: this is also the raw material for the informational
    legacy-map comparison, where hand-written ``lines`` values must not raise.
    """
    steps: list[tuple[str, float]] = []
    frames = 0
    step = 1 / fps
    for event in events:
        if event["type"] == "code_step":
            steps.append((event["lines"], round(frames / fps, 4)))
        elif event.get("frozen"):
            frames += int(event["run_time"] / step)
        else:
            frames += np.arange(0, event["run_time"], step).size
    return steps, frames


def build_map(events: list[dict], code: list[str], fps: int = 15) -> list[dict]:
    """Build ``[{time, lines}]`` from code_step events, frame-quantized at ``fps``."""
    steps, frames = quantized_code_steps(events, fps)
    for lines, _ in steps:
        validate_lines(lines, code)
    entries: list[dict] = []
    for lines, time in steps:
        if not entries or entries[-1]["lines"] != lines:
            entries.append({"time": time, "lines": lines})
    if (
        entries
        and entries[-1]["lines"] != entries[0]["lines"]
        and frames / fps > entries[-1]["time"]
    ):
        entries.append({"time": round(frames / fps, 4), "lines": entries[-1]["lines"]})
    return entries


def build_payload(result: dict, scene_cls: type, category: str, fps: int = 15) -> dict:
    """Assemble the website map JSON payload for a recorded SyncedScene."""
    code = list(scene_cls.DISPLAY_CODE)
    if not code:
        raise MapEmissionError(
            f"{result['scene']}.DISPLAY_CODE is empty: declare the code the page displays"
        )
    entries = build_map(result["events"], code, fps)
    if not entries:
        raise MapEmissionError(
            f"{result['scene']} recorded no code_step events: call code_step(...) in construct()"
        )
    return {
        "video": f"Videos/{category}/{result['scene']}.webm",
        "code": code,
        "map": entries,
    }
