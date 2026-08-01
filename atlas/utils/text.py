import re


def slugify(name: str) -> str:
    """
    Convert text into URL/folder friendly slug.

    Example:
    Gradient Descent -> gradient-descent
    """

    return re.sub(
        r"[^a-z0-9]+",
        "-",
        name.lower()
    ).strip("-")