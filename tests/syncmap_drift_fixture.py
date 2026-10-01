"""Drift-check fixture: this file is MUTATED (and restored) by test_syncmap_check.py."""

from manim import Create, Scene, Square


class DriftScene(Scene):
    def construct(self):
        self.play(Create(Square()))
        self.wait(1)
