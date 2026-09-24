---
name: dsa-verify
description: Use when finishing or gating any change in the DSA-Animations repo to run the verification stack (pytest, link checker, Flask route smoke tests) and interpret results. Also use when a task card in docs/Plan/ says "verify" or "gate".
---

# DSA Verify — the repo's verification stack

Run these from repo root, in this order. Report every result honestly.

## 1. Tests

```
pytest -q
```

- If tests don't exist yet (Phase 0 incomplete), note it and fall back to the manual checks below.

## 2. Link checker

```
python tools/link_check.py
```

- Exists after Phase 0 card F3. Fails on any template `href`/`url_for` that doesn't resolve to a route or an existing static file.
- Known-broken links are allowlisted in `docs/Plan/baseline-broken-links.txt`. A **new** broken link fails even if allowlisted ones pass. If your task fixes an allowlisted link, remove it from the allowlist in the same change.

## 3. Flask route smoke (manual fallback / spot check)

```
cd Website
python -c "from website import create_app; app=create_app(); c=app.test_client(); print({r.rule: c.get(r.rule).status_code for r in app.url_map.iter_rules() if r.endpoint != 'static'})"
```

Every route should print 200 (`/logout` may be 302).

## 4. Targeted checks by change type

- **Template change:** open the page with the dev server (`cd Website; python main.py`), check browser console, confirm Prism highlighting + video + sync map behavior.
- **Manim change:** review the diff against the scene. If visuals intentionally changed → note it for the render batch (RB cards). If behavior-preserving → timeline check (Phase 2+): `python -m tools.syncmap snapshot --scene <Module> <Scene>` and compare against the committed baseline in `tools/syncmap/timelines/`.
- **Flask/tools Python change:** re-run pytest + link checker.

## 5. Report format

End with: commands run → pass/fail each → failures explained → recommended next step. **Never mark a task done with a red check.**
