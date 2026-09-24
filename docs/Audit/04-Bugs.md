# Bugs

> Full-repository audit of **DSA-Animations** (commit `13f4b33`).
> Severity: 🔴 high · 🟠 medium · 🟡 low. Confidence: ✅ verified (reproduced / logic-proven / checked against installed libraries) · ⚠️ high-likelihood.

## 1. Broken Links / Routes (all 🔴 ✅ — every target checked against `views.py`)

| Bug | Location | Why it's a bug |
|---|---|---|
| `/rotation` link → 404 | `Website/website/templates/content.html:56` | No `/rotation` route exists; rotation page never built |
| **17 sidebar links to nonexistent routes** (`/types_of_trees`, `/properties_of_trees`, `/traversal`, `/breadth_first_search`, `/depth_first_search`, `/list_tree_correlation`, `/binary_search_tree`, `/ternary_tree`, `/avl_tree`, `/types_of_heaps`, `/properties_of_heap`, `/types_of_graphs`, `/graph_representation`, `/dijkstra_algorithm`, `/floyd_warshall_algorithm`, `/bellman_ford_algorithm`, `/prims_algorithm`, `/kruskal_algorithm`) | `content.html:63-97` | Flask returns 404 — Trees/Heaps/Graphs sidebar sections are dead nav |
| 8 broken **relative** links: `href="Arrays"`, `"Linked%20Lists"`, `"Stacks"`, `"Queues"`, `"Trees"`, `"Hash%20Tables"`, `"Graphs"`, `"Union-Find"` | `templates/DSA/data_structures.html:40, 61, 87, 105, 126, 177, 199, 230` | Resolve to `/Arrays`, `/Stacks`, … — routes are lowercase & different (`/arrays`, `/stack`); several targets don't exist at all (Trees, Hash Tables, Graphs, Union-Find) |
| `href="Sorting%20Algorithms"` (capitalized, relative) | `templates/DSA/algorithms.html:268` | Resolves to `/Sorting%20Algorithms` → 404 (route is `/sorting algorithms`) |
| **`href="Doubly%20Linked%20Lists.md"`** — link to a nonexistent Markdown file | `templates/LinkedList/linked_list.html:124` | Should be `url_for('views.doubly_linked_list')`; the `.md` target exists nowhere in the repo |
| 27 footer `<a>` tags with **no href** | `templates/base.html:120-186` | Not clickable — dead UI |

## 2. Flask App Defects

| Bug | Location | Severity | Why |
|---|---|---|---|
| **DB path is cwd-dependent and broken per the README's own instructions.** URI = `sqlite:///{cwd}/Website/database.db`. README says `cd Website` → `python main.py`, producing `…/Website/Website/database.db`. On **Windows** it silently resolves case-insensitively into the *package* folder `Website\website\` — which is exactly why an untracked `Website/website/database.db` exists. On **Linux/case-sensitive FS** SQLite fails to open. | `Website/website/__init__.py:12, 37`; `README.md:29-35` | 🔴 ✅ | Wrong base dir; also mixes OS separators in the URI |
| **8 templates reference static videos with lowercase `videos/`** while the actual folder is `Videos/` (`url_for('static', filename='videos/…')`) | `linear_search.html:47`, `bubble_sort.html:53`, `heap_sort.html:78`, `insertion_sort.html:63`, `merge_sort.html:89`, `quick_sort.html:83`, `selection_sort.html:59`, `stack.html:94` | 🟠 ✅ | Works on Windows (case-insensitive), **404s for the video on Linux deployments**; the other 6 templates use `Videos/` — inconsistent |
| `SECRET_KEY = 'my_secret_key'` hard-coded | `__init__.py:11` | 🟠 | Session-signing key public in repo |
| Tracked SQLite DB with schema (potential user data) committed | `Website/database.db` (git) | 🟠 | DB artifacts shouldn't be versioned |

## 3. Website Content / Code-Sample Defects (user-facing)

