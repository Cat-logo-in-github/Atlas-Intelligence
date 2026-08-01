import typer

from atlas.make.blog import generate_module_blog
from atlas.make.knowledge import generate_module_knowledge
from atlas.make.image import generate_module_image
from atlas.make.simulation import make_simulation
from atlas.make.research import make_research
from atlas.browser.edge import shutdown_browser

app = typer.Typer(help="make content for publishing: Images, Blog, Structured Data")


@app.command()
def blog(
    module_name: str
):
    """
    Generate blog from knowledge.
    """
    try:
        generate_module_blog(
            module_name
        )
    finally:
        shutdown_browser()

@app.command()
def knowledge(
    module_name: str
):
    """
    Generate Knowledge Structure from A personal blog.
    """
    try:
        generate_module_knowledge(
            module_name
        )
    finally:
        shutdown_browser()

@app.command()
def illustration(
    module_name: str
):
    """
    Generate Image asset for a prompt.
    """
    generate_module_image(
        module_name
    )

@app.command()
def simulation(
    module_name: str,
    research: bool = typer.Option(
        False,
        "--research",
        "-r",
        help="Use the latest research handoff.",
    ),
):
    try:
        make_simulation(
            module_name,
            research,
        )
    finally:
        shutdown_browser()

@app.command()
def research(
):
    """
    Generate Research for implementing simulation for a prompt.
    """
    try:
        make_research()
    finally:
        shutdown_browser()