# 05 — Phase 4: Website Content (all animations on the site)

**Objective (Goal G3):** every animation topic gets real pages — Trees, Heaps, Graphs, AVL, B-Trees, D&C, Greedy, plus the LinkedList/Queue/Arrays gaps from `docs/Audit/05 §3` (~56 videos). Also un-hides the nav placeholders hidden in B3.
**Preconditions:** Phase 2 (maps via tool) + Phase 3 (clean scene code to annotate). **Agent:** `dsa-page-builder` for all cards; every card follows the `dsa-add-page` + `dsa-highlightmap` skills (recipe lives there — cards stay short).
**Note (D7):** converting ~56 webm videos adds roughly 30–60 MB to the repo. Confirm with the user once, at C0.

### C0 — Bulk webm conversion
Agent: general · Skill: dsa-render · Depends: F5, RB1, RB2 · Size: M
**Do:** With user approval for the size delta: `python tools/convert_webm.py` for Arrays, Trees, AVLTree, BTrees, Graphs, DivideAndConquer, Greedy, LinkedList (leftovers), Stack-Queue (Queue). Use the post-RB1/RB2 renders where they exist.
**Verify:** all target `.webm` exist; each plays; exact-case paths.
**Done when:** inventory list written into the card's TASKBOARD note (scene → webm path).

### C1 — Arrays pages upgrade
**Pages:** existing `/arrays`, `/2D arrays` (routes exist; pages text-only today).
**Videos → maps:** MemoryAllocation, Indexing → `/arrays`; TwoDArraysAsMatrix, TwoDArraysMultiplication → `/2D arrays`.
**Do:** Annotate the 4 scenes (`SyncedScene` + `DISPLAY_CODE` + `code_step`), emit maps, extend both templates with video+code sections per skill.
**Grounding:** array math from `Animations/Arrays.py`; complexities are trivial (O(1) index, etc.).
**Verify:** skill checklist.

### C2 — LinkedList completion
**Pages:** existing `singly_linked_list.html` + `doubly_linked_list.html` get new anchored sections; new route `/rotation`.
**Videos → maps:** NodeExplanation, TraverseLinkedList → singly (already-converted `NodeExplanation.webm` finally used!); DoubleNodeExplanation → doubly (webm also already on disk); ListRotation → `/rotation` page.
**Do:** per skill; wire the old `content.html:56` `/rotation` link (unhide from B3).
**Verify:** skill checklist.

### C3 — Queue page video
**Page:** existing `/queue` (text-only today).
**Videos → maps:** Queue (convert in C0).
**Verify:** skill checklist.

### C4 — Trees I (foundations & traversals)
**New routes:** `/types-of-trees`, `/tree-traversals`, `/tree-list-correlation`, `/union-find`.
**Videos → maps:** TreeExplanation → types-of-trees; TreeBFS, TreeDFS, InOrderTraversal, PreOrderTraversal, PostOrderTraversal → tree-traversals (multi-video, anchored); TreeListCorrelation → tree-list-correlation; UnionFind → union-find.
**Grounding:** `Understanding/Trees/Trees.ipynb` (traversals, Union-Find with path compression + union by rank).
**Verify:** skill checklist; sidebar Trees section unhides these entries.

### C5 — Trees II (BST, ternary, heaps)
**New routes:** `/binary-search-tree`, `/ternary-tree`, `/types-of-heaps`.
**Videos → maps:** BinarySearchTreeInsertion + BinarySearchTreeDeletion → binary-search-tree (2 videos, anchored); TernaryTreeExplanation → ternary-tree; MaxHeap + MinHeap → types-of-heaps (2 videos).
**Grounding:** `Understanding/Trees/Trees.ipynb` (BST ops, heap sift); deletion 4-case explanation must mirror the scene's successor logic.
**Verify:** skill checklist.

### C6 — AVL trees
**New route:** `/avl-tree` (sidebar already expects it).
**Videos → maps:** AVLTreeInsertion, AVLTreeDeletion + the 4 rotation-case videos (LeftLeftCase, LeftRightCase, RightLeftCase, RightRightCase) — 6 videos on one multi-video page with anchored sections per rotation case.
**Grounding:** `Understanding/Trees/AVLTrees.ipynb` — the audit verified it textbook-perfect; balance-factor explanations must match it.
**Verify:** skill checklist; rotation case labels match corrected B10 text.

