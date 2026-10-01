# TASKBOARD — DSA-Animations Implementation Plan

**How to use:** pick the topmost ☐ card in dependency order (see `00-Overview.md`), tell opencode which card + agent (e.g. *"Do B5 from `docs/Plan/02-Bugfixes.md` with `dsa-bugfixer`"*), then tick it below and update the Notes column. Gate phases with `dsa-auditor`.

**Stepwise execution prompts** live in `docs/Plan/PROMPTS.md` (READ-ONLY — agents must never edit that file). Run them in numerical order; they tick the cards below.

Legend: ☐ todo · ◐ in progress · ☑ done · ✗ cancelled (note reason)

## Phase 0 — Foundation (`01-Foundation.md`)

| ID | Card | Agent | Depends | Status | Notes |
|---|---|---|---|---|---|
| F1 | Root requirements.txt (pinned) | general | — | ☑ | 8 direct deps pinned to installed; dev pins in requirements-dev.txt; converter moviepy floor → `>=2.0,<3.0` |
| F2 | pyproject.toml (ruff + pytest) | general | F1 | ☑ | config-only, no [project]; ruff runs (145 findings = R8 backlog); pytest exit 5 until F4 adds tests/ |
| F3 | tools/link_check.py + baseline | general | F2 | ☑ | baseline = 37 links (29 route-404 + 8 videos/-case); 1128 dead-anchor warnings |
| F4 | tests/test_routes.py smoke | general | F2 | ☑ | 26 tests green: 24 routes 200 + /logout 302 + no-new-links |
| F5 | tools/convert_webm.py | general | — | ☑ | VP9/-an per probe; pilot Queue.webm (150 KB) converted; 64+9 dry-run |
| F6 | CI workflow | general | F2,F3,F4 | ☑ | ubuntu, py3.11, pip cache; pytest + ruff --exit-zero (drop after PROMPT 026) |

## Phase 1 — Bugfixes (`02-Bugfixes.md`)

| ID | Card | Agent | Depends | Status | Notes |
|---|---|---|---|---|---|
| B1 | Flask config (SECRET_KEY, DB path, untrack db) | dsa-bugfixer | — | ☑ | DB had 1 test row only (test@gmail.com); instance-path DB + DSA_SECRET_KEY env; both launch styles verified |
| B2 | videos/ → Videos/ casing (8 templates) | dsa-bugfixer | — | ☑ | 8 templates fixed; stack video 200 re-verified |
| B3 | Hide dead nav honestly | dsa-bugfixer | F3 | ☑ | 18 sidebar links → span.nav-item-pending[data-target] + note; footer block hidden | re-enabled in C14 |
| B4 | Fix relative/.md links | dsa-bugfixer | F3 | ☑ | 4 real targets → url_for; 4 no-page items → pending spans + notes; algorithms/linked_list fixed |
| B5 | Binary-search sample code | dsa-bugfixer | — | ☑ | sorted array + N-1 + x=4 (matches video demo); map line refs unchanged |
| B6 | Complexity/math corrections | dsa-bugfixer | — | ☑ | 8 claim fixes; all CLRS-verifiable |
| B7 | Copy defects batch | dsa-bugfixer | — | ☑ | incl. 2 extra "the sources" hits the audit missed (arrays:28, insertion_sort:189) |
| B8 | Home honesty (ratings, controls claim) | dsa-bugfixer | — | ☑ | 6 rating frames removed; wording matches plain <video controls> |
| B9 | CSS defects (selector, invalid value, dupes) | dsa-bugfixer | — | ☑ | webkit selector → .topic-carousel; flex dropped; dup scrollbar-width deduped |
| B10 | AVL LeftLeft label → "Right Rotation" | dsa-bugfixer | — | ☑ | label fixed; RB1 must re-render LeftLeftCase |
| B11 | Floyd-Warshall k, adjacency sets→tuples, "egde" | dsa-bugfixer | — | ☑ | queue RB1: FloydWarshall + WeightedAdjecencyListUD/D + PrimsMCST re-render; FW gains intended k=0 no-update tableau (final matrix unchanged) |
| B12 | QuickSort base-case guard | dsa-bugfixer | — | ☑ | no re-render needed; demo trace: only empty call (0,-1) marked an already-green pivot |
| B13 | Heap zero-line/self-loop + comparison text | dsa-bugfixer | — | ☑ | queue RB1: MaxHeap/MinHeap re-render; root cases now draw node-only (edge/Line guarded) and skip the bogus root "correct position" text |
| B14 | D&C LCS guard, closest-pair strip, fade blocks | dsa-bugfixer | — | ☑ | queue RB1: LCS/ClosestPairPoint re-render; strip now standard y-break form (demo answer 0.28 identical to brute force); fade_in/out always defined, NameError hazard gone |
| B15 | Greedy interval label shift | dsa-bugfixer | — | ☑ | queue RB1: IntervalScheduling re-render; ruler ticks now labeled 0..12 so tick i aligns with interval start s |
| B16 | Converter moviepy 2.x, finally-close, with_suffix | dsa-bugfixer | F1 | ☑ | with_suffix + try/finally clip.close() + clip = clip.resized(); live-tested on moviepy 2.2.1 (default, --resize, output_dir=None); .bat: --no-install flag + pip errorlevel check |
| B17 | Notebooks (Dijkstra inf, heap delete, typos) | dsa-bugfixer | — | ☑ | Dijkstra test < np.inf; Wieghted→Weighted ×2, AMGaphD→AMGraphD (all cells); heap single-node delete guard (heapify-up after replacement still skipped — known limitation, out of scope); both notebooks re-executed clean via nbconvert |
| RB1 | Render batch (9 scenes) | general | B10–B15 | ☑ | 9/9 rendered -ql; 8 mp4s modified + LCS byte-identical (guard-only fix); OCR spot-checks all pass; media committed with user approval in the Phase-1 finalization commit |
| G1 | **Gate: dsa-auditor re-verifies audit 04** | dsa-auditor | RB1 | ☑ | PASSED 2026-09-25: all S1-S4 claimed rows re-derived green; S5 sources cited + 3 OCR video spot-watches; stack green (26 pytest, links 0, 24+1 routes); deferred-by-design: Roboto font (W3), @media (W1), make_arrow(-1), AVLNode typing |

