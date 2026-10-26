---
name: dsa-add-page
description: Use when adding a new topic page to the Flask website (route, template, video asset, sync map, sidebar/footer wiring, verification checklist) or upgrading an existing text-only page with video and synced code.
---

# DSA Add-Page — recipe for a website topic page

Follow every numbered step. A page is not done until the checklist passes.

## 1. Assets first

- **Video:** convert the scene's mp4 → webm (`dsa-render` skill) into `Website/website/static/Videos/<Category>/<Scene>.webm` (exact case).
- **Sync map:** annotate the scene with `SyncedScene`/`DISPLAY_CODE`/semantic `code_step(key)` calls, author `tools/syncmap/langs/<slug>.json` (C, C++, Java, Python), and emit the combined `Website/website/static/sync/<slug>.json` (`dsa-highlightmap` skill). Pacing edits (extra waits/slower run_times for breathability) are explicitly allowed — see §7.

## 2. Route (`Website/website/views.py`)

- Kebab-case path, e.g. `/binary-search-tree`. **Never delete existing routes.**
- If a legacy/space/underscore path ever pointed here, stack an extra `@views.route("<legacy>")` decorator on the same view function instead of adding a redirect.

## 3. Template (`Website/website/templates/<Section>/<slug>.html`)

- `{% extends "content.html" %}` with blocks: title, main_content, scripts.
- Content structure (in order):
  1. H1 + one-paragraph plain-language intro
  2. Concept section (page explanation) — how the structure/algorithm works; MathJax where useful
  3. Video + synced code in **four languages**: `<video id="code-video" src="{{ url_for('static', filename='Videos/<Cat>/<Scene>.webm') }}">` + language tabs (Python / C / C++ / Java, default Python, persisted) + Prism `<pre><code class="language-python">` + `data-sync` combined-JSON URL. Every language's code must be a **correct, complete implementation** of what the video demonstrates (not pseudocode) — Python in `DISPLAY_CODE`, the other three in the `langs/<slug>.json` file, all sharing the scene's semantic step keys.
  4. Worked example — walk through the exact demo input/steps the video shows (read the scene source!)
  5. Complexity analysis with **full derivations, not bare claims**: Best / Worst / Average time, each with its recurrence (or counting argument) + solution steps (master theorem / substitution / recursion-tree / aggregate analysis) in MathJax, then Space complexity with justification (aux structures, recursion stack, in-place arguments)
  6. **Must-Know points** — 4–8 bullets of exam/interview-critical facts (invariants, edge cases, classic pitfalls)
  7. **Applications** — 3–6 real-world uses of the topic
  8. **Comparison** — with closely related topics where relevant (e.g. BFS vs DFS, Prim vs Kruskal, BST vs AVL; skip only when no meaningful relative exists), as a short table or prose
  9. Takeaways + next-topic links via `url_for`
- Multi-video pages: follow the `singly_linked_list.html` pattern — anchored sections (`#length`, …), one combined slug (with its own tab set) per video.

## 4. Content accuracy rules (non-negotiable)

- Complexity claims must match `Understanding/*.ipynb` implementations or CLRS-standard results. If you cannot verify a claim, don't state it. Every Best/Worst/Average figure needs its recurrence + derivation shown — for standard analyses (e.g. QuickSort average case) reproduce the textbook derivation at CLRS level, never a bare "it is known".
- All four language implementations must be **correct**: execute the Python locally; compile and run the C/C++/Java where toolchains exist (report what you ran). Where a toolchain is unavailable, mark that language "reviewed, not executed" in your report — never present unreviewed code as verified.
- No AI meta-text ("the sources say…"), no invented stats or ratings, no marketing claims the site can't back.
- Match the existing pages' depth (expect 400–900 lines with four code blocks). Good exemplars: `linear_search.html`, `bubble_sort.html`, `singly_linked_list.html` (structure, not length).

## 5. Navigation wiring

- Sidebar (`content.html`): add the link under its section; keep the active section open.
- Footer (`base.html`): replace the matching no-href placeholder with a real `url_for` link.
- All cross-links use `url_for`.

## 6. Checklist (all must pass)

- [ ] `pytest` green, link checker green
- [ ] Route 200 via test client; template renders
- [ ] Video URL 200 (exact case); combined sync JSON loads with all four languages
- [ ] Language switcher works on all four tabs; highlighting tracks the video in Python **and** at least one more language (watch both fully once)
- [ ] Every published number (demo outputs, costs, matrices) re-derived by script with evidence in the report
- [ ] Sidebar + footer + any cross-links resolve
- [ ] Pacing edits (if any) listed with before/after durations; updated timelines committed; `syncmap check` green
- [ ] `docs/Plan/TASKBOARD.md` updated

## 7. Pacing (making videos breathable)

Fast side-by-side highlighting is hard to follow — you may add `self.wait(...)` pauses between dense step bursts or raise individual animation `run_time`s in the scene(s) you annotate. Never change WHAT the animation demonstrates, only timing. Document each edit (scene, location, old→new duration); re-run `snapshot --scene` and commit the updated timeline as expected-drift; regenerate the map(s); re-render at `-ql` and reconvert the webm; report the total duration change per scene.
