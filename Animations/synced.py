"""Annotation convention for time-synced code highlighting (Phase 2, plan card T3).

Scenes that feed the website's synced highlighting subclass :class:`SyncedScene`
and declare ``DISPLAY_CODE`` plus ``code_step`` calls. Importing this module has
zero side effects: it starts no renderer and prints nothing.
"""

from typing import ClassVar

from manim import Scene


class SyncedScene(Scene):
    """A Scene that declares the code its website page displays.

    Attributes
    ----------
    DISPLAY_CODE:
        The exact code the page shows, one string per line. ``code_step``
        line references are 1-based indices into this list.
    """

    DISPLAY_CODE: ClassVar[list[str]] = []  # exact code the website page displays

    def code_step(self, lines: str, key: str = "") -> None:
        """No-op while rendering. The syncmap recorder captures the current timestamp."""
        hook = getattr(self, "_syncmap_recorder", None)
        if hook is not None:
            hook(lines, key)
