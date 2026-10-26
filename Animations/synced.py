"""Annotation convention for time-synced code highlighting (Phase 2, plan card T3; C0M v2).

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
        The Python reference implementation the page displays by default —
        one string per line. Per-language line numbers live in
        ``tools/syncmap/langs/<slug>.json``, keyed by semantic step keys.
    """

    DISPLAY_CODE: ClassVar[list[str]] = []  # exact code the website page displays

    def code_step(self, key: str) -> None:
        """No-op while rendering. The syncmap recorder captures the key's timestamp.

        ``key`` is a short semantic slug naming the algorithm step being
        demonstrated (``"init"``, ``"partition-loop"``, ``"swap"``, ``"recurse"``).
        Keys are language-agnostic by design: each ``tools/syncmap/langs/<slug>.json``
        language maps them to that language's line numbers.
        """
        hook = getattr(self, "_syncmap_recorder", None)
        if hook is not None:
            hook(key)
