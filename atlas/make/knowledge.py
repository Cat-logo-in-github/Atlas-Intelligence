from pathlib import Path
import re

from markdownify import markdownify

from atlas.browser.edge import (
    get_edge_page,
    close_edge_page,
)
from atlas.utils.paths import MODULES_DIR



PROMPT = """
You are converting a technical blog article into a structured knowledge document.

Transform the article into a reference-quality technical knowledge page.

Rules:

- Output ONLY markdown.
- Start directly with the title.
- No explanation of the conversion.
- No "Here is the knowledge document".
- No storytelling.
- Remove unnecessary narrative language.
- Preserve all important technical information.
- Preserve equations.
- Preserve code examples.
- Preserve important examples and analogies.
- Use clear hierarchical headings.

The structure should generally follow:

# Topic Name

## The Question

Explain the fundamental problem being solved.

## Intuition

Explain the concept simply.

## Mathematics

Include formulas and definitions.

## Implementation

Include code examples where relevant.

## Visualization

Explain diagrams, processes, or mental models.

## Connections

Explain relationships to other fields.

## Limitations / Open Questions

Include unresolved issues.

## Key Takeaway

Summarize the core idea.

Adapt sections when necessary. Do not force empty sections.

Technical article:

"""



# ============================================================
# Cleaning
# ============================================================


def clean_response(text: str):

    text = text.strip()


    if text.startswith("```"):

        lines = text.splitlines()


        if lines[0].startswith("```"):
            lines = lines[1:]


        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]


        text = "\n".join(lines)



    patterns = [
        r"^Sure[!.]?\s*",
        r"^Certainly[!.]?\s*",
        r"^Here is.*?:\s*",
        r"^Here's.*?:\s*",
        r"^Below is.*?:\s*",
    ]


    for pattern in patterns:

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE
        )


    return text.strip()



# ============================================================
# Browser
# ============================================================


def wait_for_chat(page):

    page.wait_for_timeout(
        5000
    )


    box = page.locator(
        '[contenteditable="true"]'
    )


    box.wait_for(
        state="visible",
        timeout=60000
    )


    return box



def send_prompt(page, prompt):

    box = wait_for_chat(
        page
    )


    box.click()


    page.keyboard.insert_text(
        prompt
    )


    page.keyboard.press(
        "Enter"
    )



def wait_for_response(page):

    print(
        "Waiting for ChatGPT response..."
    )


    messages = page.locator(
        '[data-message-author-role="assistant"]'
    )


    previous = ""

    stable = 0


    for _ in range(240):

        count = messages.count()


        if count:

            latest = messages.last


            html = latest.inner_html()


            if html:

                if html == previous:

                    stable += 1

                else:

                    stable = 0


                previous = html


                print(
                    "HTML chars:",
                    len(html)
                )


                if stable >= 4:

                    return html


        page.wait_for_timeout(
            1000
        )


    raise RuntimeError(
        "Timed out waiting for ChatGPT"
    )



# ============================================================
# HTML -> Markdown
# ============================================================


def html_to_markdown(html):

    return markdownify(
        html,
        heading_style="ATX",
        bullets="-"
    ).strip()



# ============================================================
# Generator
# ============================================================


def generate_module_knowledge(
    module_name: str
):


    module_path = (
        MODULES_DIR /
        module_name
    )


    blog_path = (
        module_path /
        "blog.md"
    )


    output_path = (
        module_path /
        "knowledge.md"
    )


    if not blog_path.exists():

        raise FileNotFoundError(
            blog_path
        )



    blog = blog_path.read_text(
        encoding="utf-8"
    )


    prompt = (
        PROMPT +
        blog
    )


    page = get_edge_page()

    try:
        page.goto(
            "https://chatgpt.com/",
            wait_until="domcontentloaded"
        )


        print(
            "Opened ChatGPT"
        )


        send_prompt(
            page,
            prompt
        )


        html = wait_for_response(
            page
        )


        markdown = html_to_markdown(
            html
        )


        markdown = clean_response(
            markdown
        )


        if len(markdown) < 200:

            raise RuntimeError(
                "Generated knowledge document too short"
            )


        output_path.write_text(
            markdown,
            encoding="utf-8"
        )


        print(
            "Saved:",
            output_path
        )
    finally:
        close_edge_page(page)