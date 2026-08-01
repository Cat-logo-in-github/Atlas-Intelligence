import typer

from atlas.models.module import Module
from atlas.utils.paths import MODULES_DIR
from atlas.llm.ollama import generate



def generate_posts(
    slug: str,
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite an existing posts.md",
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
        "posts.md"
    )


    if destination.exists() and not force:

        print(
            f" O {module.title}/posts.md exists"
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
        f" ▶ Generating posts: {module.title}"
    )



    assets = []

    if module.assets.exists():

        assets = [
            path.name
            for path in module.assets.iterdir()
            if path.is_file()
        ]


    asset_list = "\n".join(
        f"- {asset}"
        for asset in assets
    )


    prompt = f"""
You are a technical content creator helping share
a learning project online.

Create social media posts from this Atlas knowledge module.

The goal is to create curiosity and document learning.

Do NOT write marketing content.
Do NOT sound like a company.
Write as a student/researcher sharing something interesting
they discovered.

Topic:
{module.title}


Knowledge notes:
----------------
{knowledge}
----------------


Blog draft:
-----------
{blog}
-----------


Available assets inside the module:

{asset_list if asset_list else "No existing assets available."}


Create 10 different posts.

Format every post exactly:

# Post N

## Text

The complete post text.

## Asset

Choose one existing asset filename from the list above.

Rules:

- Do not include platform names.
- Do not include hooks as separate sections.
- Do not include engagement questions.
- Do not include hashtags.
- Do not create fake asset filenames.
- The asset must exist in the provided list.
- Prefer using different assets for different posts.
- Only reuse an asset if there are not enough assets available.
- If no assets exist, describe the visual that should be created instead.

Posts should vary in angle:

- a surprising insight
- a beginner explanation
- a personal learning moment
- a mathematical intuition
- a connection to neuroscience or another field
- a misconception correction
- a project update
- a question about the idea
- a visualization explanation
- a lesson learned

Each post should stand alone and be interesting even to someone
who has never seen this module before.

Make the posts concise and natural.
"""



    result = generate(
        prompt
    )


    content = f"""# {module.title}

Generated Content Posts

{result}
"""


    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    destination.write_text(
        content,
        encoding="utf-8"
    )


    print(
        f" ✓ Generated {destination}"
    )