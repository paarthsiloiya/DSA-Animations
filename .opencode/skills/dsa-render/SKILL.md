---
name: dsa-render
description: Use when a task requires rendering Manim scenes, re-rendering after bug fixes, converting rendered mp4s to webm for the website, or anything that touches Animations/media output.
---

# DSA Render — rendering & media conversion

## Cost discipline

Each render takes minutes. **Never render all scenes.** Only render scenes whose source changed. When a card says "queue for RB batch", do NOT render — just note the scene in the batch list.

## Render one scene (web standard)

```
cd Animations
manim <File>.py <Scene> -ql
```

- `-ql` = 480p15 — the website standard. `manim.cfg` (in `Animations/`) sets 720p30 defaults when no flag is passed.
- Output: `Animations/media/videos/<File>/<quality>/<Scene>.mp4`

## After rendering

1. Watch the mp4 around the timestamps your change affects.
2. If the video goes to the website → convert it (below). **Do not commit any media >1 MB without asking the user** (repo is already ~1 GiB; LFS migration pending).
3. If the scene has a sync map on disk → regenerate it (`dsa-highlightmap` skill).

## Convert rendered mp4 → webm for the site

```
python tools/convert_webm.py <Category> --scene <Scene>   # one scene
python tools/convert_webm.py <Category> --dry-run           # preview whole category
```

- Reads from `Animations/media/videos/<File>/480p15/*.mp4`
- Writes to `Website/website/static/Videos/<Category>/<Scene>.webm` — **capital V, exact case**
- Settings mirror existing webms (probe one with `ffprobe` if the script's defaults are unclear).

## Never

- Don't hand-edit anything under `Animations/media/` or `gifs/`.
- Don't render a scene just to "see what it does" — read the code instead.
