# Implemented but Can Be Improved

> Full-repository audit of **DSA-Animations** (commit `13f4b33`).
> Items below work, but have quality issues that should be addressed before the project scales.

## 1. Code Duplication (Manim animations)

| # | Issue | Location(s) | Improvement |
|---|---|---|---|
| 1 | **Massive copy-paste of BFS/DFS animation boilerplate** — the same ~90-line while-loop exists 6× (tree + directed/undirected graph, queue/stack variants) | `Animations/Trees.py:285-341`, `:395-451`; `Animations/Graphs.py:365-427`, `:469-531`, `:746-808`, `:850-912` | Extract a shared `animate_traversal(adj, structure)` helper |
| 2 | **`ListElement` class implemented 3×** (non-VGroup ×2, VGroup ×1) | `Animations/SearchingAlgorithms.py:9-33`, `Animations/SortingAlgoritms.py:7-31`, `Animations/Arrays.py:13-31` + variant in `DivideAndConquer.py:9-35` | Move to a shared module (like `env_config.py`) |
| 3 | **`Node(VGroup)` class implemented 4×** nearly identically | `Arrays.py:33-48`, `Trees.py:14-35`, `Graphs.py:10-25`, `AVLTree.py:14-35` (`NodeVisual`), `SortingAlgoritms.py:540-561` | Same |
| 4 | **`WeightedLine` duplicated** | `Graphs.py:28-87`, `Greedy.py:138-186` (slightly different bg handling) | Merge into one |
| 5 | **`playSurroundingNodeAnimation` helper copy-pasted into 3 scenes** | `Trees.py:40-48`, `:846-854`, `:939-947`, `:1025-1033` | Scene mixin |
| 6 | **~55-line "find mobject line connecting two nodes & fade it" block duplicated 5×** inside BST deletion | `Trees.py:1688-1704`, `:1735-1751`, `:1754-1769`, `:1811-1827`, `:1830-1845`, `:1936-1952`, `:1960-1975` | One `remove_edge_visual(parent, child)` function |
| 7 | **`make_dynamic_bezier_updater` + `make_arrowhead_updater` copy-pasted into all 7 LinkedList scenes** | `LinkedList.py:145-160`, `:226-242`, `:308-324`, `:396-412`, `:523-538`, `:639-654`, `:957-981` | Module-level helper |
| 8 | **Huffman algorithm runs twice** — once to build the graph, once again in the animation (must be manually kept in sync) | `Greedy.py:230-289` vs `:371-463` | Single pass, emit animation events |
| 9 | **LCS backtracking duplicated** in `construct()` and `LCS()` | `DivideAndConquer.py:613-623` vs `:747-772` | Return both from one function |

## 2. Structure & Naming

| # | Issue | Location(s) | Improvement |
|---|---|---|---|
| 10 | **Monolithic files** — `Graphs.py` 2229 ln / `Trees.py` 2195 ln / `AVLTree.py` 1739 ln; 22 scenes in one file | `Animations/*.py` | Split per-topic or per-scene |
| 11 | **"SortingAlgoritms" typo** in folder, file name, media paths, gifs path, and converter's category list | `Animations/SortingAlgoritms.py`, `Animations/media/videos/SortingAlgoritms/`, `gifs/SortingAlgoritms/`, `mp4_to_gif_converter.py:56` | Rename to `SortingAlgorithms` (website already uses correct spelling) |
| 12 | **"Adjecency" typo** in 8 scene/class names + rendered titles; "Prims's Algorithm" footer typo; "egde" in on-screen text | `Graphs.py:171-1157` (class names), `:206`, `:666`, `:1094`, `:1330` (titles), `:1932` ("egde"), `Website/website/templates/base.html:184` ("Prims's") | Fix spelling in rendered strings at minimum |
| 13 | **Notebook typos** — `WieghtedDirectedGraph` / `WieghtedUndirectedGraph` (should be "Weighted"), `AMGaphD` | `Understanding/Graphs/Graphs.ipynb` cells 12/14/7 | Fix names |

## 3. Code Hygiene (Python)

