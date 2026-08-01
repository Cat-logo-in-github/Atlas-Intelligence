import typer

from atlas.generators.simulation import (
    generate_simulation
)

from atlas.generators.youtube import (
    generate_youtube
)

from atlas.generators.instagram import (
    generate_instagram
)

from atlas.generators.Linkedln import (
    generate_linkedln
)

from atlas.generators.quiz import (
    generate_quiz
)

from atlas.generators.post import (
    generate_posts
)

from atlas.generators.metadata import (
    generate_metadata
)

from atlas.make.liimages import (
    generate_module_liimages
)


def generate_all(
    slug: str,
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing generated files",
    ),
):

    generate_metadata(
        slug
    )

    generate_youtube(
        slug,
        force=force
    )

    generate_instagram(
        slug,
        force=force
    )

    generate_quiz(
        slug,
        force=force
    )

    generate_posts(
        slug,
        force=force
    )

    generate_linkedln(
        slug,
        force=force
    )

    generate_module_liimages(
        slug
    )


app = typer.Typer(help="Generate information/content: Simulation output/ Youtube/Instagram Script/ Linkedin/Posts/ Quiz/ MetaData")


app.command("simulation",
            help="Generates a run folder that makes outputs from simulation objects. See CONTRACT.md")(
    generate_simulation
)


app.command("youtube",
            help="Only a 10 min outline currently")(
    generate_youtube
)

app.command("instagram",
            help="Full script :)")(
    generate_instagram
)

app.command("linkdln")(
    generate_linkedln
)

app.command("quiz")(
    generate_quiz
)

app.command("posts")(
    generate_posts
)

app.command("metadata",
            help="Generates edges to link nodes. Read GRAPH.md")(
    generate_metadata
)

app.command("all")(
    generate_all
)

app.command("liimages")(
    generate_module_liimages
)