"""syncmap — machine-precise play/wait timelines for Manim scenes, no rendering.

Design contract: tools/syncmap/DESIGN.md. The recording engine lives in
``recorder``; the CLI (``python -m tools.syncmap snapshot --scene|--all``) in
``cli``. The ``map`` and ``check`` subcommands arrive with plan cards T5-T6.
"""
