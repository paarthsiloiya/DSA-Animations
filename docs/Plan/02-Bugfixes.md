# 02 — Phase 1: Bugfixes

**Objective:** kill every defect from `docs/Audit/04-Bugs.md` + copy/content defects, with minimal diffs. Manim visual fixes are **queued for render batch RB1**, not rendered per-card.
**Preconditions:** Phase 0. **Parallelizable:** B1–B4, B5–B9, B10–B17 are three independent streams; cards within a stream are sequential-ish but mostly independent (different files).

### B1 — Flask config hardening 🔴
Agent: dsa-bugfixer · Depends: — · Size: M
**Problem** (audit 04 §2): DB path is cwd-dependent (`__init__.py:12,37`) — broken on Linux, created `website/database.db` artifact on Windows; `SECRET_KEY` hardcoded (`:11`); debug prints (`:41,43`, `auth.py:53`); `Website/database.db` tracked in git.
**Do:**
- `SECRET_KEY = os.environ.get("DSA_SECRET_KEY", "dev-only-insecure-key")`
- DB: `os.makedirs(app.instance_path, exist_ok=True)`; URI → `sqlite:///{os.path.join(app.instance_path, 'database.db')}` (use `pathlib`, forward slashes in URI)
- Remove prints + commented code; `git rm --cached Website/database.db`; `.gitignore` `*.db` and `instance/` (check with user whether any real user data lives in the old DB — audit says schema-only)
**Verify:** dsa-verify + `python main.py` from both repo root and `Website/` — DB lands in `Website/instance/` both times; site works; old URLs still resolve.
**Done when:** audit 04 §2 rows all re-verified fixed.

### B2 — Static video path casing 🟠
Agent: dsa-bugfixer · Depends: — · Size: S
**Problem** (audit 04 §2): 8 templates reference `videos/` lowercase; real dir is `Videos/` — 404 on Linux/CI.
**Do:** In `linear_search.html:47`, `bubble_sort.html:53`, `heap_sort.html:78`, `insertion_sort.html:63`, `merge_sort.html:89`, `quick_sort.html:83`, `selection_sort.html:59`, `stack.html:94`: `videos/` → `Videos/`.
**Verify:** grep zero lowercase refs remain; test client GET one video URL → 200; CI (Linux) green.
**Done when:** all references exact-case.

### B3 — Dead-nav honesty pass 🟡
Agent: dsa-bugfixer · Depends: F3 · Size: M
**Problem** (audit 04 §1): 17 sidebar links + `/rotation` + 27 footer links point nowhere.
**Do:** Until P4 creates the pages: hide the Trees/Heaps/Graphs sidebar `<details>` sections and the footer link-list block (`hidden` attribute — keep markup for P4 to re-enable), add a small "More topics coming soon" note in the sidebar. Remove those entries from the F3 allowlist.
**Verify:** link checker green with allowlist shrunk accordingly; pages visually clean (no orphan "coming soon" dupes).
**Done when:** zero user-clickable dead links on the site.

### B4 — Broken relative links 🟡
Agent: dsa-bugfixer · Depends: F3 · Size: S
**Problem** (audit 04 §1): `DSA/data_structures.html` 8 relative hrefs (`Arrays`, `Linked%20Lists`, `Stacks`, `Queues`, `Trees`, `Hash%20Tables`, `Graphs`, `Union-Find`) → 404s; `algorithms.html:268` `Sorting%20Algorithms`; `linked_list.html:124` links to a `.md` file.
**Do:** Replace existing-topic links with `url_for`; topics without pages yet (Trees, Hash Tables, Graphs, Union-Find) become plain text with a "coming soon" style; the `.md` link → `url_for('views.doubly_linked_list')`. Update allowlist.
**Verify:** dsa-verify; link checker.
**Done when:** no unresolved hrefs in these files.

