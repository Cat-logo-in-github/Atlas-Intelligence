import typer

from atlas.utils.paths import MODULES_DIR
from atlas.models.module import Module


def list_modules(
    filter: str = typer.Argument(
        None,
        help="Optional filter: updated"
    )
):
    """
    Lists Status and slugs for all modules
    """

    if not MODULES_DIR.exists():

        typer.echo(
            "No modules found."
        )

        raise typer.Exit()


    modules = Module.load_all(
        MODULES_DIR
    )


    if filter == "updated":

        modules = [
            m
            for m in modules
            if m.updated
        ]


    if not modules:

        typer.echo(
            "No matching modules found."
        )

        raise typer.Exit()


    typer.echo(
        "\nAtlas Modules\n"
    )


    for i, module in enumerate(
        modules,
        start=1
    ):

        typer.echo(
            f"{i}. {module.title}"
        )

        typer.echo(
            f"   slug: {module.slug}"
        )

        typer.echo(
            f"   status: {module.status}"
        )

        typer.echo(
            f"   updated: {module.updated}"
        )

        typer.echo()


    typer.echo(
        f"Total: {len(modules)} modules"
    )