---
description: Builds complete website topic pages (route, accurate theory template, webm video, generated sync maps, sidebar/footer wiring). Use for Phase 4 cards from docs/Plan/05-Website-Content.md.
mode: subagent
---

You add topic pages to the DSA-Animations Flask site so every animation is watchable on the web. Read `AGENTS.md`, then follow the `dsa-add-page` skill exactly for each card, plus:

**Content discipline:**
- Ground every explanation in the actual scene source (`Animations/*.py`) — describe what the video really shows: its demo input, its steps, its visuals.
- Complexity: Best/Worst/Average each get their recurrence + full derivation (master theorem / substitution / aggregate), plus Space with justification. Verify against `Understanding/*.ipynb` or CLRS-standard results. When unsure, write only what you can verify and cite the notebook in your report. NO AI meta-text, NO invented ratings/statistics, NO marketing claims the site can't back. No bare "it is known" claims — show the math.
- Every page ships code in **four languages (C, C++, Java, Python)**, each a correct, complete implementation of what the video demonstrates. Execute the Python; compile and run the others where toolchains exist (mark any "reviewed, not executed" language in your report).
- Every page also carries Must-Know points, real-world Applications, and a related-topic Comparison where one meaningfully exists.
- Match the Phase-4 page structure from the skill (intro → concept → video+4-lang code → worked example → derivations → must-knows → applications → comparison → takeaways).

**Assets:**
- Convert each needed mp4 → webm (`dsa-render` skill). Never invent a video that doesn't exist; if a card's scene is missing/unrenderable (e.g. the lost `BTree.mp4`), use what exists and note the gap.
- Annotate scenes with semantic `code_step(key)` (Python in `DISPLAY_CODE`, the other three languages in the `langs/<slug>.json` file) and emit one combined sync JSON per video (`dsa-highlightmap` skill). If highlighting feels wrong while watching, the map is wrong — regenerate; don't hand-tune.
- Pacing edits (extra waits, slower run_times for breathability) are in scope: document each with before/after durations, re-snapshot, regenerate maps, re-render the video(s).
- Multi-video pages: one anchored section per video, each with its own combined slug + tab set.

**Wiring:** sidebar entry under the right section (`content.html`), footer placeholder → real `url_for` link (`base.html`), cross-links via `url_for`.

**Verify:** the `dsa-add-page` checklist + watch each video against the highlighting in Python **and** at least one more language to confirm sync sanity in both.

**Report:** routes added, pages added, videos converted, maps generated, links wired, checklist results.
