#!/usr/bin/env python3
"""
MP4 to WebM converter for the AlgoViz website.

Converts manim's 480p15 renders in Animations/media/videos/<Category>/ to
Website/website/static/Videos/<Category>/<Scene>.webm. Encode settings reuse
what was probed from the existing site videos (VP9 video, no audio - manim
renders are silent, so -an matches the site's streams).

Category names map as-is from media/videos to static/Videos unless registered
in CATEGORY_ALIASES. Existing outputs are never overwritten unless --force.

Paths are resolved from this file's location, so the tool works from any
working directory.
"""

import argparse
import subprocess
import sys
from pathlib import Path

from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
MEDIA_ROOT = ROOT / "Animations" / "media" / "videos"
DEST_ROOT = ROOT / "Website" / "website" / "static" / "Videos"
QUALITY_DIR = "480p15"

CATEGORY_ALIASES: dict[str, str] = {"Stack-Queue": "StackAndQueue", "SortingAlgoritms": "SortingAlgorithms"}

FFMPEG_VIDEO_ARGS = ["-c:v", "libvpx-vp9", "-crf", "33", "-b:v", "0", "-an"]


def find_source_files(categories: list[str] | None, scene: str | None) -> list[tuple[str, Path]]:
    category_dirs = []
    if categories:
        for name in categories:
            category_dir = MEDIA_ROOT / name
            if category_dir.is_dir():
                category_dirs.append(category_dir)
            else:
                print(f"category not found: {name}")
    else:
        category_dirs = sorted(path for path in MEDIA_ROOT.iterdir() if path.is_dir())

    sources: list[tuple[str, Path]] = []
    for category_dir in category_dirs:
        quality_dir = category_dir / QUALITY_DIR
        if not quality_dir.is_dir():
            continue
        for mp4 in sorted(quality_dir.glob("*.mp4")):
            if scene and mp4.stem != scene:
                continue
            sources.append((category_dir.name, mp4))
    return sources


def destination_for(category: str, source: Path) -> Path:
    site_category = CATEGORY_ALIASES.get(category, category)
    return DEST_ROOT / site_category / f"{source.stem}.webm"


def convert_file(source: Path, destination: Path) -> bool:
    command = ["ffmpeg", "-y", "-i", source.as_posix(), *FFMPEG_VIDEO_ARGS, destination.as_posix()]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode == 0 and destination.is_file():
        return True
    destination.unlink(missing_ok=True)
    stderr_tail = result.stderr.strip().splitlines()
    print(f"FAILED: {source.as_posix()}")
    print(f"  {stderr_tail[-1] if stderr_tail else 'ffmpeg produced no error output'}")
    return False


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert manim 480p15 MP4s to WebM for the website (VP9, no audio)"
    )
    parser.add_argument(
        "--category",
        nargs="+",
        metavar="NAME",
        help="media/videos subdirectory to convert (default: all categories)",
    )
    parser.add_argument("--scene", help="convert only the scene whose file stem matches this name")
    parser.add_argument("--dry-run", action="store_true", help="list conversions without converting")
    parser.add_argument("--force", action="store_true", help="overwrite existing .webm outputs")
    args = parser.parse_args(argv)

    sources = find_source_files(args.category, args.scene)
    if not sources:
        print("no matching 480p15 MP4 files found")
        return 1
    print(f"found {len(sources)} source MP4(s)")

    counts = {"converted": 0, "skipped": 0, "failed": 0}
    total_bytes = 0

    for category, source in tqdm(sources, desc="converting", unit="file", disable=args.dry_run):
        destination = destination_for(category, source)
        if destination.is_file() and not args.force:
            counts["skipped"] += 1
            print(f"skipped (exists): {destination.as_posix()}")
            continue
        if args.dry_run:
            print(f"would convert: {source.as_posix()} -> {destination.as_posix()}")
            counts["converted"] += 1
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if convert_file(source, destination):
            counts["converted"] += 1
            total_bytes += destination.stat().st_size
            print(f"converted: {source.as_posix()} -> {destination.as_posix()}")
        else:
            counts["failed"] += 1

    print(f"\n{'status':<12}{'count':>6}")
    print("-" * 18)
    for status in ("converted", "skipped", "failed"):
        print(f"{status:<12}{counts[status]:>6}")
    if args.dry_run:
        print("dry run - nothing was written")
    else:
        print(f"total bytes written: {total_bytes:,}")
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
