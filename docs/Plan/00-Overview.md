# 00 — Implementation Plan Overview

**Repo:** DSA-Animations · **Audit baseline:** commit `13f4b33` (see `docs/Audit/01..05-*.md`) · **Created:** 2026-09-24

## Goals

| # | Goal | Delivered by |
|---|---|---|
| G1 | Fix all bugs; make code cleaner & more scalable **without losing current functionality** | Phase 1 (bugfixes) + Phase 3 (refactor) |
| G2 | Replace hand-eyeballed `highlightMap` JS with a Python tool that parses an animation class and emits the exact timestamp→line mapping + code | Phase 2 (sync tool) — becomes the refactor oracle and the page-building engine |
| G3 | Get **all** animations onto the website (51 orphan videos + page-less topics) | Phase 4 (content) |
| G4 | Improve the website overall (responsive, dark mode, fonts, SEO, search, honest UI) | Phase 5 (polish) |

## Non-goals

- No re-design of the animation pedagogy; scenes keep their visual identity.
- No user-data migration (DB contains schema + test rows only — confirm before B1).
- No re-render of all 72 scenes; only scenes whose visuals changed.
- No Git LFS migration inside this plan (flagged as follow-up; media freeze enforced via safety rails).

## Phase map & dependencies

```
P0 Foundation ──► P1 Bugfixes ──► P2 Sync Tool ──► P3 Refactor ──► P4 Website Content ──► P5 Polish
(guardrails)     (behavior may      (oracle built     (oracle proves       (uses tool +        (independent
                  change: fixes)     BEFORE refactor)  behavior kept)       refactored code)     after content lands)
```

Why this order: the sync tool must exist **before** the refactor so every refactor card can prove behavior preservation with byte-identical timeline snapshots (Decision D6). Bugfixes land before snapshots so baselines capture the corrected code.

## The task-card format (vibe-coding ready)

Every card in `01..06-*.md` is a self-contained subagent prompt:

```
### <ID> — <Title>
Agent: <which subagent to dispatch> · Skill: <skill to load> · Depends: <IDs> · Size: S/M/L
Problem: <what's wrong, with audit + file:line references>
Do: <exact change spec>
Verify: <how to prove it worked>
Done when: <checklist>
```

### Driving a session (the loop)

1. Open `docs/Plan/TASKBOARD.md`, pick the next ☐ card (dependencies first).
2. Tell opencode: *"Do card B5 from `docs/Plan/02-Bugfixes.md` with the `dsa-bugfixer` agent"* (or just *"next task"* — cards are ordered).
3. The agent loads its skill(s), executes, and reports with verification evidence.
4. Gate phases with the `dsa-auditor` agent (it verifies adversarially, cannot edit).
5. Tick the card in `TASKBOARD.md`. Commit per card or in small batches (user's call).

## Agentic infrastructure (this repo)

| Piece | Path | Purpose |
|---|---|---|
| Agent guide | `AGENTS.md` | Always-loaded repo context, commands, safety rails |
| Skill: verify | `.opencode/skills/dsa-verify/` | The verification stack every task ends with |
| Skill: render | `.opencode/skills/dsa-render/` | Rendering + webm conversion discipline |
| Skill: highlightmap | `.opencode/skills/dsa-highlightmap/` | The G2 tool: convention + CLI + wiring |
| Skill: add-page | `.opencode/skills/dsa-add-page/` | The full recipe a new page must follow |
| Agent: bugfixer | `.opencode/agents/dsa-bugfixer.md` | Minimal-diff bug fixing (P1) |
| Agent: refactorer | `.opencode/agents/dsa-refactorer.md` | Behavior-preserving refactor (P3) |
| Agent: page-builder | `.opencode/agents/dsa-page-builder.md` | Page assembly (P4) |
| Agent: auditor | `.opencode/agents/dsa-auditor.md` | Phase gates + adversarial QA (read-only) |
| Config | `opencode.json` | Loads `AGENTS.md` into every session |

## Decision log

| ID | Decision | Rationale |
|---|---|---|
| D1 | New routes kebab-case; legacy space-routes survive as **stacked aliases** on the same view function | Zero broken bookmarks; no redirects needed |
| D2 | Rename `SortingAlgoritms` → `SortingAlgorithms` (source, converter, `git mv` media dir) | Scalability goal; one-time cost, website paths unaffected (webm names don't embed category typo… category folder does — handled in card) |
| D3 | Content stays public (no `@login_required`); `subscribed` column kept but untouched | "Without compromising functionality"; newsletter = future work |
| D4 | New pages load sync maps from JSON (`static/sync/`); legacy inline maps stay until optional W10 migration | No big-bang rewrite of working pages |
| D5 | Behavior-preservation oracle = syncmap timeline snapshots (byte-identical) + spot renders | Cheap, machine-checkable, stronger than eyeballing |
| D6 | Sync tool built **before** refactor | D5 requires it |
| D7 | No new media committed >1 MB without explicit user approval | Repo already ~1 GiB; webm conversions for P4 (~56 small files) to be confirmed with user |
| D8 | Website render standard = 480p15 (`-ql`) | Matches existing webms + fast renders |

## Project definition of done

1. All TASKBOARD cards ☑ (or explicitly cancelled with reason)
2. `pytest` + link checker green with an empty baseline allowlist
3. Every scene that has a video on the site has a machine-generated sync map (`tools.syncmap check` green)
4. Every audit bug from `docs/Audit/04-Bugs.md` re-verified fixed by `dsa-auditor`
5. Site works on a case-sensitive filesystem (CI green) — every topic from the audit gap list has a page
6. Final audit report written (`docs/Audit/` re-run via dsa-auditor)
