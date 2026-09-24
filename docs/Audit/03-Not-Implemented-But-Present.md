# Not Implemented but Present

> Full-repository audit of **DSA-Animations** (commit `13f4b33`).
> Stubs, placeholders, dead code, and unused / never-referenced files that exist in the repo.

## 1. Empty / Dead Files (git-tracked)

| Item | Evidence |
|---|---|
| `Website/website/templates/Linked List/linked_lists.html` | **0-byte file**, git-tracked, never referenced. The folder name (with a space) doesn't match any route; the actual route renders `LinkedList/linked_list.html` instead |
| `utils/filtered_tree.txt` | **0-byte file**, git-tracked, never used anywhere |

## 2. Dead Methods / Dead Code Inside Source Files

| Item | Location |
|---|---|
| `insert_into_AVLTree()` + `insert()` — ~60 lines never called (`construct` uses `build_tree_silently`) | `Animations/AVLTree.py:1551-1611` |
| `reconnect_after_rotation()` — one-line helper whose comment admits it does nothing ("The parent will call set_left()…") | `AVLTree.py:1545-1549` |
| `remove_keys_after()` — never called anywhere | `Animations/BTrees.py:188-191` |
| Duplicated assignments `current_value, current_node = bst_root[0]` twice; `parent_node` assigned then immediately overwritten | `Trees.py:1390-1394`, `:1404→1450` |
| `old_balance` / `new_balance` computed twice from the same expression | `AVLTree.py:282-285` |
| Dead `if hasattr(L, 'symbol') and hasattr(R, 'symbol')` — always true | `Greedy.py:393` |
| `distance` dict in Prim's — written, never read | `Graphs.py:1919-1930`, `:1986-1988` |
| networkx `G` built & updated in MaxHeap/MinHeap scenes but never rendered | `Trees.py:1262`, `:1364` |
| Commented-out code blocks (full list in the Improvements report, item 16) | various |
| Dark-theme CSS (`:root[data-theme="dark"]`) — CSS written, but `data-theme` is hardcoded `"light"` and **no toggle exists** | `Website/website/templates/base.html:2`, `static/styles.css:73-79` |

## 3. Unused Static Assets (exist, never referenced by any template/route)

| Asset | Notes |
|---|---|
| `Website/website/static/images/logo-icon.png` (112 KB) | No template references it |
| `Website/website/static/Videos/LinkedList/NodeExplanation.webm` | No template references it |
| `Website/website/static/Videos/LinkedList/DoubleNodeExplanation.webm` | No template references it |

## 4. Placeholder Navigation / Dead UI (renders, goes nowhere)

| Item | Location |
|---|---|
| **Entire Trees / Heaps / Graphs sidebar sections** — placeholder links pointing at routes that don't exist (17 broken links — full list in the Bugs report) | `Website/website/templates/content.html:60-99` |
| **Footer link list — 27 `<a>` tags with no `href` at all** (Our Team, Contact Us, Privacy Policy, Terms of Service, all algorithm names) | `base.html:118-187` |
| **"Explore" buttons on all 6 home-page topic cards — no `onclick`/`href`, do nothing** | `home.html:115`, `:158`, `:201`, `:244`, `:287`, `:330` |
| Home cards advertise Trees/Heap/Graphs content and fake ratings "4.6 (1.2k)" | `home.html:86-94` etc. |
| `AVLNode(value: int)` typed but constructed with strings `AVLNode("X")` | `AVLTree.py:405`, `:434`, `:466-467` etc. |

## 5. Lost / Deleted Sources Evidenced by Media Artifacts

Rendered media exists in git for scenes that have **no corresponding source class** — the source was deleted or never committed, so these videos cannot be re-rendered from the current codebase.

| Evidence | Interpretation |
|---|---|
| `Animations/media/videos/BTrees/480p15/BTree.mp4` (tracked) | `BTree` was once a `Scene`; in current source `BTree` is only a `VGroup` — the video has **no rendering source** |
| Empty `partial_movie_files` dirs in `Graphs`: `Graph`, `GraphTest`, `GraphText`, `Issue` | Deleted test/explanation scenes |
| Empty dirs in `AVLTree`: `AVLTreeExplanation`, `AVLTreeTest`, `RightRightRotation` | Deleted scenes |
| Empty dirs in `LinkedList`: `CreateNewNode`, `Insertion` | Deleted scenes |
| Empty dir in `Greedy`: `IntervalSceduling` (typo'd) | Deleted scene |
| Empty dirs in `Trees`: `AVLTreeExplanation`, `AVLTreeScene`, `BinarySearchTree` | Deleted scenes |
| `utils/TreeView.txt` (dev note) confirms `AVLTreeExplanation.mp4`, `BinarySearchTree.mp4`, `GraphTest/Issue…png` (ManimCE v0.19.0) previously existed | Corroborates lost sources |

## 6. On-Disk but Untracked / Runtime Artifacts

| Item | Notes |
|---|---|
| `Website/website/database.db` (untracked) | Runtime artifact created *inside the package folder* due to the cwd-dependent DB path bug (see Bugs report §2); its tracked twin `Website/database.db` should not be in git either |
| `Animations/media/texts/`, `media/Tex/`, `media/images/`, empty `partial_movie_files` dirs | Manim caches — correctly gitignored but present on disk |
| `utils/IDEAS.md`, `utils/TreeView.txt` | Dev notes deliberately gitignored (`.gitignore:210, 213`) |
| `gifs/Graphs/FloydWarshall.gif` | Exists on disk but is gitignored (`.gitignore:215`) — the only gif not in git |
| `__pycache__/` folders (root, `Animations/`, `Website/website/`) | Correctly gitignored, present on disk |
