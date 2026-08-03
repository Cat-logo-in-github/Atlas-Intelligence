from pathlib import Path

from atlas.browser.edge import (
    get_edge_page,
    close_edge_page,
)

from atlas.utils.filesystem import write_if_changed
from atlas.utils.paths import WEBSITE_DIR


INDEX_PATH = (
    WEBSITE_DIR
    /
    "content"
    /
    "index.md"
)

BLOG_INDEX_PATH = (
    WEBSITE_DIR
    /
    "content"
    /
    "blog.md"
)



def wait_for_chat(page):

    page.wait_for_timeout(5000)

    box = page.locator(
        '[contenteditable="true"]'
    )

    box.wait_for(
        state="visible",
        timeout=60000
    )

    return box



def send_prompt(page, prompt):

    import pyperclip

    box = wait_for_chat(page)

    pyperclip.copy(prompt)

    page.locator(
        "#prompt-textarea"
    ).focus()

    page.keyboard.press(
        "Control+V"
    )

    page.keyboard.press(
        "Enter"
    )



def wait_for_response(page):

    page.wait_for_timeout(5000)

    messages = page.locator(
        '[data-message-author-role="assistant"]'
    )

    previous = ""
    stable = 0

    for _ in range(240):

        if messages.count():

            latest = messages.last

            text = latest.inner_text()

            if text == previous:
                stable += 1
            else:
                stable = 0

            previous = text

            if stable >= 4:
                return text

        page.wait_for_timeout(1000)


    raise RuntimeError(
        "Timed out waiting for response"
    )



def build_index(modules):


    module_data = "\n".join(
        [
            f"- Title: {m.title}\n"
            f"  Slug: {m.slug}\n"
            f"  Tags: {', '.join(m.tags)}\n"
            f"  Difficulty: {m.difficulty}"
            for m in modules
        ]
    )


    prompt = f"""
You are the Atlas Organization Agent.

Your job is to create the homepage index for a personal knowledge atlas.

You receive a list of knowledge modules.

Organize them into meaningful sections.

Rules:

- Do not invent modules.
- Every module must appear exactly once.
- Use the existing slug for links.
- Create useful categories based on the metadata.
- Prefer broad knowledge areas over individual tags.
- The output will be placed directly into Quartz markdown.

Return ONLY markdown.

Format:

# Atlas of Intelligence

Short one sentence description.

## Category Name

- [Module Title](module-slug/)

## Another Category

- [Module Title](module-slug/)


Modules:

{module_data}
"""


    page = get_edge_page()


    try:

        page.goto(
            "https://chatgpt.com/",
            wait_until="domcontentloaded"
        )


        print(
            "Generating Atlas organization..."
        )


        send_prompt(
            page,
            prompt
        )


        response = wait_for_response(
            page
        )


        write_if_changed(
            INDEX_PATH,
            response
        )


        print(
            " ✓ index.md generated"
        )


    finally:

        close_edge_page(
            page
        )


def build_blog_index(modules):

    module_data = "\n".join(
        [
            f"- Title: {m.title}\n"
            f"  Slug: {m.slug}\n"
            f"  Tags: {', '.join(m.tags)}\n"
            f"  Difficulty: {m.difficulty}"
            for m in modules
        ]
    )

    prompt = f"""
You are the Atlas Narrative Organization Agent.

Your job is to create the Blog homepage for a personal knowledge atlas.

This is NOT a table of contents.

Readers should feel like they are exploring ideas rather than browsing files.

Organize the articles into a handful of meaningful themes or learning journeys.

Rules:

- Do not invent articles.
- Every article must appear exactly once.
- Use the existing slug for links.
- Create engaging section names.
- Prefer broad themes over individual tags.
- The output will be placed directly into Quartz markdown.

Return ONLY markdown.

Format:

# Atlas Blog

A one sentence introduction.

## Theme Name

A short sentence describing this theme.

- [Module Title](module-slug/module-slug-blog)

## Another Theme

A short sentence describing this theme.

- [Module Title](module-slug/module-slug-blog)

Articles:

{module_data}
"""

    page = get_edge_page()

    try:

        page.goto(
            "https://chatgpt.com/",
            wait_until="domcontentloaded"
        )

        print(
            "Generating Blog organization..."
        )

        send_prompt(
            page,
            prompt
        )

        response = wait_for_response(
            page
        )

        write_if_changed(
            BLOG_INDEX_PATH,
            response
        )

        print(
            " ✓ blog.md generated"
        )

    finally:

        close_edge_page(
            page
        )