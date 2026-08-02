import json
from datetime import datetime

import typer

from atlas.utils.paths import MODULES_DIR
from atlas.utils.text import slugify



def create(
    name: str
):
    """
    Create a module(content_stack)
    """

    slug = slugify(name)


    MODULES_DIR.mkdir(
        exist_ok=True
    )


    module_path = (
        MODULES_DIR /
        slug
    )


    if module_path.exists():

        typer.echo(
            f"Module already exists: {module_path}"
        )

        raise typer.Exit(
            code=1
        )


    module_path.mkdir(
        parents=True
    )


    (module_path / "assets").mkdir()

    (module_path / "simulation").mkdir()


    (module_path / "knowledge.md").write_text(
f"""# {name}


## The Question


## Intuition


## Mathematics


## Implementation


## Visualization


## Connections


## Open Questions

""",
        encoding="utf-8"
    )


    (module_path / "blog.md").write_text(
f"""# {name}


Write the narrative version of this topic here.

""",
        encoding="utf-8"
    )


    (module_path / "metadata.yaml").write_text(
f"""
title: "{name}"

slug: "{slug}"

module: ""

status: seed

difficulty: beginner

created: "{datetime.now().isoformat()}"

updated: false

last_build: ""

content_hash: ""

tags: []

related: []

outputs:
  quiz:
    published: false

  website:
    published: false

  youtube:
    published: false
    url: ""

  instagram:
      published: false
      url: ""

  blog:
    published: false
    url: ""

  notebook:
    published: false

  simulation:
    published: false
    build: false
""",
        encoding="utf-8"
    )


    notebook = {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5
    }


    (module_path / "notebook.ipynb").write_text(
        json.dumps(
            notebook,
            indent=2
        ),
        encoding="utf-8"
    )


    typer.echo(
        f"Created module: {module_path}"
    )