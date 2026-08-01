import typer

from atlas.models.module import Module
from atlas.utils.paths import MODULES_DIR
from atlas.llm.ollama import generate


def generate_instagram(
    slug: str,
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite an existing instagram.md",
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
        "instagram.md"
    )


    if destination.exists() and not force:
        print(
            f" O {module.title}/instagram.md exists"
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
        f" ▶ Generating Instagram script: {module.title}"
    )


    prompt = f"""
You are a short-form educational content creator.

Create a 30-60 second Instagram Reel script
from the following research material.

Topic:
{module.title}


Knowledge notes:
----------------
{knowledge}


Blog draft:
-----------
{blog}


Create:

# Hook

A powerful first sentence that grabs attention
within 3 seconds.


# Script

Write the complete spoken narration.
It should:
- sound natural when spoken aloud
- be understandable to beginners
- explain one important idea
- avoid generic motivational language
- avoid ai talk and buzzwords
- fit within 30-60 seconds


# Visual Ideas

Suggest what should appear on screen
during each part of the script.


# Caption

Write a short Instagram caption.


# Hashtags

Give relevant hashtags.
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