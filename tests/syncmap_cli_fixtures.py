"""Fixture scenes for the syncmap CLI tests (no ``test_`` prefix: never collected by pytest)."""

from typing import ClassVar

from manim import Create, Scene, Square, Uncreate
from synced import SyncedScene


class FixtureScene(Scene):
    def construct(self):
        self.play(Create(Square()))
        self.wait(0.5)


class FixtureBoom(Scene):
    def construct(self):
        raise RuntimeError("fixture boom")


class FixtureSyncedScene(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "def f(x):",
        "    return x + 1",
    ]

    def construct(self):
        self.code_step("1", key="enter")
        self.play(Create(Square()))
        self.code_step("2", key="call")
        self.play(Uncreate(Square()))
        self.wait(0.5)


class FixtureDedupeScene(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "def g():",
        "    return 1",
        "    return 2",
    ]

    def construct(self):
        self.code_step("1")
        self.code_step("1")
        self.play(Create(Square()))
        self.code_step("3")
        self.code_step("3")
        self.code_step("1")
        self.play(Uncreate(Square()))


class FixtureOutOfRangeScene(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "def h():",
        "    pass",
    ]

    def construct(self):
        self.play(Create(Square()))
        self.code_step("3")
