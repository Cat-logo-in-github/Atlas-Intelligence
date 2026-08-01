import typer

from atlas.utils.paths import MODULES_DIR
from atlas.models.module import Module

from atlas.validators.metadata import (
    validate_metadata
)

from atlas.validators.notebook import (
    notebook_has_content
)



def file_has_content(
    path,
    minimum_length=200
):

    if not path.exists():
        return False


    text = path.read_text(
        encoding="utf-8"
    ).strip()


    return len(text) >= minimum_length



def folder_has_files(path):

    if not path.exists():
        return False


    return any(
        path.iterdir()
    )

def simulation_has_files(path):

    if not path.exists():
        return False

    files = [
        file
        for file in path.iterdir()
        if file.is_file()
    ]

    if not files:
        return False

    return all(
        file.suffix == ".py"
        for file in files
    )

def check(
    module_name: str = typer.Argument(
        None,
        help="Optional module slug to check"
    )
):
    """
    Checks the health of a given module (can check all modules. Not recommended. Use list instead to find status first)
    """

    if not MODULES_DIR.exists():

        typer.echo(
            "No modules found."
        )

        raise typer.Exit()


    all_modules = Module.load_all(
        MODULES_DIR
    )


    if module_name:

        modules = [
            module
            for module in all_modules
            if module.slug == module_name
        ]


        if not modules:

            typer.echo(
                f"Module not found: {module_name}"
            )

            raise typer.Exit(
                code=1
            )

    else:

        modules = all_modules



    for module in modules:

        typer.echo(
            f"\n{module.slug}"
        )


        ready = True


        metadata_errors = validate_metadata(
            module
        )


        if not metadata_errors:

            typer.echo(
                "  ✓ metadata.yaml"
            )

        else:

            for error in metadata_errors:

                typer.echo(
                    f"  ✗ {error}"
                )

            ready = False



        if file_has_content(
            module.knowledge
        ):

            typer.echo(
                "  ✓ knowledge.md"
            )

        else:

            typer.echo(
                "  ⚠ knowledge.md needs more content"
            )

            ready = False



        if file_has_content(
            module.blog
        ):

            typer.echo(
                "  ✓ blog.md"
            )

        else:

            typer.echo(
                "  ⚠ blog.md needs more content"
            )

            ready = False

        if module.notebook.exists():

            if notebook_has_content(
                module.notebook
            ):

                typer.echo(
                    "  ✓ notebook.ipynb"
                )

            else:

                typer.echo(
                    "  - notebook.ipynb empty"
                )

        else:

            typer.echo(
                "  - notebook.ipynb missing"
            )        

        generated = module.generated

        required_generated = [
            "posts.md",
            "linkedln.md",
            "quiz.md",
        ]

        optional_generated = [
            "instagram.md",
            "youtube.md",
        ]
        typer.echo("  generated-")

        for filename in required_generated:

            path = generated / filename

            if file_has_content(path):

                typer.echo(
                    f"  ✓ {filename}"
                )

            else:

                typer.echo(
                    f"  ⚠ {filename} missing"
                )

                ready = False


        for filename in optional_generated:

            path = generated / filename

            if file_has_content(path):

                typer.echo(
                    f"  ✓ {filename}"
                )

            else:

                typer.echo(
                    f"  - {filename} optional"
                )        

        typer.echo("  others -")

        if simulation_has_files(
            module.simulation
        ):

            typer.echo(
                "  ✓ simulation"
            )

        else:

            typer.echo(
                "  - simulation empty"
            )



        if folder_has_files(
            module.assets
        ):

            typer.echo(
                "  ✓ assets"
            )

        else:

            typer.echo(
                "  - assets empty"
            )


        if ready:

            typer.echo(
                "  Ready for build."
            )

        else:

            typer.echo(
                "  Incomplete."
            )