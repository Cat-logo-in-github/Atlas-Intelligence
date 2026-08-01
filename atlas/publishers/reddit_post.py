from pathlib import Path
import re

from atlas.browser.edge import (
    get_edge_page,
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
# Markdown
# ============================================================

def clean_text(text):
    return re.split(
        r"## Asset",
        text,
        flags=re.IGNORECASE
    )[0].strip()


def find_next_post(path: Path, community_name):

    md = path.read_text(
        encoding="utf-8"
    )

    title_match = re.search(
        r"^# (.+)$",
        md,
        re.MULTILINE
    )

    title = (
        title_match.group(1).strip()
        if title_match
        else "Atlas"
    )


    posts = re.split(
        r"(?=^# Post \d+)",
        md,
        flags=re.MULTILINE
    )


    for post in posts:

        header_match = re.search(
            r"^# Post \d+(?: \(reddit:[^)]+\))*",
            post,
            re.MULTILINE
        )

        if not header_match:
            continue


        header = header_match.group(0)


        if f"(reddit:{community_name})" in post:
            continue


        text_match = re.search(
            r"## Text\s*(.*?)\s*## Asset",
            post,
            re.DOTALL
        )


        asset_match = re.search(
            r"([\w\-]+\.(png|jpg|jpeg|webp|gif))",
            post,
            re.I
        )


        return {
            "header": header,
            "title": title,
            "text": clean_text(text_match.group(1))
            if text_match else "",
            "image": asset_match.group(1)
            if asset_match else None
        }


    return None



def mark_post_published(
    path: Path,
    header: str,
    subreddit: str
):

    md = path.read_text(
        encoding="utf-8"
    )

    new_header = (
        header +
        f" (reddit:{subreddit})"
    )

    md = md.replace(
        header,
        new_header,
        1
    )

    path.write_text(
        md,
        encoding="utf-8"
    )

# ============================================================
# Reddit elements
# ============================================================

def wait_title(page):

    for _ in range(60):

        el = page.locator(
            'textarea[name="title"]'
        )


        if el.count() and el.first.is_visible():

            return el.first


        page.wait_for_timeout(1000)


    raise RuntimeError(
        "Title missing"
    )



def wait_body(page):

    print(
        "Searching Reddit body..."
    )


    for i in range(60):

        editors = page.locator(
            'div[aria-label="Post body text field"][contenteditable="true"]'
        )


        print(
            "body scan",
            i,
            editors.count()
        )


        for x in range(editors.count()):

            el = editors.nth(x)


            try:

                if el.is_visible():

                    box = el.bounding_box()

                    if box:

                        print(
                            "Using body",
                            x,
                            box
                        )

                        return el


            except:
                pass


        page.wait_for_timeout(1000)


    raise RuntimeError(
        "Body missing"
    )

# ============================================================
# Footer
# ============================================================

def reddit_footer():

    links = []


    if WEBSITE_LINK:
        links.append(
            f"Website: {WEBSITE_LINK}"
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
        "\n\n---\n\n"
        "Follow Atlas for more:\n" +
        "\n".join(links)
    )

# ============================================================
# Body
# ============================================================

def insert_body(
    page,
    body,
    text
):

    print(
        "Clicking body"
    )


    body.click(
        force=True
    )


    page.wait_for_timeout(
        1000
    )


    active = page.evaluate(
        """
        () => ({
            tag: document.activeElement.tagName,
            role: document.activeElement.getAttribute("role"),
            aria: document.activeElement.getAttribute("aria-label")
        })
        """
    )


    print(
        "ACTIVE:",
        active
    )


    page.keyboard.insert_text(
        text
    )


    page.wait_for_timeout(
        3000
    )


    visible = body.inner_text()


    print(
        "VISIBLE BODY:",
        repr(visible[:100])
    )


    if len(visible.strip()) < 5:

        raise RuntimeError(
            "Reddit rejected body input"
        )


# ============================================================
# Upload
# ============================================================

def upload_image(
    page,
    image
):

    inputs = page.locator(
        'input[type="file"]'
    )


    print(
        "Uploads:",
        inputs.count()
    )


    inputs.nth(0).set_input_files(
        str(image)
    )


    page.wait_for_timeout(
        5000
    )



# ============================================================
# Publisher
# ============================================================

def select_community(page, community_name: str):

    print("Opening community picker")

    page.get_by_role(
        "button",
        name="Select Community"
    ).click(
        force=True
    )

    page.wait_for_timeout(2000)


    search = page.locator(
        'textarea[placeholder="Search"]'
    ).first


    search.wait_for(
        state="visible",
        timeout=10000
    )


    print(
        "Typing:",
        community_name
    )


    search.fill(
        community_name
    )


    page.wait_for_timeout(
        3000
    )


    print(
        "Looking for result..."
    )


    result = page.get_by_text(
        "r/" + community_name,
        exact=True
    ).last


    result.wait_for(
        state="visible",
        timeout=10000
    )


    print(
        "Found:",
        result.inner_text()
    )


    # Reddit's clickable area is usually the nearest
    # div with a pointer cursor
    clicked = False


    for level in range(1, 8):

        candidate = result.locator(
            "xpath=" + "/.." * level
        )


        try:

            if candidate.is_visible():

                box = candidate.bounding_box()

                if box:

                    print(
                        "Trying parent",
                        level,
                        box
                    )


                    candidate.click(
                        force=True
                    )

                    clicked = True
                    break


        except Exception:

            pass


    if not clicked:

        print(
            "Falling back to text click"
        )

        result.click(
            force=True
        )


    page.wait_for_timeout(
        5000
    )


    print(
        "Community selected"
    )

def click_post(page):

    print(
        "Waiting for Post button..."
    )

    button = page.get_by_role(
        "button",
        name="Post",
        exact=True
    )


    button.wait_for(
        state="visible",
        timeout=15000
    )


    print(
        "Post button found"
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

def publish_reddit_post(module_name: str, community_name: str):


    module_path = MODULES_DIR / module_name


    post_path = (
        module_path /
        "generated" /
        "posts.md"
    )


    post = find_next_post(
        post_path,
        community_name
    )


    if not post:

        print(
            "No posts"
        )

        return



    page = get_edge_page(reuse=True)

    try:
        page.goto(
            "about:blank"
        )

        page.wait_for_timeout(1000)

        page.goto(
            "https://www.reddit.com/submit?type=TEXT",
            wait_until="domcontentloaded"
        )

        stabilize_page(page)


        print(
            "Reddit loaded"
        )


        page.wait_for_timeout(
            5000
        )

        
        select_community(
            page,
            community_name
        )

        print(
            "Reddit Community Selected"
        )

        title = wait_title(page)


        title.fill(
            post["title"]
        )


        print(
            "Title done"
        )

        body = wait_body(page)
        text = post["text"]
        footer = reddit_footer()
        if footer:

            text += footer


        insert_body(
            page,
            body,
            text
        )

        if post["image"]:

            image = (
                module_path /
                "assets" /
                post["image"]
            )


            if image.exists():

                upload_image(
                    page,
                    image
                )


        print(
            "Reddit draft ready"
        )

        click_post(page)

        page.wait_for_timeout(
            5000
        )

        mark_post_published(
            post_path,
            post["header"],
            community_name
        )


        print(
            "Published marker added"
        )
    finally:
        try:
            page.goto("about:blank")
        except Exception:
            pass



if __name__ == "__main__":

    publish_reddit_post(
        "gradient-descent",
        "learnmachinelearning"
    )