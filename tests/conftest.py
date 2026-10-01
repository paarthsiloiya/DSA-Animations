"""Shared pytest setup: make Animations/ importable so ``synced`` resolves everywhere.

Must run before any test module (or fixture module) executes
``from synced import SyncedScene``.
"""

import sys
from pathlib import Path

ANIMATIONS_DIR = Path(__file__).resolve().parents[1] / "Animations"
if str(ANIMATIONS_DIR) not in sys.path:
    sys.path.insert(0, str(ANIMATIONS_DIR))