### C7 — B-Trees
**New route:** `/b-tree`.
**Videos → maps:** BTreeScene (the only sourceable scene).
**Note:** `BTree.mp4` is a lost source (audit 03 §5) — page ships without it; add a "coming" note, no fake content.
**Verify:** skill checklist.

### C8 — Graphs I (types & representations)
**New routes:** `/types-of-graphs`, `/graph-representation`.
**Videos → maps:** UndirectedGraphs, DirectedGraphs, WeightedUDGraphs, WeightedDGraphs → types-of-graphs (4 videos); the 8 adjacency scenes (post-R6 names) → graph-representation (multi-video, grouped U/D then weighted).
**Grounding:** `Understanding/Graphs/Graphs.ipynb` (matrix/list representations, memory trade-offs).
**Verify:** skill checklist; adjacency page uses corrected (B11) tuple visuals language.

### C9 — Graphs II (traversals)
**New route:** `/graph-traversals`.
**Videos → maps:** UndirectedGraphBFS/DFS, DirectedGraphBFS/DFS (4 videos).
**Grounding:** `Graphs.ipynb`; complexity claims (O(V+E)) verified against notebook.
**Verify:** skill checklist.

### C10 — Graphs III (shortest paths)
**New routes:** `/dijkstra-algorithm`, `/bellman-ford-algorithm`, `/floyd-warshall-algorithm`.
**Videos → maps:** Dijkstra, BellmanFord, FloydWarshall (1:1).
**Grounding:** `Graphs.ipynb` (Dijkstra, Bellman-Ford incl. negative-cycle note, Floyd-Warshall). State Bellman-Ford's negative-cycle detection honestly — the animation skips the V-th iteration (audit 05 §3); describe it as future work on the page.
**Verify:** skill checklist.

### C11 — Graphs IV (MCST & topo sort)
**New routes:** `/prims-algorithm`, `/kruskal-algorithm`, `/topological-sort`.
**Videos → maps:** PrimsMCST, KruskalMCST, TopologicalSort (1:1).
**Grounding:** `Graphs.ipynb` (heap-Prim's, rank-Kruskal, Kahn's).
**Verify:** skill checklist.

### C12 — Divide & Conquer
**New routes:** `/count-inversions`, `/closest-pair-of-points`, `/longest-common-subsequence`, `/median-of-medians` + a new sidebar section for D&C.
**Videos → maps:** CountInversions, ClosestPairPoint, LongestCommonSubsequence, MedianOfMedians (1:1).
**Grounding:** `Animations/DivideAndConquer.py` demo inputs; recurrence/master-theorem content must be CORRECT this time (audit 04 §3 found the old DSA page mangled — fixed in B6; keep new pages accurate).
**Verify:** skill checklist.

### C13 — Greedy
**New routes:** `/interval-scheduling`, `/huffman-encoding` + new sidebar section.
**Videos → maps:** IntervalScheduling, HuffmanEncoding (1:1).
**Grounding:** `Animations/Greedy.py`; Huffman page notes the animation builds the tree (codes display = future work, per audit 05 §3).
**Verify:** skill checklist.

### C14 — Navigation sweep (un-hide + footer)
Agent: dsa-page-builder · Depends: C1–C13 · Size: M
**Do:** Unhide the Trees/Heaps/Graphs sections (hidden in B3); point every sidebar link at the new kebab routes; replace all 27 footer no-href placeholders with real `url_for` links (dead ones → nearest real page or remove honestly); data_structures.html "coming soon" texts → real links; home-page Explore buttons → wired to section pages.
**Verify:** link checker with **empty allowlist**; manual nav pass.
**Done when:** zero dead links repo-wide.

### C15 — Phase gate
Agent: dsa-auditor · Depends: C14 · Size: M
**Do:** Full sweep: route smoke (all routes incl. new), link checker, sync `check`, spot-watch 6 videos across topics against their highlighting, verify accuracy of complexity claims on 4 random new pages against notebooks.
**Done when:** auditor verdict + blockers list; TASKBOARD updated.

### Phase 4 exit gate

- [ ] Every topic from audit 05 §3 has a page; ~56 videos live
- [ ] All maps machine-generated; `tools.syncmap check` green
- [ ] Sidebar + footer fully wired; link checker allowlist empty
- [ ] Auditor sign-off
