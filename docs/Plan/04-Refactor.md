# 04 — Phase 3: Refactor (behavior-preserving)

**Objective (Goal G1 "cleaner & scalable"):** pay down the duplication/dead-code debt from `docs/Audit/02` + `03` with **zero behavior change**, proven by the Phase 2 timeline oracle.
**Preconditions:** Phase 2 (T7 baselines committed). **Parallelizable:** R1–R5 mostly independent per-file; R6 needs coordination with RB2.

The `dsa-refactorer` agent runs every card: baseline check → mechanical change → snapshot re-check (byte-identical unless the card lists expected text diffs) → dsa-verify.

### R1 — `Animations/common.py`: shared visual classes
Agent: dsa-refactorer · Depends: — · Size: L
**Problem** (audit 02 §1): `ListElement` ×3 (+1 variant), `Node`/`NodeVisual` ×4, `WeightedLine` ×2, `playSurroundingNodeAnimation` ×3, bezier/arrowhead updater helpers ×7 copies.
**Do:** Create `Animations/common.py` (alongside `env_config.py`) with one implementation of each, parameterized for the small variants (bg handling in `WeightedLine`, fonts in `ListElement`). Migrate all usages file-by-file: `SearchingAlgorithms.py`, `SortingAlgoritms.py`, `Arrays.py`, `DivideAndConquer.py`, `Trees.py`, `Graphs.py`, `AVLTree.py`, `Greedy.py`, `LinkedList.py`.
**Verify:** snapshot diff = byte-identical for every touched scene; spot-render ONE migrated scene (e.g. `BubbleSort`) and compare visually.
**Done when:** duplicates deleted; oracle green.

### R2 — Traversal animation helper
Agent: dsa-refactorer · Depends: — · Size: M
**Problem** (audit 02 §1): ~90-line BFS/DFS while-loop block ×6 (`Trees.py:285-341,395-451`; `Graphs.py:365-427,469-531,746-808,850-912`).
**Do:** `animate_traversal(...)` in `common.py` taking the varying parts (adjacency structure, container type, labels/positions, callback hooks). Migrate the 6 sites.
**Verify:** oracle byte-identical.
**Done when:** 6 sites collapsed; oracle green.

### R3 — BST edge-removal helper
Agent: dsa-refactorer · Depends: — · Size: M
**Problem** (audit 02 §1): ~55-line "find connecting line & fade" block ×5 in `Trees.py` BST deletion (`:1688-1704`, `:1735-1751`, `:1754-1769`, `:1811-1827`, `:1830-1845`, plus `:1936-1952`, `:1960-1975` variants).
**Do:** `remove_edge_visual(parent, child)` helper; migrate all sites.
**Verify:** oracle byte-identical.
**Done when:** blocks collapsed.

