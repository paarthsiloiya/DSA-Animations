---
name: dsa-add-page
description: Use when adding a new topic page to the Flask website (route, template, video asset, sync map, sidebar/footer wiring, verification checklist) or upgrading an existing text-only page with video and synced code.
---

# DSA Add-Page — recipe for a website topic page

Follow every numbered step. A page is not done until the checklist passes.

## 1. Assets first

- **Video:** convert the scene's mp4 → webm (`dsa-render` skill) into `Website/website/static/Videos/<Category>/<Scene>.webm` (exact case).
- **Sync map:** annotate the scene with `SyncedScene`/`DISPLAY_CODE`/`code_step` and emit `Website/website/static/sync/<slug>.json` (`dsa-highlightmap` skill).

## 2. Route (`Website/website/views.py`)

- Kebab-case path, e.g. `/binary-search-tree`. **Never delete existing routes.**
- If a legacy/space/underscore path ever pointed here, stack an extra `@views.route("<legacy>")` decorator on the same view function instead of adding a redirect.

## 3. Template (`Website/website/templates/<Section>/<slug>.html`)

- `{% extends "content.html" %}` with blocks: title, main_content, scripts.
- Content structure (in order):
  1. H1 + one-paragraph plain-language intro
  2. Concept section — how the structure/algorithm works; MathJax where useful
  3. Video + synced code block: `<video id="code-video" src="{{ url_for('static', filename='Videos/<Cat>/<Scene>.webm') }}">` + Prism `<pre><code class="language-python">` + `data-sync` JSON URL
  4. Worked example — walk through the exact demo input/steps the video shows (read the scene source!)
  5. Complexity table + properties/edge cases
  6. Takeaways + next-topic links via `url_for`
- Multi-video pages: follow the `singly_linked_list.html` pattern — anchored sections (`#length`, …), one map slug per video.

## 4. Content accuracy rules (non-negotiable)

- Complexity claims must match `Understanding/*.ipynb` implementations or CLRS-standard results. If you cannot verify a claim, don't state it.
- No AI meta-text ("the sources say…"), no invented stats or ratings, no marketing claims the site can't back.
- Match the existing pages' structure and depth (200–650 lines). Good exemplars: `linear_search.html`, `bubble_sort.html`, `singly_linked_list.html`.

## 5. Navigation wiring

- Sidebar (`content.html`): add the link under its section; keep the active section open.
- Footer (`base.html`): replace the matching no-href placeholder with a real `url_for` link.
- All cross-links use `url_for`.

## 6. Checklist (all must pass)

- [ ] `pytest` green, link checker green
- [ ] Route 200 via test client; template renders
- [ ] Video URL 200 (exact case), sync JSON loads, highlighting follows the video
- [ ] Sidebar + footer + any cross-links resolve
- [ ] `docs/Plan/TASKBOARD.md` updated
