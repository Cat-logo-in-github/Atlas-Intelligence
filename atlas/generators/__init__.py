import typer

from atlas.generators.simulation import (
    generate_simulation,
)

from atlas.generators.youtube import (
    generate_youtube,
)

app = typer.Typer()

app.command("simulation")(
    generate_simulation
)

app.command("youtube")(
    generate_youtube
)