### R4 — Dead-code & hygiene sweep
Agent: dsa-refactorer · Depends: — · Size: M
**Problem** (audit 03 §2 + 02 §3): unused `insert_into_AVLTree`/`insert` (`AVLTree.py:1551-1611`), `reconnect_after_rotation` (`:1545-1549`), `remove_keys_after` (`BTrees.py:188-191`), dead Prim's `distance` dict (`Graphs.py:1919-1930,1986-1988`), ghost networkx graphs in heap scenes (`Trees.py:1262,1364`), dead `hasattr` (`Greedy.py:393`), dup assignments (`Trees.py:1390-1394`; `AVLTree.py:282-285`), debug prints (`AVLTree.py:293-307,381`), commented-out code (audit 02 item 16 list), unused imports (audit 02 item 17), mid-file imports/redefs (`SortingAlgoritms.py:535-538`, `DivideAndConquer.py:268`), loop-var shadowing (`LinkedList.py:703/745`, `Graphs.py:105-107,547-548,999-1000,1235-1236`).
**Do:** Remove all listed items. Nothing else.
**Verify:** oracle byte-identical (dead code by definition can't affect timelines); pytest green.
**Done when:** every listed item gone.

### R5 — BTrees logger fix
Agent: dsa-refactorer · Depends: — · Size: S
**Problem** (audit 02 §3): `BTrees.py:6-23` hijacks root logger at import, writes `btree_operations.log` into source tree.
**Do:** `if __name__ == "__main__"` guard or module-level `logger = logging.getLogger(__name__)` without side effects; drop INFO-level noise; no file handler by default.
**Verify:** `import` of the module creates no files, prints nothing.
**Done when:** clean import.

### R6 — Typo renames (visual diffs expected)
Agent: dsa-refactorer · Depends: R1 · Size: M · **Queues render batch RB2**
**Problem** (audit 02 §2): `SortingAlgoritms` file/folder/category typo; `Adjecency` in 8 scene class names + rendered titles; "Prims's" footer; `AVLNode(value: int)` constructed with strings.
**Do:**
- `git mv Animations/SortingAlgoritms.py Animations/SortingAlgorithms.py`; `git mv Animations/media/videos/SortingAlgoritms Animations/media/videos/SortingAlgorithms`; update `mp4_to_gif_converter.py:56` category list; grep all usages (media paths, docs, TASKBOARD refs).
- Rename the 8 `Adjecency*` classes → `Adjacency*` AND fix the on-screen title strings (`Graphs.py:206,666,1094,1330`), "egde"→"edge" if not already done in B11.
- `base.html:184` "Prims's Algorithm" → "Prim's Algorithm".
- `AVLTree.py` `self.value: int` → `str | int` (matches actual usage).
**Verify:** usage inventory in report; snapshots show only the expected on-screen text diffs (list them); RB2 queued for the 8 adjacency scenes (titles changed).
**Done when:** renames complete; expected-diff list matches snapshots.

### R7 — Flask cleanups
Agent: dsa-refactorer · Depends: — · Size: S
**Problem** (audit 02 §4): legacy `User.query.get` (`__init__.py:32`) → `db.session.get`; hardcoded template paths instead of `url_for` (sweep); routes-with-spaces get kebab-case **aliases** (D1 — stack extra decorators, e.g. `@views.route("/linked-list")` alongside `@views.route("/linked list")`).
**Do:** As listed. Templates: replace hardcoded `/xyz` hrefs with `url_for`.
**Verify:** pytest routes green for BOTH alias sets; link checker green.
**Done when:** legacy + kebab both resolve; no hardcoded hrefs.

### R8 — Ruff full pass
Agent: dsa-refactorer · Depends: R1–R7 · Size: M
**Do:** `ruff check Animations Website tools *.py` → fix all findings (unused imports will mostly be gone via R4); `ruff format` only on files already touched by this phase (no repo-wide reformat noise).
**Verify:** `ruff check` clean; oracle byte-identical (formatting can't change timelines).
**Done when:** clean lint.

### R9 — (Stretch, optional) Huffman single-pass
Agent: dsa-refactorer · Depends: R1 · Size: M
**Problem** (audit 02 §1): `Greedy.py` runs the algorithm twice (graph build + animation).
**Do:** One pass emitting animation events. **Skip if timeline diff can't be kept byte-identical** — then it becomes a future card.
**Verify:** oracle + spot-render.
**Done when:** merged or explicitly deferred with reason.

### RB2 — Render batch (graph titles)
Agent: general · Skill: dsa-render · Depends: R6 · Size: M
**Do:** Render at `-ql`: the 8 renamed adjacency scenes (titles changed on-screen: `AdjacencyMatrixUD`, `AdjacencyListUD`, `AdjacencyMatrixD`, `AdjacencyListD`, `WeightedAdjacencyMatrixUD`, `WeightedAdjecencyListUD`→`WeightedAdjacencyListUD`, etc.). Spot-check titles.
**Done when:** 8 scenes re-rendered with corrected titles.

### Phase 3 exit gate (dsa-auditor)

- [ ] Every touched scene: snapshot byte-identical (or expected-diff list from R6/RB2 only)
- [ ] `ruff check` clean; pytest + link checker green
- [ ] Duplicated classes/blocks from audit 02 §1 gone (grep proves single definitions in `common.py`)
- [ ] All 25 original routes + new kebab aliases resolve
