from pathlib import Path
import urllib.parse

import requests
import typer

from atlas.utils.paths import MODULES_DIR


STYLE = """
Create a clean illustrative image of the Prompt.

Style:
- flat vector
- white background
- thumbnail like professional quality
- minimal colors
- no decorative elements

Rules:
- no text
- no labels
- no captions
- clear geometric shapes
- suitable for understanding
"""


def generate_image(
    prompt: str,
    output: Path,
):

    full_prompt = f"""
{STYLE}

Diagram:
{prompt}
"""

    encoded = urllib.parse.quote(full_prompt)

    url = (
        "https://image.pollinations.ai/prompt/"
        + encoded
        + "?model=flux"
        + "&width=1400"
        + "&height=900"
    )

    print("\nGenerating diagram...")

    response = requests.get(
        url,
        timeout=180,
    )

    response.raise_for_status()

    output.write_bytes(response.content)


def generate_module_image(
    module_name: str,
):

    module = (
        MODULES_DIR
        / module_name
    )

    assets = (
        module
        / "assets"
    )

    assets.mkdir(
        exist_ok=True
    )

    title = typer.prompt(
        "TITLE"
    ).strip()

    prompt = typer.prompt(
        "PROMPT"
    ).strip()

    filename = (
        title
        .lower()
        .replace(" ", "-")
        + ".png"
    )

    output = (
        assets
        / filename
    )

    generate_image(
        prompt,
        output,
    )

    print(
        f"\nSaved:\n{output}"
    )