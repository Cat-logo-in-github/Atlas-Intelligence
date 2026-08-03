import typer
import sys
from atlas.dashboard import show_dashboard
from atlas.commands.create import create
from atlas.commands.build import build
from atlas.commands.check import check
from atlas.commands.list import list_modules
from atlas.commands.version import version
from atlas.commands.run import run


app = typer.Typer(
    no_args_is_help=True,
    help="Atlas - Knowledge management CLI"
)


from atlas.commands.generate import app as generate_app

app.add_typer(
    generate_app,
    name="generate"
)


from atlas.commands.publish import app as publish_app

app.add_typer(
    publish_app,
    name="publish"
)

from atlas.commands.make import app as make_app

app.add_typer(
    make_app,
    name="make"
)


app.command()(create)

app.command()(build)

app.command()(check)

app.command()(run)

app.command("list")(list_modules)

app.command()(version)


def main():
    if len(sys.argv) == 1:
        show_dashboard()
    else:
        app()