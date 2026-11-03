"""Demo package for the s05 todo_write lesson.

A tiny, dependency-free package used to illustrate package layout,
type hints, docstrings, and pytest-based tests.
"""

from __future__ import annotations

from .utils import average, chunk, slugify

__all__ = ["average", "chunk", "slugify"]

__version__ = "0.1.0"
