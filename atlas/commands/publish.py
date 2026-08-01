import typer
import json
from pathlib import Path
from atlas.publishers.substack import publish_substack
from atlas.publishers.linkedln import publish_linkedin
from atlas.publishers.reddit_post import publish_reddit_post
from atlas.publishers.github import publish_module
from atlas.publishers.reddit import publish_reddit
from atlas.browser.edge import close_edge_page,shutdown_browser
from atlas.utils.urls import REDDIT_COMMUNITIES

PUBLISH_QUEUE = Path("atlas/outputs/publish_queue.json")


app = typer.Typer(
    no_args_is_help=True,
    help="Publish modules"
)


@app.callback()
def main():
    """
    Publish modules.
    """
    pass


@app.command()
def substack(
    module_name: str,
):
    """
    Publish a module to Substack.
    """

    publish_substack(
        module_name
    )


@app.command()
def linkedln(
    module_name: str,
):
    """
    Publish a module to LinkedIn.
    """
    try:
        publish_linkedin(
            module_name
        )
    finally:
        shutdown_browser()


@app.command()
def reddit_post(
    module_name: str,
    subreddit: str = None,
):
    """
    Publish a Post to Reddit.
    """
    communities = (
        [subreddit]
        if subreddit
        else REDDIT_COMMUNITIES
    )
    try:
        for community in communities:
            print(f"\nPublishing {module_name} -> r/{community}")
            publish_reddit_post(
                module_name,
                community
            )
    finally:
        close_edge_page()
        shutdown_browser()

@app.command()
def reddit(
    module_name: str,
    subreddit: str = None,
):
    """
    Publish a Module/(knowledge.md) to Reddit.
    """
    communities = (
        [subreddit]
        if subreddit
        else REDDIT_COMMUNITIES
    )
    try:
        for community in communities:
            print(f"\nPublishing {module_name} -> r/{community}")
            publish_reddit(
                module_name,
                community
            )
    finally:
        close_edge_page()
        shutdown_browser()

@app.command()
def github(
    module_name: str
):

    publish_module(
        module_name
    )


def load_publish_queue():

    if not PUBLISH_QUEUE.exists():
        return []


    text = PUBLISH_QUEUE.read_text(
        encoding="utf-8"
    ).strip()


    if not text:
        return []


    return json.loads(text)

@app.command()
def module(
    module_name: str,
):
    """
    Schedule and publish a completed module.
    """
    from atlas.commands.build import build

    build()
    publish_module(module_name)

    
    queue = load_publish_queue()
    # Substack happens now (human review)
    typer.echo(
        "\nOpening Substack draft..."
    )

    publish_substack(
        module_name
    )


    answer = typer.confirm(
        "\nSubstack looks good. Continue with Reddit?"
    )

    if answer:
        try:
            for community in REDDIT_COMMUNITIES:
                print(f"\nPublishing {module_name} -> r/{community}")
                publish_reddit(
                    module_name,
                    community,
                )
        finally:
            shutdown_browser()

        typer.echo("\n✓ Reddit published")


    # Queue future LinkedIn + Reddit posts

    for day in range(5):

        queue.append({
            "days": day,
            "type": "linkedin",
            "module": module_name,
        })


    for day in range(10):

        queue.append({
            "days": day,
            "type": "reddit_post",
            "module": module_name,
        })


    PUBLISH_QUEUE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    PUBLISH_QUEUE.write_text(
        json.dumps(
            queue,
            indent=4
        ),
        encoding="utf-8",
    )


    typer.echo(
        f"\n✓ Scheduled publishing for '{module_name}'"
    )

    typer.echo(
        "  • LinkedIn : 5 posts"
    )

    typer.echo(
        "  • Reddit posts : 10 posts"
    )

    close_edge_page()
    shutdown_browser()