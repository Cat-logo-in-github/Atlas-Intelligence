import yaml
import typer

from atlas.models.module import Module
from atlas.utils.paths import MODULES_DIR
from atlas.llm.ollama import generate



def generate_metadata(
    slug: str,
):

    module_path = MODULES_DIR / slug


    if not module_path.exists():

        raise typer.Exit(
            f"Unknown module: {slug}"
        )


    module = Module(module_path)



    if not module.knowledge.exists():

        raise typer.Exit(
            "Module has no knowledge.md"
        )


    knowledge = module.knowledge.read_text(
        encoding="utf-8"
    )



    all_modules = Module.load_all(
        MODULES_DIR
    )


    module_index = []

    for item in all_modules:

        module_index.append(
            {
                "slug": item.slug,
                "title": item.title,
                "tags": item.tags,
            }
        )



    prompt = f"""
You are organizing a knowledge graph.

You are given one Atlas knowledge module.

Your task:
1. Generate useful tags.
2. Find related modules.

Tags:
- Can be new concepts.
- Should describe the ideas, mathematics, fields,
  algorithms, techniques, or applications involved.
- These tags will be used for search,
  content generation, and categorization.
- Prefer meaningful technical tags over generic words.

Related:
- You MUST ONLY choose slugs from the provided module list.
- Choose modules that have conceptual connections.
- Do not invent new modules.
- Choose between 0 and 5 related modules.


Current module:

Title:
{module.title}


Knowledge:
----------------
{knowledge}
----------------



Available modules:

{module_index}



Return ONLY valid JSON.

Format:

{{
    "tags": [
        "optimization",
        "machine-learning"
    ],

    "related": [
        "linear-regression",
        "backpropagation"
    ]
}}
"""


    print(
        "Generating metadata..."
    )


    result = generate(
        prompt
    )



    try:

        data = yaml.safe_load(
            result
        )


    except Exception:

        raise typer.Exit(
            "LLM returned invalid JSON"
        )



    tags = data.get(
        "tags",
        []
    )


    related = data.get(
        "related",
        []
    )



    valid_slugs = {
        m.slug
        for m in all_modules
    }


    related = [
        r
        for r in related
        if r in valid_slugs
        and r != slug
    ]



    metadata_path = (
        module_path /
        "metadata.yaml"
    )


    with open(
        metadata_path,
        "r",
        encoding="utf-8"
    ) as f:

        metadata = yaml.safe_load(
            f
        )



    metadata["tags"] = tags

    metadata["related"] = related



    with open(
        metadata_path,
        "w",
        encoding="utf-8"
    ) as f:

        yaml.safe_dump(
            metadata,
            f,
            sort_keys=False,
            allow_unicode=True
        )



    print(
        f"✓ Updated {module.title}"
    )


    print(
        "Tags:",
        tags
    )


    print(
        "Related:",
        related
    )