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
| R1 | common.py shared classes (ListElement/Node/WeightedLine/updaters) | dsa-refactorer | G2 | ☑ | 2026-10-01: 9 modules migrated to new Animations/common.py (153 ln); ListElement×4→1 (VGroup, getListElement()=self; dual isFound/isSorted flag; value alpha-preserving coercion), visual Node×5→1 (radius/font_size params), WeightedLine×2→1 (standalone_bg + weight_font params), bezier/arrowhead updater pair×7→1 (back= param folds the _back mirror), playSurroundingNodeAnimation×4→1 (TreeListCorrelation copy was dead — deleted); full check 72/72 events byte-identical (69 timelines regenerated, source_sha256 only), exit 0; BubbleSort control render vs HEAD source: PSNR inf, 535/535 frames identical; committed BubbleSort.mp4 found stale (520f/34.67s @2025-07-24 vs webm 35.3s current — pre-existing, working tree media restored); pytest 64 green, links 0, ruff 145→133 no new classes |
| R2 | animate_traversal helper (6 sites) | dsa-refactorer | G2 | ☑ | 2026-10-01: 6 BFS/DFS while-loops (TreeBFS/TreeDFS + 4 Graph scenes) → one animate_traversal(scene, graph, adjacency_list, start, start_text, *, use_stack, container_shift, processing_buff, explanatory_font_size, neighbors_of, edge_highlight, on_visit) in common.py; pre-verified via normalization diff that all 6 blocks are one idiom; scoped oracles 14/14 + 22/22 events identical, full check 72/72 exit 0; grep: while (queue|stack) 6→0, "Processing node {current}" 6→1 |
| R3 | remove_edge_visual helper (7 sites) | dsa-refactorer | G2 | ☑ | 2026-10-01: 7 BST-deletion edge-removal blocks → one remove_edge_visual(scene, graph, u_value, v_value, u_node, v_node) returning the removed mobject; normalization diff proved all 7 identical (3 parent-edge blocks byte-identical → replaceAll); in-loop tree_node_map lookups moved to call-site args (no behavior change); BinarySearchTreeDeletion events byte-identical; grep: "for edge in list(G.edges)" 7→0, isinstance(manim_edge, Line) 7→1 |
| R4 | Dead-code sweep (audit 02/03 lists) | dsa-refactorer | G2 | ☑ | 2026-10-03: all 11 modules swept, −1,269 net LOC; removed AVLTree dead insert_into_AVLTree/insert + reconnect_after_rotation (4 call sites — proven no-op: rotations already clear_updaters on the returned node) + 5 debug prints + dup balance computation; BTrees remove_keys_after; Graphs Prim's write-only distance dict (kept try/except KeyError); Trees MaxHeap/MinHeap ghost nx graphs + 2× duplicated bst_root[0] + dead parent_node + comment remnant; Greedy always-true hasattr; all audit-listed commented-out blocks + identical duplicates; F401 imports (Percent/Pixels ×7, CurvedArrow ×2, AVLTree nx, BTrees random/np/os) + mid-file imports moved (SortingAlgoritms networkx + EDGE_COL redef deleted, D&C math); shadow renames (Graphs nodes[_]→idx ×4, LinkedList inner i→j); pyproject per-file-ignores F403 for Animations/*.py (star imports are the module mechanism); ruff --select F401,F403 zero findings; kept: Insertion-scene parent_node (live), Dijkstra loop var _ (not an index), LinkedList comments (not audit-listed), ruff F403 noise on I001-order |
| R5 | BTrees logger fix | dsa-refactorer | G2 | ☑ | 2026-10-03: deleted import-time root-handler hijack + basicConfig + FileHandler + os/random/np imports; module-level logger = logging.getLogger(__name__); ~86 logger.info trace calls + 12 companion dead vars deleted, 5 warning/error + 19 pre-existing debug calls kept; verified: scratch-cwd import → zero output, zero btree_operations.log (stale gitignored file removed); 111 log calls → 24 |
| R6 | Typo renames (SortingAlgorithms, Adjacency, Prim's, AVLNode typing) | dsa-refactorer | R1 | ☑ | 2026-10-03: git mv SortingAlgoritms.py → SortingAlgorithms.py (R, history preserved) + media/videos dir (12 files R); Graphs.py Adjecency→Adjacency ×12 (8 class names + 4 "Adjecency Matrix" titles) via replaceAll; mp4_to_gif_converter category updated; convert_webm.py CATEGORY_ALIASES += SortingAlgoritms→SortingAlgorithms (alias key = the only sanctioned old-spelling hit); base.html "Prims's"→"Prim's"; AVLNode value: str \| int (param + attribute); old Adjecency*.json timelines removed, snapshot --all re-run: all 8 events byte-identical (scene+sha only), 6 sorting timelines module→Animations.SortingAlgorithms, manifest rekeyed; full check 72/72 exit 0; grep Adjecency 0 in Animations/tools, SortingAlgoritms 0 in live code, Prims's 0; RB2 (PROMPT 028) must render the 8 renamed adjacency scenes + 6 sort scenes under the new module dir |
| R7 | Flask cleanups + kebab aliases | dsa-refactorer | G2 | ☑ | 2026-10-03: user_loader → db.session.get(User, int(id)) (legacy User.query.get gone); 16 kebab-case aliases ADDED as stacked second @views.route decorators (original space-URLs untouched, no redirects — both spellings 200 directly); template sweep: 3 remaining hardcoded href="/" in content.html → url_for('views.home') (rest already url_for from B4); tests/test_routes.py: original 25 kept + 16 alias-200 + 16 alias-same-page (byte-identical) params → 57 tests, full suite 96 passed; link checker 0; syncmap formality check 72/72 exit 0 (no scenes touched); live dev-server curl: /linked-list ≡ "/linked list" (30525 B), /heap-sort ≡ "/heap sort" (42346 B), both 200 |
| R8 | Ruff full pass | dsa-refactorer | R1–R7 | ☑ | 2026-10-04: 90 findings → 0 across Animations/Website/tools/converter (F841 31 dead vars incl. 4 Graphs degrees + 2 traversal-scene nodes, I001 18 headers hand-sorted, F541 13 f-prefixes, C408 6 dict()→{}, B023 5 noqa late-binding updaters, PLC0206 2 →items()/values(), UP034 3 + UP039 2 parens, SIM102/SIM113/B026/C413/PIE808/RUF010/RUF013/PYI041/BLE001-noqa/F401 singles; 3 cascading findings fixed on re-check); --fix never run on repo files (temp-copy reference only, and that proved wrong — ruff --diff on real files is authoritative); ORACLE caught my replaceAll overreach: 17 Graphs scenes crashed NameError (used nodes/graphVertices/degrees deleted alongside the 6+12 unused ones) — restored in all 16 scenes, only truly-unused sites stay deleted; full check 72/72 events byte-identical, exit 0; pytest 96 green, links 0, dev-server spot / + /dsa + /heap-sort 200; ruff format NOT run (deliberate: avoid churn); CI may now drop --exit-zero (auditor to confirm in PROMPT 029) |
| R9 | (Stretch) Huffman single-pass | dsa-refactorer | R1 | ☑ | 2026-10-04: MERGED — new huffman_steps(s) computes the merge sequence once ((freq,symbol) sort provably tie-free → deterministic), emitting 9-field event tuples consumed by BOTH build_huffman_graph (G/labels/weights, same node+edge insertion order → same visuals) and animate_huffman_construction (same play/wait sequence → HuffmanEncoding timeline byte-identical, oracle events-identical proof); Node-object bookkeeping (node_objects/node_id_map/temp_nodes/counters) eliminated from both passes; net −92 lines; oracle clean 72/72, pytest 96, links 0, ruff 0 |
| RB2 | Render batch (8 adjacency scenes) | general | R6 | ☑ | 2026-10-04: 8/8 rendered -ql in one 5-min batch (mp4 ready times 13:32:02→13:36:13, 23-46s each); durations/frames EXACTLY match old (682/640/614/599f); pixel spot-check vs old mp4s: 4 list scenes 0.0000% diff (titles were already correct), 2 unweighted matrix = single 12×16px glyph at (522,54) = the "Adjecency"→"Adjacency" title fix isolated to the one corrected letter, 2 weighted matrix = title fix + ~0.1% sub-pixel anti-aliasing drift at weight-label glyphs only (old mp4s are 2025-07-24 pre-uniformity renders; proven environmental — today's render matches the RB1-era 2026 weighted-list renders 0.0000%); no media committed — 8 stale Adjecency*.mp4 await user-approved git rm |
| G3 | **Gate: auditor proves byte-identical timelines** | dsa-auditor | R8,RB2 | ☑ | PASSED 2026-10-04: fresh snapshot --all (72/72, 0 errors) vs HEAD baseline (9976380, pre-Phase-3 PROMPT-019 oracle): 58 scenes events byte-identical + sha-only, 14 expected-rename-diffs (8 adjacency scene-names + 6 sorting module SortingAlgoritms→SortingAlgorithms), DRIFT NONE; duplication: all 8 shared helpers defined exactly once in common.py (Node×2 = canonical + LinkedList's distinct linked-list Node); dead code gone (insert_into_AVLTree only AVLTreeInsertion's live def+call, remove_keys_after/reconnect_after_rotation/AVL prints/logger.info/basicConfig/FileHandler all 0); BTrees scratch-cwd import: zero output, zero log file; Adjecency 0 in Animations/tools, SortingAlgoritms 0 in live code (1 = mandated convert_webm alias key), base.html "Prim's Algorithm" ✓; 5 sampled route pairs both spellings 200 + byte-identical; ruff exit 0, pytest 96, links 0; 3-video spot check: WeightedAdjacencyListD 0.0000% pixel diff, MatrixUD/D title-letter-only (12×16 bbox, ~0.03%); ci.yml --exit-zero confirmed present — NOW REMOVABLE per PROMPT 026 |

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
