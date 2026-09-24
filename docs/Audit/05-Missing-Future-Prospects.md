# Missing / Future Prospects

> Full-repository audit of **DSA-Animations** (commit `13f4b33`).
> What's absent but expected/referenced, and natural next features.

## 1. README Claims vs Reality

| README promise (`README.md`) | Status |
|---|---|
| "Animated explanations for … Trees (Binary, AVL, B-Trees), Heaps, Graphs, Greedy and Divide & Conquer" | ✅ All exist in `Animations/` with rendered media |
| "Jupyter notebooks for interactive exploration" | ✅ 3 complete notebooks in `Understanding/` |
| "Website interface for browsing and viewing animations" | ⚠️ **Partial** — website covers only Searching (2), Sorting (6), LinkedList (4 of 9 ops), Stack (not Queue), Arrays (text only). **No pages at all** for Trees (14 videos), Graphs (22), AVL (6), B-Trees (2), D&C (4), Greedy (2); LinkedList `NodeExplanation`, `DoubleNodeExplanation`, `ListRotation`, `TraverseLinkedList`, and `Queue` have no page or video |
| "Contributions are welcome! Please open issues or submit pull requests" | ⚠️ No `CONTRIBUTING.md`, no issue templates, no dev setup docs (how to render with manim, how to install Flask deps) |

## 2. Missing Engineering Essentials

- **No `requirements.txt` for the main project** — manim 0.19 / Flask / Flask-SQLAlchemy / Flask-Login dependencies are nowhere declared (only the converter's `requirements_converter.txt` exists, and it's broken — see Bugs report §6).
- **No tests** (0 test files; the algorithms are eminently testable — the notebooks contain pure implementations).
- **No CI** (no `.github/`), **no linting config**, **no Dockerfile / deployment config**, **no Procfile**.
- **License not mentioned in README** (MIT `LICENSE` exists but is unlinked).
- **Git hygiene:** 73 mp4s + 72 gifs + 16 webm + a SQLite DB are tracked (~1.09 GiB of git objects; `gifs/Graphs/FloydWarshall.gif` alone had to be gitignored, presumably for size). No Git LFS.

## 3. Content Gaps (animations exist ↔ website missing, and vice versa)

| Gap | Evidence |
|---|---|
| **Website coverage missing for 6 entire animation topics**: Trees, Graphs, AVL Trees, B-Trees, Divide & Conquer, Greedy — 51 rendered videos with no web pages, while the sidebar/footer/home already advertise them as placeholders | `views.py` vs `git ls-files` media |
| `Queue` page has no video (`Queue.mp4` exists in media; `Queue.webm` absent from static) | `queue.html` (no `<video>`), `static/Videos/StackAndQueue/` (Stack only) |
| Arrays pages are text-only though 4 array videos exist | `arrays.html`, `2Darrays.html` |
| `HuffmanEncoding` animation **never computes or displays the actual codes** — only builds the tree | `Animations/Greedy.py:229-465` |
| Bellman-Ford animation skips the V-th iteration for **negative-cycle detection** (`utils/IDEAS.md` explicitly lists "Detecting Cycles (Negative cycles also)" as planned) | `Graphs.py:1663`; `utils/IDEAS.md:29` |
| `BTree.mp4` cannot be re-rendered — its source class is a `VGroup`, not a `Scene`; plus 12 other scene names survive only as empty `partial_movie_files` dirs | see Not-Implemented report §5 |
| Auth half-features: `subscribed` checkbox stored but no email/newsletter backend (Flask-Mail installed in env but unused); no password reset; no email verification; no profile page; no `@login_required` anywhere | `models.py:9`, `views.py` |
| Missing pages promised by signup flow: "Terms of Service and Privacy Policy" (plain text, no links/pages) | `signup.html:31-33` |

## 4. Concrete Future Prospects

### 4.1 Website completion (highest leverage — media already exists)

1. **Trees / Graphs / AVL / B-Tree / D&C / Greedy web sections** reusing the 51 already-rendered videos + the existing `content.html` + `highlightMap` machinery.
2. A `/rotation` page (the `ListRotation` video already exists).
3. Queue video page (`Queue.mp4` just needs a webm conversion).
4. Wire up the 3 orphaned static videos (`NodeExplanation.webm`, `DoubleNodeExplanation.webm`, `logo-icon.png`).
5. Fix or remove the 17 dead sidebar links and 27 dead footer links.

### 4.2 New algorithm animations (matching `utils/IDEAS.md` and the site's footer promises)

1. Red-Black Trees
2. Tries
3. Hashing / Hash Tables
4. Dynamic Programming (0/1 knapsack, LIS — LCS already exists under D&C)
5. Interpolation Search
6. Cycle detection / negative-cycle detection (finish Bellman-Ford)
7. String matching (KMP)
8. Floyd-Warshall fixed to include vertex 0 as intermediate
9. Huffman animation extended to actually emit the binary codes
10. Heap sort with duplicate-value handling

### 4.3 Interactivity & engagement

1. **Interactive web visualizers** (JS canvas recreations of the sorts/searches with user-provided input) to fulfill the home page's "Interactive Visualization — pause, play, speed up, step through" claim.
2. **Quiz / exercise mode** tied to each topic; progress tracking for logged-in users (the auth + `subscribed` schema already exist).
3. **Search bar & sitemap** for the growing topic list.
4. **Dark-mode toggle** — the CSS is already written (`:root[data-theme="dark"]`), only the JS toggle is missing.
5. **Auto-sync highlight maps:** emit `(time, line)` events directly from manim scenes, replacing the manual notebook simulation.

### 4.4 Engineering / ops

1. Root `requirements.txt` (pinned) covering manim + Flask stack.
2. Dockerfile + deployment config.
3. GitHub Actions CI: render smoke-tests + a template-link checker (would have caught every broken-link bug in the Bugs report §1).
4. Git LFS or GitHub Releases for media; untrack the SQLite DB.
5. `CONTRIBUTING.md`, issue templates, dev setup docs.
6. Favicon + SEO meta + per-page titles.
7. Mobile breakpoints (zero `@media` queries today).
8. Restore the 13 lost scene sources (`BTree`, `GraphTest`, `AVLTreeExplanation`, `BinarySearchTree`, etc.) from history or re-write them.
