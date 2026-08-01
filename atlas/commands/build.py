import typer

from atlas.utils.paths import MODULES_DIR

from atlas.models.module import Module

from atlas.generators.website import (
    build_website
)

from atlas.commands.generate import (
    generate_all
)

from atlas.generators.simulation import (
    generate_simulation
)

from atlas.generators.run_simulations import (
    run_simulation
)

from atlas.generators.graph import (
    build_graph
)

from atlas.validators.module import (
    module_needs_build
)

from pathlib import Path


def append_quiz(module):

    quiz = module.generated / "quiz.md"

    if not quiz.exists():
        return


    knowledge = module.knowledge


    quiz_text = quiz.read_text(
        encoding="utf-8"
    ).strip()


    knowledge_text = knowledge.read_text(
        encoding="utf-8"
    ).rstrip()


    # Prevent accidental duplicate appends
    if "## Quiz" in knowledge_text:
        return


    with knowledge.open(
        "a",
        encoding="utf-8"
    ) as f:

        f.write("\n\n")
        f.write("## Quiz\n\n")
        f.write(quiz_text)
        f.write("\n")

def build():
    """
    Build Simulation, Notebooks, Website-Content and Graph all-together for a given module
    """

    typer.echo(
        "\nAtlas Build"
    )


    modules = Module.load_all(
        MODULES_DIR
    )


    typer.echo(
        f"\nFound {len(modules)} modules"
    )

    for module in modules:

        if not module_needs_build(module):
            print(
                f" O {module.slug} unchanged"
            )
            continue

        # generate_all(module.slug)

        if not module.website_enabled:
            append_quiz(module)

        if module.simulation_enabled:
            generate_simulation(module.slug)
            run_simulation(module)

    
    build_website(
        modules
    )


    build_graph(
        modules
    )

    typer.echo(
        "\nBuild complete."
    )