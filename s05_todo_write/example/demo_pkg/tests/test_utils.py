"""Tests for :mod:`demo_pkg.utils`."""

from __future__ import annotations

import pytest

from demo_pkg.utils import average, chunk, slugify


class TestAverage:
    """Tests for :func:`demo_pkg.utils.average`."""

    def test_single_value(self) -> None:
        assert average([4]) == 4.0

    def test_multiple_values(self) -> None:
        assert average([1, 2, 3, 4]) == 2.5

    def test_accepts_tuple(self) -> None:
        assert average((2.0, 4.0)) == 3.0

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="at least one number"):
            average([])


class TestChunk:
    """Tests for :func:`demo_pkg.utils.chunk`."""

    def test_even_split(self) -> None:
        assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_remainder_chunk(self) -> None:
        assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_size_larger_than_input(self) -> None:
        assert chunk([1, 2], 10) == [[1, 2]]

    def test_empty_iterable(self) -> None:
        assert chunk([], 3) == []

    def test_accepts_generator(self) -> None:
        assert chunk(iter(range(3)), 2) == [[0, 1], [2]]

    @pytest.mark.parametrize("size", [0, -1])
    def test_non_positive_size_raises(self, size: int) -> None:
        with pytest.raises(ValueError, match="size must be positive"):
            chunk([1, 2, 3], size)


class TestSlugify:
    """Tests for :func:`demo_pkg.utils.slugify`."""

    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("Hello, World!", "hello-world"),
            ("  Multiple   Spaces  ", "multiple-spaces"),
            ("Already-a-slug", "already-a-slug"),
            ("Under_scores Kept", "under_scores-kept"),
            ("", ""),
            ("!!!", ""),
        ],
    )
    def test_slugify(self, text: str, expected: str) -> None:
        assert slugify(text) == expected


def test_package_exports_helpers() -> None:
    """The package re-exports the helpers it advertises in ``__all__``."""
    import demo_pkg

    for name in demo_pkg.__all__:
        assert hasattr(demo_pkg, name)
