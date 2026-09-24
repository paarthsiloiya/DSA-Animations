# TASKBOARD — DSA-Animations Implementation Plan

**How to use:** pick the topmost ☐ card in dependency order (see `00-Overview.md`), tell opencode which card + agent (e.g. *"Do B5 from `docs/Plan/02-Bugfixes.md` with `dsa-bugfixer`"*), then tick it below and update the Notes column. Gate phases with `dsa-auditor`.

**Stepwise execution prompts** live in `docs/Plan/PROMPTS.md` (READ-ONLY — agents must never edit that file). Run them in numerical order; they tick the cards below.

Legend: ☐ todo · ◐ in progress · ☑ done · ✗ cancelled (note reason)

## Phase 0 — Foundation (`01-Foundation.md`)

| ID | Card | Agent | Depends | Status | Notes |
|---|---|---|---|---|---|
| F1 | Root requirements.txt (pinned) | general | — | ☐ | |
| F2 | pyproject.toml (ruff + pytest) | general | F1 | ☐ | |
| F3 | tools/link_check.py + baseline | general | F2 | ☐ | baseline-broken-links.txt = audit 04 §1 |
| F4 | tests/test_routes.py smoke | general | F2 | ☐ | |
| F5 | tools/convert_webm.py | general | — | ☐ | probe settings from existing webm |
| F6 | CI workflow | general | F2,F3,F4 | ☐ | |

## Phase 1 — Bugfixes (`02-Bugfixes.md`)

| ID | Card | Agent | Depends | Status | Notes |
|---|---|---|---|---|---|
| B1 | Flask config (SECRET_KEY, DB path, untrack db) | dsa-bugfixer | — | ☐ | ask user re: DB contents |
| B2 | videos/ → Videos/ casing (8 templates) | dsa-bugfixer | — | ☐ | |
| B3 | Hide dead nav honestly | dsa-bugfixer | F3 | ☐ | re-enabled in C14 |
| B4 | Fix relative/.md links | dsa-bugfixer | F3 | ☐ | |
| B5 | Binary-search sample code | dsa-bugfixer | — | ☐ | recheck inline map |
| B6 | Complexity/math corrections | dsa-bugfixer | — | ☐ | verify vs Understanding/*.ipynb |
| B7 | Copy defects batch | dsa-bugfixer | — | ☐ | |
| B8 | Home honesty (ratings, controls claim) | dsa-bugfixer | — | ☐ | |
| B9 | CSS defects (selector, invalid value, dupes) | dsa-bugfixer | — | ☐ | |
| B10 | AVL LeftLeft label → "Right Rotation" | dsa-bugfixer | — | ☐ | queue RB1 |
| B11 | Floyd-Warshall k, adjacency sets→tuples, "egde" | dsa-bugfixer | — | ☐ | queue RB1 |
| B12 | QuickSort base-case guard | dsa-bugfixer | — | ☐ | no visual change |
| B13 | Heap zero-line/self-loop + comparison text | dsa-bugfixer | — | ☐ | queue RB1 |
| B14 | D&C LCS guard, closest-pair strip, fade blocks | dsa-bugfixer | — | ☐ | queue RB1 |
| B15 | Greedy interval label shift | dsa-bugfixer | — | ☐ | queue RB1 |
| B16 | Converter moviepy 2.x, finally-close, with_suffix | dsa-bugfixer | F1 | ☐ | |
| B17 | Notebooks (Dijkstra inf, heap delete, typos) | dsa-bugfixer | — | ☐ | |
| RB1 | Render batch (9 scenes) | general | B10–B15 | ☐ | needs media-commit approval (D7) |
| G1 | **Gate: dsa-auditor re-verifies audit 04** | dsa-auditor | RB1 | ☐ | |

## Phase 2 — Sync Tool (`03-Sync-Tool.md`)

| ID | Card | Agent | Depends | Status | Notes |
|---|---|---|---|---|---|
| T1 | Spike → tools/syncmap/DESIGN.md | explore | — | ☐ | time model vs manim 0.19 |
| T2 | Recorder core + unit tests | general | T1 | ☐ | |
| T3 | Animations/synced.py (SyncedScene) | general | — | ☐ | no-op when rendering |
| T4 | Snapshot CLI (--scene/--all) | general | T2,T3 | ☐ | |
| T5 | Map emit + content.html loader | general | T4 | ☐ | wire one real page as proof |
| T6 | Drift check command | general | T4,T5 | ☐ | |
| T7 | Baseline snapshots of all 72 scenes | general | T4, **P1 done** | ☐ | THE refactor oracle |
| T8 | Tool README + skill sync | general | T2–T6 | ☐ | |
| G2 | **Gate: auditor checks determinism + drift detection** | dsa-auditor | T7,T8 | ☐ | |

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
