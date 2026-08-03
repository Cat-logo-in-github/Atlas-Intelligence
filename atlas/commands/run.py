import typer

from atlas.utils.paths import MODULES_DIR
from atlas.models.module import Module

from atlas.simulation import Simulation
from atlas.simulation.loader import load_simulation


def run(
    module_name: str = typer.Argument(
        ...,
        help="Module slug"
    ),
    simulation_name: str = typer.Argument(
        ...,
        help="Simulation filename (without .py)"
    ),
):
    """
    Run a single simulation file without exporting outputs.
    """

    modules = Module.load_all(
        MODULES_DIR
    )

    module = next(
        (
            m
            for m in modules
            if m.slug == module_name
        ),
        None,
    )

    if module is None:

        typer.echo(
            f"Module not found: {module_name}"
        )

        raise typer.Exit(
            code=1
        )


    if not simulation_name.endswith(".py"):
        simulation_name += ".py"


    simulation_file = (
        module.simulation /
        simulation_name
    )


    if not simulation_file.exists():

        typer.echo(
            f"Simulation not found: {simulation_name}"
        )

        raise typer.Exit(
            code=1
        )


    typer.echo(
        f"Running {module.slug}/{simulation_name}\n"
    )


    simulation = Simulation(
        output=None
    )


    simulation.set_context(
        simulation_file
    )


    try:

        load_simulation(
            simulation_file,
            simulation
        )

        simulation.preview()

        typer.echo(
            "\n✓ Finished"
        )

    except Exception as e:

        typer.echo(
            f"\n✗ {e}"
        )

        raise typer.Exit(
            code=1
        )