| # | Issue | Location(s) | Improvement |
|---|---|---|---|
| 14 | **Debug `print()` left in animation code** (case prints, per-insert print) | `AVLTree.py:293, 297, 301, 307, 381` | Remove or route through `logging` |
| 15 | **`BTrees.py` hijacks the root logger & writes `btree_operations.log` into the source tree at import time**, ~90 verbose log calls (INFO never emits due to level=WARNING) | `BTrees.py:6-23` + throughout | Guard behind `if __name__`, log to temp, drop verbosity |
| 16 | **Commented-out code blocks left in scenes** | `Arrays.py:229-233`, `Stack-Queue.py:243-248`, `Trees.py:2121`, `Graphs.py:131-142`, `:994-995`, `:1025-1036`, `:1230-1231`, `:1570-1572`, `:1991` (`# print(minCost)`), `DivideAndConquer.py:436-437`, `:440`, `:522` (`#print(Px,Py)`) | Delete |
| 17 | **Unused imports** in most scene files (`Percent`, `Pixels`, `CurvedArrow`) | `SearchingAlgorithms.py:2-3`, `Arrays.py:2-3`, `Stack-Queue.py:2`, `LinkedList.py:2`, `Trees.py:2`, `AVLTree.py:2`, `Greedy.py:2` | Remove; add ruff/flake8 |
| 18 | **Mid-file `import` statements & re-definitions** | `SortingAlgoritms.py:535` (`import networkx`), `:537-538` (re-defines `EDGE_COL`/`NODE_COL` already in `env_config`), `DivideAndConquer.py:268` | Move to top; delete redefs |
| 19 | **Loop variable shadowing** — inner `for i in range(num_objects-1)` overwrites outer `i`; `_` used as index (`nodes[_]`) | `LinkedList.py:703/745`, `Graphs.py:105-107`, `:547-548`, `:999-1000`, `:1235-1236` | Rename |
| 20 | **`random.randint(1000,9999)` fake addresses can collide** between nodes (fixed seed saved it) | `LinkedList.py:17`, `:790` | Use a counter/UUID |
| 21 | **Prim's uses `try/except KeyError` for undirected edge-key lookups**; maintains a `distance` dict that is written but never read for selection | `Graphs.py:1940-1947`, `:1962-1971`, `:1986-1988` | Normalize keys once; drop dead dict |
| 22 | **Inconsistent color constants** — raw `BLACK`/`WHITE` instead of `TEXTCOL`/theme constants in Greedy | `Greedy.py:32`, `:42`, `:360`, `:399`, `:420`, `:438` | Use constants |
| 23 | **MaxHeap vs MinHeap on-screen comparison text uses opposite operand order** | `Trees.py:1239` vs `:1341` | Unify |
| 24 | **`highlight_subtree(... font="Arial", fsize=24)` default args** contradict project font and are never exercised | `Trees.py:873`, `:967` | Remove misleading defaults |
| 25 | **`BTreeScene` has no real animations** — tree updates happen synchronously between 2-second waits (slideshow effect, not animation) | `BTrees.py:450-475` | Add transforms between rebuilds |

## 4. Flask App

| # | Issue | Location(s) | Improvement |
|---|---|---|---|
| 26 | **Hard-coded `SECRET_KEY`** | `Website/website/__init__.py:11` (`'my_secret_key'`) | Load from env var |
| 27 | **DB path depends on `os.getcwd()`** and mixes `/` and `\` in the sqlite URI | `__init__.py:12, 37` | Use `os.path.dirname(__file__)` / `instance_path` |
| 28 | **Debug prints & commented-out code** | `__init__.py:41, 43` ("Created Database!"), `auth.py:53` | Remove |
| 29 | **No `@login_required` on any content route; `subscribed` column never used after signup** | `views.py` (all), `models.py:9` | Protect content or drop the flag; wire newsletter via Flask-Mail (installed but unused) |
| 30 | **`User.query.get(int(id))`** — legacy API, deprecation warning under Flask-SQLAlchemy 3.1 | `__init__.py:32` | `db.session.get(User, id)` |
| 31 | **URL routes contain literal spaces** (`/data structures`, `/2D arrays`, `/bubble sort`) — work but produce `%20` URLs and are unusual | `views.py:14, 26, 30, …` | Kebab-case + `url_for` everywhere (some templates hardcode `/...` paths instead of `url_for`) |

## 5. Website UI

| # | Issue | Location(s) | Improvement |
|---|---|---|---|
| 32 | **Zero responsive design** — no `@media` queries at all; fixed 310px cards, 12.5rem carousel padding; carousel drag uses mouse events only (no touch) | `Website/website/static/styles.css` (whole file), `templates/home.html:542-571` | Add breakpoints + Pointer Events |
| 33 | **Fonts referenced but never loaded** — `Roboto`, `"JetBrains Mono"`, `Arial` (no webfont link) — silently falls back | `styles.css:87`, `:387`, `:441`, `:489`, `:661` | Add font link or system stack |
| 34 | **`highlightMap`s are hand-synced** by re-simulating every animation `run_time` in a notebook — any timing tweak in a manim scene silently desyncs website highlighting | `utils/createHighlightMap.ipynb` + all topic templates | Auto-generate from scene logs |
| 35 | **Sidebar `<details>` all `open` by default** — huge always-expanded nav | `templates/content.html:5-99` | Collapse non-active sections |
| 36 | **No favicon, no meta description, generic `<title>`** ("DSA Animation" default; algorithms page titled "DSA") | `base.html:56`, `templates/DSA/algorithms.html:1` | Add favicon + per-page titles |

## 6. Project / Engineering

| # | Issue | Location(s) | Improvement |
|---|---|---|---|
| 37 | **Requirements not pinned; no `requirements.txt` for the main project** — manim/flask deps nowhere declared | `requirements_converter.txt:2-3` (`moviepy>=1.0.3`, `tqdm>=4.64.0`) | Pin versions (`manim==0.19.0`, `flask==3.0.3`, …) in a root `requirements.txt` |
| 38 | **~1.09 GiB of git objects from committed binaries**: 73 mp4s (432 MB), 72 gifs (986 MB), 16 webm (33 MB), `Website/database.db` | `git count-objects -vH`; `Animations/media/videos/**`, `gifs/**`, `Website/website/static/Videos/**` | Move media to Git LFS or Releases; untrack DBs |
| 39 | **No tests, no CI, no linter config anywhere** | repo-wide | pytest for notebooks' algorithm code; GitHub Actions render smoke-test |
| 40 | **Notebook Dijkstra neighbor test `adj_matrix[u][v] > 0` treats `np.inf` (non-edge) as a valid neighbor** — works only because `dist + inf` never improves anything | `Understanding/Graphs/Graphs.ipynb` cell 12 | Test `< np.inf` instead |
