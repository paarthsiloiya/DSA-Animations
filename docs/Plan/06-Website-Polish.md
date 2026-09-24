# 06 — Phase 5: Website Polish

**Objective (Goal G4):** overall site quality — responsive, themeable, findable, honest, fast.
**Preconditions:** Phase 4 (nav is real; polish targets stable markup). **Parallelizable:** W1–W5 touch mostly disjoint areas (CSS / base.html head / home / new pages) — coordinate via TASKBOARD notes; W6+ sequential.

### W1 — Responsive design
Agent: dsa-page-builder · Depends: — · Size: L
**Problem** (audit 02 §5): zero `@media` queries; fixed 310px cards; carousel is mouse-events-only (no touch).
**Do:** Breakpoints (≥1024 / 768–1023 / <768): fluid grid for home cards + sidebar, `details` sidebar collapses to hamburger or inline sections on mobile, topic carousel switches to Pointer Events (pointerdown/move/up with `touch-action: pan-y`), code blocks scroll horizontally, tables get overflow wrappers. Test at 390px/768px/1440px widths.
**Verify:** dsa-verify + manual widths; carousel drags via touch emulation.
**Done when:** no horizontal scrollbars at 390px on any page.

### W2 — Dark mode toggle
Agent: dsa-page-builder · Depends: — · Size: M
**Problem** (audit 03 §4): `styles.css:73-79` has a complete dark theme but `data-theme` is hardcoded `"light"` with no toggle.
**Do:** Toggle button in navbar (sun/moon); JS: `document.documentElement.dataset.theme` + `localStorage` persistence + respect `prefers-color-scheme` on first visit; swap Prism to a dark code theme when dark (load both themes, toggle class); ensure MathJax/inline colors don't break (audit which elements hardcode colors).
**Verify:** toggle persists across reloads; no unreadable text in dark on content pages (check 4 pages incl. a code+video page).
**Done when:** theme switch works site-wide.

### W3 — Fonts decision & load
Agent: dsa-page-builder · Depends: — · Size: S
**Problem** (audit 02 §5): `Roboto`, `JetBrains Mono`, `Arial` referenced, never loaded.
**Do:** Decide with the user: self-host (no external requests) vs Google Fonts. Default: self-host woff2 subsets under `static/fonts/` + `@font-face`, full font stack fallbacks.
**Verify:** computed styles show the real font; Lighthouse no longer flags fallback-only.
**Done when:** fonts actually render.

### W4 — Favicon, titles, meta
Agent: dsa-page-builder · Depends: — · Size: S
**Problem** (audit 02 §5): no favicon, generic titles ("DSA" on algorithms page), no meta description.
**Do:** Favicon (reuse `static/images/logo-icon.png` — finally referenced!); per-page `<title>{Topic} — DSA-Animations</title>` via the title block; meta description per page; og: tags on home.
**Verify:** dsa-verify; tab titles correct on 5 pages.
**Done when:** done.

### W5 — Search
Agent: dsa-page-builder · Depends: C14 · Size: M
**Do:** Lightweight client-side search: build a JSON index (page title, URL, section headings, keywords) via a small generator script (`tools/build_search_index.py` run at deploy, output `static/search-index.json`); search box in navbar filters dropdown-style. No server round-trips.
**Verify:** finds "AVL rotation" from the /avl-tree page; empty query shows nothing weird.
**Done when:** search usable on every page.

### W6 — Home page final pass
Agent: dsa-page-builder · Depends: C14 · Size: S
**Do:** Explore buttons wired (C14 may cover); topic cards reflect real content counts (e.g. "6 videos" not invented ratings); any "coming soon" copy only where content genuinely isn't there yet.
**Verify:** honesty grep (no ratings, no unverifiable claims); visual pass.
**Done when:** home is 100% honest + wired.

### W7 — Account/legal pages
Agent: dsa-page-builder · Depends: — · Size: S
**Problem:** signup page promises "Terms of Service and Privacy Policy" that don't exist; footer wants About/Contact.
**Do:** Simple, truthful static pages: `/privacy`, `/terms` (plain honest text — no invented legal entities), `/about` describing the project; link from footer + signup text. Contact → GitHub issues link (README already says contributions welcome).
**Verify:** link checker; pages render.
**Done when:** no promised-but-missing pages.

### W8 — Auth polish (scoped)
Agent: dsa-page-builder · Depends: — · Size: S
**Do:** Keep content public (D3). Add flash-message styling polish; wire the `subscribed` checkbox honestly: label it clearly on signup and either store silently (current) or remove — **ask the user**, default = keep + label "we'll never email you until a newsletter exists".
**Verify:** signup flow works; no dead ends.
**Done when:** decided + implemented.

### W9 — Performance pass
Agent: dsa-page-builder · Depends: W1 · Size: S
**Do:** `preload="none"` + `poster` frames on below-the-fold videos; `loading="lazy"` on images; CDN scripts (MathJax/Prism) get `defer`; check template weight (inline JS blocks that grew large move to `static/js/`).
**Verify:** home + one content page Lighthouse ≥ 90 perf / no layout shift from videos.
**Done when:** pass.

### W10 — (Optional) Legacy inline-map migration
Agent: general · Depends: C15 · Size: M
**Do:** Annotate the ~10 legacy-page scenes (searches, sorts, linked lists, stack), emit JSON maps, delete inline `highlightMap` arrays from templates. Pure win once maps are machine-verified; skip any scene whose timings were hand-tuned in the notebook harness (report those).
**Verify:** `tools/syncmap check --legacy` green before deleting each inline map.
**Done when:** inline maps gone or consciously kept with reasons.

### W11 — Final audit & DoD
Agent: dsa-auditor · Depends: all · Size: M
**Do:** Re-run the full 5-report audit (like the original exploration): fresh bug scan, link checker with empty allowlist, route smoke incl. aliases, syncmap check, responsive spot-check, content accuracy sampling, git hygiene check (no new big binaries committed unapproved). Update `docs/Audit/*` with a "2026 post-fix" addendum per report.
**Verify:** everything (that's the point).
**Done when:** project DoD checklist in `00-Overview.md` fully checked.

### Phase 5 exit gate

- [ ] Responsive green at 3 widths; dark mode persists; fonts real
- [ ] Search works; titles/favicons/meta everywhere; honest UI copy
- [ ] Final auditor report written; all audit addenda updated
- [ ] Project DoD (00-Overview) satisfied
