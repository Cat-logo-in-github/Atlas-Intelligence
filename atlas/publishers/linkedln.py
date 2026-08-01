from pathlib import Path
import re
import time
import io

from PIL import Image
import win32clipboard
import win32con

from atlas.browser.edge import (
    get_edge_page,
    close_edge_page,
    stabilize_page,
)
from atlas.utils.paths import MODULES_DIR
from atlas.utils.urls import (
    WEBSITE_LINK,
    GITHUB_LINK,
    INSTAGRAM_ID_LINK,
    YOUTUBE_ID,
)


# ============================================================
# Clipboard image handling
# ============================================================

def copy_image_to_clipboard(image_path: Path):

    image = Image.open(
        image_path
    )

    image = image.convert(
        "RGB"
    )

    output = io.BytesIO()

    image.save(
        output,
        "BMP"
    )

    data = output.getvalue()[14:]


    win32clipboard.OpenClipboard()

    try:

        win32clipboard.EmptyClipboard()

        win32clipboard.SetClipboardData(
            win32con.CF_DIB,
            data
        )

    finally:

        win32clipboard.CloseClipboard()



# ============================================================
# Markdown parsing
# ============================================================

def clean_linkedin_text(text: str):

    # Remove everything from Suggested Asset onward
    text = re.split(
        r"\*\*Suggested Asset:\*\*|Suggested Asset:",
        text,
        flags=re.IGNORECASE
    )[0]


    # Remove markdown bold markers
    text = text.replace(
        "**",
        ""
    )


    return text.strip()


def find_next_post(path: Path):

    md = path.read_text(
        encoding="utf-8"
    )


    posts = re.split(
        r"(?=### Post \d+:)",
        md
    )


    for post in posts:

        if not post.strip():
            continue


        header = post.splitlines()[0]


        if "(published)" in header:
            continue


        text_match = re.search(
            r"Text:\s*(.*)",
            post,
            flags=re.DOTALL
        )


        if not text_match:
            continue


        clean_text = clean_linkedin_text(
            text_match.group(1)
        )


        image_match = re.search(
            r"([A-Za-z0-9_\-]+\.(png|jpg|jpeg|webp|gif))",
            post,
            flags=re.IGNORECASE
        )


        return {
            "header": header,
            "text": clean_text,
            "image": (
                image_match.group(1)
                if image_match
                else None
            )
        }


    return None

def linkedin_footer():

    links = []


    if WEBSITE_LINK:
        links.append(
            f"Check the Atlas: {WEBSITE_LINK}"
        )


    if GITHUB_LINK:
        links.append(
            f"Github: {GITHUB_LINK}"
        )


    if INSTAGRAM_ID_LINK:
        links.append(
            f"Instagram: {INSTAGRAM_ID_LINK}"
        )


    if YOUTUBE_ID:
        links.append(
            f"Youtube: {YOUTUBE_ID}"
        )


    if not links:
        return ""


    return (
        "Follow for more:\n" +
        "\n".join(links)
    )
    

def mark_post_published(
    path: Path,
    header: str
):

    md = path.read_text(
        encoding="utf-8"
    )


    md = md.replace(
        header,
        header + " (published)",
        1
    )


    path.write_text(
        md,
        encoding="utf-8"
    )



# ============================================================
# LinkedIn composer
# ============================================================

def click_start_post(page):

    print(
        "Finding Start a post..."
    )


    button = page.get_by_text(
        "Start a post",
        exact=True
    )


    print(
        "Found:",
        button.count()
    )


    if button.count() == 0:

        raise RuntimeError(
            "Start a post button missing"
        )


    button.first.click()


    print(
        "Clicked Start a post"
    )



def wait_for_editor(page):

    print(
        "Waiting for editor..."
    )


    selectors = [
        '[contenteditable="true"]',
        '[role="textbox"]',
        '.ql-editor',
    ]


    for i in range(60):

        print(
            "Editor scan",
            i
        )


        for selector in selectors:

            loc = page.locator(selector)


            for x in range(loc.count()):

                el = loc.nth(x)


                try:

                    if el.is_visible():

                        print(
                            "Using editor:",
                            selector,
                            x,
                            el.get_attribute("aria-label"),
                            el.get_attribute("class")
                        )

                        return el


                except:
                    pass


        page.wait_for_timeout(
            1000
        )


    raise RuntimeError(
        "LinkedIn composer did not appear"
    )


def insert_text(
    page,
    editor,
    text
):

    editor.click()

    page.wait_for_timeout(
        500
    )


    page.keyboard.type(
        text,
        delay=1
    )


    page.wait_for_timeout(
        1000
    )

def click_post(page):

    print(
        "Looking for LinkedIn Post button..."
    )


    # Let React finish rendering the composer controls
    page.wait_for_timeout(
        3000
    )


    buttons = page.locator(
        "button"
    )


    print(
        "Total buttons:",
        buttons.count()
    )


    for i in range(buttons.count()):

        try:

            button = buttons.nth(i)


            if not button.is_visible():
                continue


            text = button.inner_text().strip()

            aria = button.get_attribute(
                "aria-label"
            )


            print(
                i,
                repr(text),
                aria
            )


            if (
                text == "Post"
                or aria == "Post"
                or "Post" in (aria or "")
            ):

                print(
                    "FOUND POST BUTTON:",
                    i
                )


                button.click(
                    force=True
                )


                print(
                    "Post clicked"
                )


                page.wait_for_timeout(
                    5000
                )


                return


        except Exception as e:

            print(
                "Button scan error:",
                e
            )


    raise RuntimeError(
        "LinkedIn Post button not found"
    )

# ============================================================
# Publisher
# ============================================================

def publish_linkedin(
    module_name: str
):

    module_path = (
        MODULES_DIR /
        module_name
    )


    post_path = (
        module_path /
        "generated" /
        "linkedln.md"
    )


    if not post_path.exists():

        raise FileNotFoundError(
            post_path
        )



    post = find_next_post(
        post_path
    )


    if post is None:

        print(
            "All LinkedIn posts published."
        )

        return



    page = get_edge_page()

    try:
        page.goto(
            "https://www.linkedin.com/feed/",
            wait_until="domcontentloaded"
        )

        stabilize_page(page)


        print(
            "LinkedIn loaded"
        )


        page.wait_for_timeout(
            10000
        )


        click_start_post(
            page
        )


        # LinkedIn needs time to mount Quill editor
        page.wait_for_timeout(
            5000
        )


        editor = wait_for_editor(
            page
        )


        insert_text(
            page,
            editor,
            post["text"]
        )


        print(
            "Text inserted"
        )


        # ----------------------------------------
        # Optional image
        # ----------------------------------------

        if post["image"]:

            image_path = (
                module_path /
                "assets" /
                post["image"]
            )


            if image_path.exists():

                print(
                    "Adding image:",
                    image_path
                )


                page.keyboard.press(
                    "Enter"
                )


                copy_image_to_clipboard(
                    image_path
                )


                page.keyboard.press(
                    "Control+V"
                )


                page.wait_for_timeout(
                    5000
                )


            else:

                print(
                    "Image missing:",
                    image_path
                )

        footer = linkedin_footer()

        if footer:

            page.keyboard.press(
                "Enter"
            )

            page.keyboard.insert_text(
                "\n" + footer
            )


        print(
            "\nLinkedIn draft ready."
        )


        print(
            "\nLinkedIn publishing..."
        )


        click_post(page)


        mark_post_published(
            post_path,
            post["header"]
        )


        print(
            "Published and marked."
        )

    finally:
        close_edge_page(page)

if __name__ == "__main__":

    publish_linkedin(
        "gradient-descent"
    )