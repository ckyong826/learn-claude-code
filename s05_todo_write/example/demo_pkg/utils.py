"""Small, dependency-free helper functions used by :mod:`demo_pkg`."""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence

__all__ = ["average", "chunk", "slugify"]

_SLUG_STRIP = re.compile(r"[^\w\s-]")
_SLUG_SEP = re.compile(r"[-\s]+")


def average(numbers: Sequence[float]) -> float:
    """Return the arithmetic mean of ``numbers``.

    Args:
        numbers: A non-empty sequence of numbers.

    Returns:
        The mean of ``numbers`` as a float.

    Raises:
        ValueError: If ``numbers`` is empty.
    """
    if not numbers:
        raise ValueError("average() requires at least one number")
    return sum(numbers) / len(numbers)


def chunk(items: Iterable[object], size: int) -> list[list[object]]:
    """Split ``items`` into consecutive sub-lists of at most ``size`` items.

    The final chunk may be shorter than ``size``. The input is not modified.

    Args:
        items: Any iterable of items to split.
        size: Maximum number of items per chunk. Must be positive.

    Returns:
        A list of chunks, each a list of at most ``size`` items. Returns an
        empty list when ``items`` is empty.

    Raises:
        ValueError: If ``size`` is not positive.
    """
    if size < 1:
        raise ValueError(f"chunk() size must be positive, got {size}")

    materialized = list(items)
    return [materialized[i : i + size] for i in range(0, len(materialized), size)]


def slugify(text: str) -> str:
    """Convert ``text`` into a lowercase, hyphen-separated slug.

    Punctuation is dropped, runs of whitespace or hyphens collapse into a
    single hyphen, and leading/trailing hyphens are removed.

    Args:
        text: The string to slugify.

    Returns:
        The slug. Returns an empty string when ``text`` contains no
        alphanumeric characters.

    Examples:
        >>> slugify("Hello, World!")
        'hello-world'
    """
    cleaned = _SLUG_STRIP.sub("", text.strip().lower())
    return _SLUG_SEP.sub("-", cleaned).strip("-")
