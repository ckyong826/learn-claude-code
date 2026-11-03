"""Small greeting example used by the s05 todo_write lesson."""

from __future__ import annotations


def greet(name: str) -> str:
    """Build and print a greeting for ``name``.

    Args:
        name: The name of the entity to greet.

    Returns:
        The greeting message that was printed.
    """
    message: str = f"Hello, {name}"
    print(message)
    return message


def main() -> None:
    """Run the example."""
    greet("Claude")


if __name__ == "__main__":
    main()