| Bug | Location | Severity |
|---|---|---|
| **Binary search sample code is wrong twice:** runs on an **unsorted** array `[5,2,4,6,3,1]` *and* is called with `high = N` (off-by-one; `x > all elements` ⇒ `arr[N]` IndexError) | `templates/SearchingAlgorithms/binary_search.html:48-51` | 🔴 |
| **Syntax error in displayed code:** `s.push(data):` — trailing colon | `templates/StackAndQueue/stack.html:85` | 🔴 |
| Wrong complexity claims: Insertion Sort "typically **O(n)**" (should be O(n²)); Selection Sort "**$O(n)$**" (should be O(n²)); Quick Sort "worst-case running time is $O(n)$" (should be O(n²)) | `templates/SortingAlgorithms/sorting_algorithms.html:91, 96, 103` | 🔴 |
| "quadratic time complexity **(O(n))**" — exponent dropped | `templates/SortingAlgorithms/insertion_sort.html:266` | 🔴 |
| "square of its input size **$O(n)$** … slower than … $O(n)$" — first should be $O(n^2)$ | `templates/DSA/dsa.html:113-114` | 🔴 |
| Master-theorem example mangled: "so **$n$ dominates $n$**. Thus $T(n) = \Theta(n)$" — should be $n^3$ dominates $n$, $\Theta(n^3)$; also "$\frac{n}{2}=1$, meaning $n=2$" (should be $n/2^k$) | `templates/DSA/algorithms.html:225-226, 175` | 🔴 |
| "average-case running time for linear search is a **quadratic function**" — false (it's Θ(n)) | `templates/SearchingAlgorithms/linear_search.html:140-142` | 🟠 |
| "The first element would be at `<code>A</code>`" — indices lost, should be `A[0][0]` | `templates/Arrays/2Darrays.html:28` | 🟠 |
| Signup submit button labeled **"LogIn"** on the sign-up page | `templates/auth/signup.html:27-29` | 🟠 |
| AI-summary meta-text leaked into user-visible prose: "While **the sources** do not explicitly detail…", "(mentioned as a chapter topic **in the sources**)", "**The sources** provide explicit classifications…", "(information outside **the given sources**)" | `arrays.html:28-32`, `2Darrays.html:13, 31`, `linked_list.html:19, 108`, `sorting_algorithms.html:123-124, 194`, `heap_sort.html:125` | 🟠 |
| Page title block says "DSA" on the Algorithms page | `templates/DSA/algorithms.html:1` | 🟡 |
| "Feature Topics" (should be "Featured Topics"); feature card "Concept-to-Code Connection" reuses the "Animated Clarity" description verbatim | `home.html:49`, `:429-433` | 🟡 |
| `deleteHighlightMap` labels the delete function as "insertNode" | `templates/LinkedList/singly_linked_list.html:604, 616` | 🟡 |
| `linear_search.html` says worst-case Θ(n) "provides an **upper bound**" (Θ is a tight bound; O is the upper bound) | `linear_search.html:116-119` | 🟡 |
| Malformed HTML: `<li>` elements floating outside any list between code blocks | `stack.html:101-112` | 🟡 |
| Marketing claim "You're in control… Pause, play, speed up, or step through" — no such interactive controls exist (plain `<video controls>`) | `home.html:389-393` vs topic templates | 🟡 |

## 4. CSS Defects

| Bug | Location | Severity |
|---|---|---|
| `.carousel::-webkit-scrollbar { display:none }` — **wrong selector**; class is `.topic-carousel`, so WebKit browsers show a scrollbar despite the intent | `Website/website/static/styles.css:565-567` | 🟡 ✅ |
| `justify-content: flex;` — invalid value, declaration dropped | `styles.css:125` | 🟡 ✅ |
| `font-family: Roboto` never loaded anywhere (no Google Fonts / `@font-face`) | `styles.css:87` | 🟡 ✅ |
| Duplicate `scrollbar-width: none` in same rule | `styles.css:556, 560` | 🟡 |
| No `@media` queries anywhere — layout breaks on mobile | whole `styles.css` | 🟠 |

## 5. Manim Scene Defects

| Bug | Location | Severity | Explanation |
|---|---|---|---|
| **Left-Left case shows the label "Left Rotation" while performing a right rotation** | `Animations/AVLTree.py:646` (label) vs `:655-672` (performs right rotation; docstring line 541 says "needs right rotation") | 🔴 ✅ | Wrong on-screen text in a teaching video (rendered into final `LeftLeftCase.mp4`) |
| **Floyd-Warshall skips vertex 0 as an intermediate:** `for k in range(1, len(vertices))` | `Graphs.py:1809` | 🟠 ✅ | Correct **only** because node 0 has in-degree 0 in this example; the notebook version correctly uses `range(self.nodes)`. Non-standard, silently wrong for other graphs |
| **Adjacency-list stores unordered *sets*:** `adjecencyList[u].append({v, w})` — renders as `{10, 1}` with braces and hash-order instability | `Graphs.py:1192-1193` (WeightedAdjecencyListUD), `:1419` (WeightedAdjecencyListD) | 🟠 ✅ | Wrong data structure; visible in the rendered videos; should be a tuple `(v, w)` |
| **QuickSort base case marks `arr[low]` when the subarray is empty** (`low > high`) — marks the wrong element, and **IndexError when `low == len(arr)`** (e.g. input `[1,3,2]` triggers `arr[3]`) | `SortingAlgoritms.py:416-419` | 🟠 ✅ (logic proven; demo input `[5,2,4,6,3,1]` happens to be safe) | Guard should be `if low <= high` or bounds-checked |
| **LCS table construction only works when both strings have equal length:** `np.hstack`/`vstack` of an `(m+1)×(n+1)` DP table with an `(n+1)` column requires `m == n`; crashes otherwise | `DivideAndConquer.py:553-554` | 🟠 ✅ | Works solely because `"bisect"` and `"secret"` are both 6 chars |
| **Closest-pair strip check skips pairs `(Sy[0], Sy[k>1])`:** only `(Sy[0], Sy[1])` is seeded; loop starts at `i=1` | `DivideAndConquer.py:465-469` | 🟠 ⚠️ | Can miss the true closest pair if it involves the first strip point |
| Heap root insertion creates a **degenerate zero-length `Line`** and a **self-loop edge** `G.add_edge(v, v)` (`parent_index = -1` → last element) | `Trees.py:1196-1197` (MaxHeap), `:1298-1299` (MinHeap) | 🟡 ✅ | Renders as an invisible artifact; fragile |
| Post-heapify text compares against `heap[-1]` when a value bubbles to the root (`parent_index = -1`) → **wrong comparison text** ("2 <= 3" comparing root with the last leaf) | `Trees.py:1239` (MaxHeap), `:1341` (MinHeap) | 🟠 ✅ | Triggered whenever an insert bubbles to root — visible in rendered video |
| `make_arrow(i, "i")` called with `i = -1` → indexes `arr[-1]` (last element) before being repositioned | `SortingAlgoritms.py:444-446` | 🟡 | Harmless but constructs at a wrong anchor; latent if code changes |
| NameError-prone conditional animation: `fade_in`/`fade_out` only defined inside `if` blocks but used unconditionally at line 404; also passes `fade_in` twice | `DivideAndConquer.py:391-404` | 🟡 ⚠️ | Unreachable with current fixed input since base cases catch s≤3 — restructure |
| Interval-scheduling timeline labels appear **shifted one unit** relative to interval positions (tick `i` labeled `i+1` while intervals shift by `RIGHT * s`) | `Greedy.py:74-81` vs `:63-65` | 🟡 ⚠️ | Cosmetic ruler misalignment in the rendered video |
| `AVLNode` stores `self.value: int` but scenes pass `"X"`/`"Y"` strings | `AVLTree.py:40`, `:405`, `:434`, `:466, …` | 🟡 | Type contract violated (works at runtime) |
| Notebook `MinHeap.delete` / `MaxHeap.delete` crash on single-node heap (`parent_of_last` is `None` → `AttributeError`); also skip heapify-up after replacement | `Understanding/Trees/Trees.ipynb` cells 7/9 | 🟡 ⚠️ | Edge-case only |

## 6. Converter / Tooling Defects

| Bug | Location | Severity | Explanation |
|---|---|---|---|
| **moviepy version conflict** — `from moviepy import VideoFileClip` (2.x-only import) while requirements allow `moviepy>=1.0.3` (1.x needs `from moviepy.editor import …`); **and** on moviepy 2.2.1 `clip.resize(...)` no longer exists (renamed `resized`) so **`--resize` crashes** | `mp4_to_gif_converter.py:11` vs `requirements_converter.txt:2`; `mp4_to_gif_converter.py:86` | 🟠 ✅ (verified against installed moviepy 2.2.1: `resize` absent, `resized` present) | Pin `moviepy>=2.0` and switch to `clip.resized()`; or support both |
| `clip.close()` not in `finally` → reader leak if `write_gif` throws | `mp4_to_gif_converter.py:82-92` | 🟡 | Use try/finally |
| `gif_path = mp4_path.replace(".mp4", ".gif")` — naive replace mangles paths containing ".mp4" in a directory name | `mp4_to_gif_converter.py:74` | 🟡 | Use `Path.with_suffix(".gif")` |
| `.bat` runs `pip install -r` on every double-click, no error checks, `pause` regardless | `convert_mp4_to_gif.bat:3-9` | 🟡 | Optional |
