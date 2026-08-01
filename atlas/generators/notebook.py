import json
import subprocess
import sys
from pathlib import Path

from atlas.utils.paths import WEBSITE_DIR
from atlas.utils.filesystem import write_if_changed, copy_if_changed
from atlas.validators.notebook import notebook_has_content


def copy_notebook(module):

    if not notebook_has_content(
        module.notebook
    ):
        return


    destination = (
        WEBSITE_DIR
        /
        "content"
        /
        module.slug
        /
        "notebook.ipynb"
    )


    if copy_if_changed(
        module.notebook,
        destination
    ):
        print(
            f" ✓ {module.slug}/notebook.ipynb updated"
        )



def build_notebook_page(module):

    if not notebook_has_content(
        module.notebook
    ):
        return


    content = f"""
---
title: "{module.title} Notebook"
---

This notebook accompanies the research module.

## Notebook

- [View notebook](notebook.html)
- [Download notebook](notebook.ipynb)
"""


    destination = (
        WEBSITE_DIR
        /
        "content"
        /
        module.slug
        /
        "notebook.md"
    )


    if write_if_changed(
        destination,
        content
    ):
        print(
            f" ✓ {module.slug}/notebook.md updated"
        )



def build_notebook_html(module):

    if not notebook_has_content(
        module.notebook
    ):
        return


    destination = (
        WEBSITE_DIR
        /
        "content"
        /
        module.slug
        /
        "notebook.html"
    )


    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    subprocess.run(
        [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "html",
            "--output",
            destination.stem,
            "--output-dir",
            str(destination.parent),
            str(module.notebook)
        ],
        check=True
    )