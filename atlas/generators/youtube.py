import typer

from atlas.models.module import Module
from atlas.utils.paths import MODULES_DIR
from atlas.llm.ollama import generate


def generate_youtube(
    slug: str,
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite an existing youtube.md",
    ),
):

    module_path = MODULES_DIR / slug

    if not module_path.exists():
        raise typer.Exit(
            f"Unknown module: {slug}"
        )

    module = Module(module_path)

    destination = (
        module.generated
        /
        "youtube.md"
    )

    if destination.exists() and not force:
        print(
            f" O {module.title}/youtube.md exists"
        )
        return

    knowledge = ""

    if module.knowledge.exists():
        knowledge = module.knowledge.read_text(
            encoding="utf-8"
        )

    blog = ""

    if module.blog.exists():
        blog = module.blog.read_text(
            encoding="utf-8"
        )

    print(
        f" ▶ Generating YouTube outline: {module.title}"
    )

    prompt = f"""
You are a YouTube educational content strategist.

Create a video outline from the following research material.

Topic:
{module.title}

Knowledge notes:
----------------
{knowledge}

Blog draft:
-----------
{blog}

Create:

# Video Title Ideas
Give 5 compelling titles.

# Video Structure

Include:
- timestamps
- section names
- purpose of each section
- teaching flow

The video should:
- start with intuition
- build mathematical understanding
- include examples
- connect to applications
- end with a memorable summary

# Video Description

Write a YouTube description.

# Thumbnail Ideas

Give 5 thumbnail concepts.
"""

    result = generate(prompt)

    content = f"""# {module.title}

{result}
"""

    destination.write_text(
        content,
        encoding="utf-8"
    )

    print(
        f" ✓ Generated {destination}"
    )