### B5 — Binary-search sample code 🔴
Agent: dsa-bugfixer · Depends: — · Size: S
**Problem** (audit 04 §3): `binary_search.html:48-51` — unsorted array + `high = N` off-by-one.
**Do:** Fix the displayed code: sorted array (matching the video's demo `[1,2,3,4,5,6]`), `high = len(arr) - 1`. Adjust the page's inline `highlightMap` if line indices shifted (lines are few; recheck against the video timeline).
**Verify:** code renders correctly; map still highlights sanely against video (watch once).
**Done when:** sample is correct Python; highlighting follows.

### B6 — Complexity & math corrections 🔴
Agent: dsa-bugfixer · Depends: — · Size: M
**Problem** (audit 04 §3): wrong claims in `sorting_algorithms.html:91,96,103` (Insertion "O(n)", Selection "$O(n)$", Quick worst "$O(n)$"), `insertion_sort.html:266` (exponent dropped), `dsa.html:113-114` ($O(n^2)$ mangled), `algorithms.html:175,225-226` (master-theorem mangled), `linear_search.html:116-119,140-142` (Θ vs O; "quadratic function" false).
**Do:** Correct each claim to textbook values (verify against `Understanding/*.ipynb`): Insertion avg/worst O(n²) best O(n); Selection O(n²); Quick worst O(n²) avg O(n log n); master theorem Θ(n³) with n³ dominating; linear search avg Θ(n), Θ is tight (O is the upper bound).
**Verify:** every changed claim cross-checked against a notebook or CLRS; MathJax renders.
**Done when:** audit rows re-verified fixed.

### B7 — Copy defects batch 🟠/🟡
Agent: dsa-bugfixer · Depends: — · Size: M
**Problem** (audit 04 §3): `stack.html:85` (`s.push(data):` syntax) + `:101-112` floating `<li>`; `2Darrays.html:28` (`A` → `A[0][0]`); `signup.html:27-29` ("LogIn" → "Sign Up"); `algorithms.html:1` (title "DSA"); `home.html:49` ("Feature Topics"), `:429-433` (duplicate card description); `singly_linked_list.html:604,616` (delete map labeled "insertNode"); AI meta-text in `arrays.html:28-32`, `2Darrays.html:13,31`, `linked_list.html:19,108`, `sorting_algorithms.html:123-124,194`, `heap_sort.html:125`.
**Do:** Fix each; rewrite AI-meta sentences into direct prose (no "the sources…").
**Verify:** pages render; no meta-text remains (grep "the sources", "given sources").
**Done when:** all rows fixed.

### B8 — Home-page honesty 🟡
Agent: dsa-bugfixer · Depends: — · Size: S
**Problem** (audit 04 §3): fake ratings "4.6 (1.2k)"; "Pause, play, speed up, or step through" claim with no such controls.
**Do:** Remove invented ratings; reword the interactivity card to describe what exists (video playback controls) until P5 possibly adds real interactivity.
**Verify:** home renders; no false claims.
**Done when:** done.

### B9 — CSS defects 🟡
Agent: dsa-bugfixer · Depends: — · Size: S
**Problem** (audit 04 §4): `styles.css:565-567` wrong selector (`.carousel` → `.topic-carousel`); `:125` invalid `justify-content: flex;` (inspect rule intent — likely `space-between` or remove); `:556,560` duplicate `scrollbar-width`.
**Verify:** carousel scrollbar hidden in a WebKit browser; CSS parses with no dropped declarations.
**Done when:** rows fixed.

### B10 — Manim: AVL LeftLeft label 🔴
Agent: dsa-bugfixer · Depends: — · Size: S · **Queues render RB1**
**Problem** (audit 04 §5): `AVLTree.py:646` shows "Left Rotation" while performing a right rotation.
**Do:** Label → "Right Rotation" (docstring at `:541` already says so).
**Verify:** read diff; queue RB1.
**Done when:** diff correct.

### B11 — Manim: Graphs correctness 🟠
Agent: dsa-bugfixer · Depends: — · Size: M · **Queues render RB1**
**Problem** (audit 04 §5): `Graphs.py:1809` Floyd-Warshall `range(1, len(vertices))` skips vertex 0 (notebook is correct); `:1192-1193` + `:1419` adjacency lists store unordered sets `{v, w}` (braces visible in videos, hash-order instability) → tuples; `:1932` "egde" typo.
**Do:** `k` loop from 0; sets → tuples `(v, w)` rendered appropriately; typo fix.
**Verify:** diff review; queue RB1 (FloydWarshall + both WeightedAdjecencyList scenes).
**Done when:** rows fixed.

### B12 — Manim: QuickSort base-case guard 🟠
Agent: dsa-bugfixer · Depends: — · Size: S
**Problem** (audit 04 §5): `SortingAlgoritms.py:416-419` marks `arr[low]` when `low > high` — IndexError if `low == len(arr)`.
**Do:** Guard `if low <= high:` for the arrow-marking block. Demo input's visuals unchanged.
**Verify:** code path reasoning; no render needed (timeline identical for demo input — confirm via snapshot once P2 lands).
**Done when:** guard correct.

### B13 — Manim: Heap visuals 🟠
Agent: dsa-bugfixer · Depends: — · Size: M · **Queues render RB1**
**Problem** (audit 04 §5): `Trees.py:1196-1197` (MaxHeap) + `:1298-1299` (MinHeap) zero-length Line + self-loop `G.add_edge(v, v)` when parent_index = -1; `:1239`/`:1341` wrong comparison text when a value bubbles to root.
**Do:** Skip edge/line when `parent_index < 0`; guard the comparison text (skip when at root).
**Verify:** diff; queue RB1 (MaxHeap, MinHeap).
**Done when:** rows fixed.

### B14 — Manim: D&C latent crashes 🟠
Agent: dsa-bugfixer · Depends: — · Size: M · **Queue render RB1 (IntervalScheduling? no — this is D&C; LCS/ClosestPair affected)**
**Problem** (audit 04 §5): `DivideAndConquer.py:553-554` LCS table only builds when both strings equal length (crashes otherwise); `:465-469` closest-pair strip misses pairs `(Sy[0], Sy[k>1])`; `:391-404` NameError-prone `fade_in/fade_out` conditional + duplicated arg.
**Do:** LCS: raise clear `ValueError` if lengths differ (documented demo constraint) — full generalization is a future card; strip check: seed correctly and iterate all pairs within window; restructure 391-404 so `fade_in/fade_out` are always defined and used once.
**Verify:** diff; queue RB1 (LongestCommonSubsequence, ClosestPairPoint).
**Done when:** rows fixed; no behavior change for demo inputs.

### B15 — Manim: Greedy label shift 🟡
Agent: dsa-bugfixer · Depends: — · Size: S · **Queues render RB1**
**Problem** (audit 04 §5): `Greedy.py:74-81` vs `:63-65` interval ruler labels shifted one unit.
**Do:** Align tick `i` label with interval positions.
**Verify:** diff; queue RB1 (IntervalScheduling).
**Done when:** row fixed.

### B16 — Converter fixes 🟠
Agent: dsa-bugfixer · Depends: F1 · Size: S
**Problem** (audit 04 §6): moviepy 2.x import vs `>=1.0.3` requirement; `clip.resize` gone in 2.x → `--resize` crashes; no try/finally close; naive `.replace(".mp4", ".gif")`.
**Do:** `requirements_converter.txt` → `moviepy>=2.0,<3.0`; `resize(...)` → `resized(...)`; wrap convert in try/finally `clip.close()`; `Path.with_suffix(".gif")`.
**Verify:** run a real conversion of one mp4 to a temp dir with and without `--resize`.
**Done when:** works on installed moviepy 2.2.1.

### B17 — Notebook fixes 🟡
Agent: dsa-bugfixer · Depends: — · Size: S
**Problem** (audit 04 §5): `Graphs.ipynb` Dijkstra treats `inf` as neighbor + `Wieghted*` typos; `Trees.ipynb` heap `delete` crashes on single-node heap.
**Do:** neighbor test `< np.inf`; rename typos; guard `parent_of_last is None`.
**Verify:** execute both notebooks end-to-end.
**Done when:** notebooks run clean.

### RB1 — Render batch (after B10–B15 land)
Agent: general · Skill: dsa-render · Depends: B10, B11, B13, B14, B15 · Size: M
**Do:** Render at `-ql`: `LeftLeftCase`, `FloydWarshall`, `WeightedAdjecencyListUD`, `WeightedAdjecencyListD`, `MaxHeap`, `MinHeap`, `LongestCommonSubsequence`, `ClosestPairPoint`, `IntervalScheduling`. Spot-check each changed segment. Committing rendered mp4s needs explicit user approval (D7) — default: render locally, update site-bound webms only if those scenes are already on the site (they're not yet — P4 converts from whatever's newest).
**Verify:** watch each; `docs/Audit` bug claims about on-screen text no longer reproducible.
**Done when:** batch rendered + spot-checked.

### Phase 1 exit gate (run dsa-auditor)

- [ ] Every row of `docs/Audit/04-Bugs.md §1–§4` re-verified fixed
- [ ] §5 manim rows fixed in source; RB1 rendered
- [ ] Link checker green with shrunken allowlist; pytest green
- [ ] No behavior lost: all 25 routes live, videos still play
