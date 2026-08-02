import typer

from atlas.utils.paths import MODULES_DIR

from atlas.models.module import Module

from atlas.generators.website import (
    build_website
)

from atlas.commands.generate import (
    generate_quiz,
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

from atlas.utils.quiz import append_quiz

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

        if not module.quiz_enabled:
            generate_quiz(module.slug)
            append_quiz(module)

        if module.simulation_enabled and module.simulation_needs_build:
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