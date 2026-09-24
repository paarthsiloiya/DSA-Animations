# DSA-Animations

This repository contains animations and visualizations for various Data Structures and Algorithms (DSA) topics using the manim library.

## Features

- Animated explanations for:
  - Searching and Sorting Algorithms
  - Arrays
  - Linked Lists
  - Stacks & Queues
  - Trees (Binary, AVL, B-Trees)
  - Heaps
  - Graphs (Directed, Undirected, Weighted, DAGs)
  - Greedy and Divide & Conquer techniques
- Jupyter notebooks for interactive exploration
- Website interface for browsing and viewing animations

## Directory Structure

- `Animations/` — Manim scene scripts (one file per DSA topic) plus rendered videos
- `Understanding/` — Jupyter notebooks (ground-truth algorithm implementations)
- `Website/` — Flask-based web app for serving animations
- `docs/Audit/` — five-part code audit: implemented / improvable / dead code / bugs / gaps
- `docs/Plan/` — phased implementation plan: task cards, `TASKBOARD.md`, and `PROMPTS.md` (a read-only library of stepwise execution prompts)
- `AGENTS.md` — guide for AI coding agents (commands, conventions, safety rails)
- `.opencode/` — opencode skills and subagent definitions used to execute the plan
- `utils/`, `tools/` — developer notes and helper scripts

## Running the Website

To view and browse the animations through a web interface:

1. Navigate to the `Website/` directory:
   ```sh
   cd Website
   ```
2. Start the Flask web server:
   ```sh
   python main.py
   ```

## Development Workflow

This repository is developed according to a phased, agent-executable plan:

1. [`docs/Plan/00-Overview.md`](docs/Plan/00-Overview.md) — goals, phase map, decision log.
2. [`docs/Plan/PROMPTS.md`](docs/Plan/PROMPTS.md) — 52 self-contained, stepwise execution prompts (read-only; run strictly in order). Progress is tracked in [`docs/Plan/TASKBOARD.md`](docs/Plan/TASKBOARD.md).
3. [`docs/Audit/`](docs/Audit/) — the code audit the plan acts on (bugs, improvements, dead code, gaps).
4. `AGENTS.md` — project conventions, commands, and safety rails for AI agents (read this first if you are an agent or contributor using agentic tools).

## Contributing

Contributions are welcome! Please open issues or submit pull requests for new animations, bug fixes, or improvements.
