from pathlib import Path
import re
import time

from markdownify import markdownify

from atlas.browser.edge import (
    get_edge_page,
    close_edge_page,
)
from atlas.utils.paths import MODULES_DIR



PROMPT = """
You are writing a technical blog post.

Transform the following knowledge document into a narrative article.

Rules:

- Output ONLY the article.
- Use markdown formatting.
- Start directly with the title.
- No explanations about the transformation.
- No "Here is the blog".
- No conversational introduction.
- Use storytelling.
- Begin with an interesting hook.
- Explain intuition before equations.
- Preserve technical depth.
- Keep useful code examples.
- Use meaningful headings.
- Make it enjoyable for software engineers.

Knowledge document:

"""



# ============================================================
# Cleaning
# ============================================================


def clean_response(text: str):

    text = text.strip()


    # Remove accidental markdown fences

    if text.startswith("```"):

        lines = text.splitlines()

        if lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines)


    # Remove common assistant wrappers

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
# ChatGPT browser
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


            # IMPORTANT:
            # Grab rendered HTML, not text

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

    md = markdownify(
        html,
        heading_style="ATX",
        bullets="-"
    )


    return md.strip()



# ============================================================
# Generator
# ============================================================


def generate_module_blog(
    module_name: str
):


    module_path = (
        MODULES_DIR /
        module_name
    )


    knowledge_path = (
        module_path /
        "knowledge.md"
    )


    output_path = (
        module_path /
        "blog.md"
    )


    if not knowledge_path.exists():

        raise FileNotFoundError(
            knowledge_path
        )


    knowledge = knowledge_path.read_text(
        encoding="utf-8"
    )


    prompt = (
        PROMPT +
        knowledge
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
                "Generated blog too short"
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