## Phase 2 — Sync Tool (`03-Sync-Tool.md`)

| ID | Card | Agent | Depends | Status | Notes |
|---|---|---|---|---|---|
| T1 | Spike → tools/syncmap/DESIGN.md | explore | — | ☑ | 2026-09-28: NullRenderer via Scene(renderer=...) beats monkey-patch — 25/25 events byte-identical to CairoRenderer skip path; LinearSearch/TreeBFS/Dijkstra all run headless (9.5s/73.9s/118.9s raw); key finding: video time needs frame quantization (ceil plays, floor static waits) — two-clock model |
| T2 | Recorder core + unit tests | general | T1 | ☑ | NullRenderer via Scene(renderer=...) per DESIGN.md §3; 13 tests green (defaults, wait, run_time, code_step ordering, Succession/LaggedStart totals, determinism, clamp, error capture, CairoRenderer-skip cross-validation); LinearSearch live proof: recorded 9.5s == manual sum, first 8 run_times identical |
| T3 | Animations/synced.py (SyncedScene) | general | — | ☑ | no-op when rendering; code_step forwards to injected _syncmap_recorder hook; DISPLAY_CODE typed ClassVar (RUF012); import-silence covered by subprocess test |
| T4 | Snapshot CLI (--scene/--all) | general | T2,T3 | ☑ | python -m tools.syncmap snapshot --scene|--all --batch --modules --out; 72 scenes enumerated across the 11 modules (incl. dash-named Stack-Queue); LinearSearch re-run SHA-256-identical (24F249…807B); SearchingAlgorithms bench 6.4s for 2 scenes incl. startup; manifest "generated" kept env-independent (no wall-clock) so files stay byte-comparable |
| T5 | Map emit + content.html loader | general | T4 | ☑ | map cmd (tools/syncmap/emit.py) + data-sync fetch loader w/ inline fallback; LinearSearch annotated as SyncedScene (timeline proven byte-identical: 25 play/wait events unchanged, 12 zero-time code_steps added); emitted map frame-exact vs webm transitions (±1 60fps frame), hand map drifted up to +0.53s; real-page wiring deferred to Phase 4 per prompt (scratch proof page removed); found: media/LinearSearch.mp4 is a stale render (127f/8.47s) vs webm (current scene, ~9.47s content) — flag for T7 spot-check |
| T6 | Drift check command | general | T4,T5 | ☑ | check: timelines byte-compare (distinguishes events-drift vs stale source_sha256), maps re-derive in memory, un-snapshotted warning (exit 0), --legacy inline-map parser (10 pages, informational >1.0s threshold); injection proof: run_time 0.4→0.45 flagged w/ first differing event, revert → clean; pyc same-size-mutation trap documented (drift fixture mutates size-changing) |
| T7 | Baseline snapshots of all 72 scenes | general | T4, **P1 done** | ☑ | 72/72 scenes snapshotted, 0 errors, manifest clean; recorder fix required first: tex_dir now pinned to gitignored Animations/media/Tex (15 MathTex scenes failed with media\Tex FileNotFoundError from repo-root cwd); determinism proven across two --all runs (73 files byte-identical, 0 diffs) + check re-record (clean 72); timelines/ = 0.42 MB; LinearSearch 5387a35c…, TreeBFS bd97b54c…, AVLTreeInsertion 30e5f8bd… identical in both runs |
| T8 | Tool README + skill sync | general | T2–T6 | ☑ | tools/syncmap/README.md written (purpose, convention, CLI+schemas, 5-line time model, loader); skill NOT edited per prompt — 6 discrepancies reported to user (mechanism, ClassVar, --category, check semantics, data-from-sync, loader line range) |
| G2 | **Gate: auditor checks determinism + drift detection** | dsa-auditor | T7,T8 | ☑ | PASSED 2026-09-29: full --all re-run vs baseline 73/73 files byte-identical (72 scenes, 0 errors); LinearSearch annotation proven timeline-neutral (25 play/wait events byte-identical committed-vs-live, 12 zero-time code_steps, 9.5s); fresh map validates (12 entries, lines independently checked vs 11-line DISPLAY_CODE); scratch artifacts confirmed gone; +0.5s drift flagged via temp-module monkeypatch (no repo edits), revert → clean; pytest 63, links 0, 25/25 route smoke; docs findings: README omits check's --timelines/--sync/--modules flags; 6 skill discrepancies reported for user update |

## Phase 3 — Refactor (`04-Refactor.md`) — oracle must stay byte-identical

| ID | Card | Agent | Depends | Status | Notes |
|---|---|---|---|---|---|
| R1 | common.py shared classes (ListElement/Node/WeightedLine/updaters) | dsa-refactorer | G2 | ☐ | |
| R2 | animate_traversal helper (6 sites) | dsa-refactorer | G2 | ☐ | |
| R3 | remove_edge_visual helper (7 sites) | dsa-refactorer | G2 | ☐ | |
| R4 | Dead-code sweep (audit 02/03 lists) | dsa-refactorer | G2 | ☐ | |
| R5 | BTrees logger fix | dsa-refactorer | G2 | ☐ | |
| R6 | Typo renames (SortingAlgorithms, Adjacency, Prim's, AVLNode typing) | dsa-refactorer | R1 | ☐ | expected text diffs listed; queue RB2 |
| R7 | Flask cleanups + kebab aliases | dsa-refactorer | G2 | ☐ | both alias sets must pass |
| R8 | Ruff full pass | dsa-refactorer | R1–R7 | ☐ | |
| R9 | (Stretch) Huffman single-pass | dsa-refactorer | R1 | ☐ | skip if timeline changes |
| RB2 | Render batch (8 adjacency scenes) | general | R6 | ☐ | |
| G3 | **Gate: auditor proves byte-identical timelines** | dsa-auditor | R8,RB2 | ☐ | |

## Phase 4 — Website Content (`05-Website-Content.md`) — agent: dsa-page-builder

| ID | Card | Depends | Status | Notes |
|---|---|---|---|---|
| C0 | Bulk webm conversion (~56) | F5, RB1, RB2 | ☐ | confirm size delta with user (D7) |
| C1 | Arrays pages + 4 videos | C0 | ☐ | routes exist |
| C2 | LinkedList leftovers + /rotation | C0 | ☐ | 2 orphan webms finally used |
| C3 | Queue page video | C0 | ☐ | |
| C4 | Trees I: types, traversals, list-correlation, union-find | C0 | ☐ | 8 videos |
| C5 | Trees II: BST, ternary, heaps | C0 | ☐ | 5 videos |
| C6 | /avl-tree (6 videos) | C0 | ☐ | rotations page sections |
| C7 | /b-tree (BTreeScene) | C0 | ☐ | BTree.mp4 lost — honest note |
| C8 | Graphs I: types + representation (12 videos) | C0 | ☐ | |
| C9 | Graphs II: traversals (4 videos) | C0 | ☐ | |
| C10 | Graphs III: shortest paths (3 pages) | C0 | ☐ | honest about BF cycle-check gap |
| C11 | Graphs IV: Prim's, Kruskal's, topo sort | C0 | ☐ | |
| C12 | D&C section (4 pages) | C0 | ☐ | new sidebar section |
| C13 | Greedy section (2 pages) | C0 | ☐ | honest about Huffman codes gap |
| C14 | Nav sweep: un-hide + footer + allowlist → 0 | C1–C13 | ☐ | |
| G4 | **Gate: auditor full content sweep** | C14 | ☐ | |

## Phase 5 — Website Polish (`06-Website-Polish.md`)

| ID | Card | Agent | Depends | Status | Notes |
|---|---|---|---|---|---|
| W1 | Responsive CSS + touch carousel | dsa-page-builder | G4 | ☐ | |
| W2 | Dark mode toggle (CSS exists!) | dsa-page-builder | G4 | ☐ | + Prism theme swap |
| W3 | Fonts load or system stack | dsa-page-builder | G4 | ☐ | ask user: self-host vs CDN |
| W4 | Favicon/titles/meta/OG | dsa-page-builder | G4 | ☐ | logo-icon.png finally used |
| W5 | Client-side search | dsa-page-builder | C14 | ☐ | |
| W6 | Home final honesty pass | dsa-page-builder | C14 | ☐ | |
| W7 | Privacy/terms/about pages | dsa-page-builder | G4 | ☐ | promised at signup |
| W8 | Auth polish (subscribed decision) | dsa-page-builder | G4 | ☐ | ask user |
| W9 | Performance pass | dsa-page-builder | W1 | ☐ | |
| W10 | (Optional) legacy inline-map migration | general | G4 | ☐ | |
| G5 | **Gate: final audit re-run + DoD sign-off** | dsa-auditor | all | ☐ | audit addenda written |
