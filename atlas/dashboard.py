# atlas/dashboard.py

import json
from pathlib import Path
from datetime import datetime

from atlas.publishers.linkedln import publish_linkedin
from atlas.publishers.reddit_post import publish_reddit_post
from atlas.browser.edge import shutdown_browser
from atlas.utils.urls import REDDIT_COMMUNITIES

QUEUE_PATH = Path("atlas/outputs/publish_queue.json")


ATLAS_ASCII = r"""
                     █████╗ ████████╗██╗      █████╗ ███████╗
                    ██╔══██╗╚══██╔══╝██║     ██╔══██╗██╔════╝
                    ███████║   ██║   ██║     ███████║███████╗
                    ██╔══██║   ██║   ██║     ██╔══██║╚════██║
                    ██║  ██║   ██║   ███████╗██║  ██║███████║
                    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝                  
"""


def load_queue():

    if not QUEUE_PATH.exists():
        return []

    return json.loads(
        QUEUE_PATH.read_text(
            encoding="utf-8"
        )
    )


def save_queue(queue):

    QUEUE_PATH.write_text(
        json.dumps(
            queue,
            indent=4
        ),
        encoding="utf-8"
    )


def publish_job(job):

    module = job["module"]

    if job["type"] == "linkedin":
        try:
            publish_linkedin(
                module
            )
        finally:
            shutdown_browser()


    elif job["type"] == "reddit_post":
        """
        Publish a Post to Reddit.
        """ 
        try:
            for community in REDDIT_COMMUNITIES:
                print(f"\nPublishing {module} -> r/{community}")
                publish_reddit_post(
                    module,
                    community
                )
        finally:
            shutdown_browser()    


def show_dashboard():

    print(ATLAS_ASCII)

    print(
        "       Knowledge becomes momentum. Your Personal content automation engine\n\n"
    )

    print(
        "──────────────────────────────────────────"
    )

    queue = load_queue()


    today = [
        x for x in queue
        if x["days"] == 0
    ]


    future = [
        x for x in queue
        if x["days"] > 0
    ]


    linkedin_remaining = len([
        x for x in queue
        if x["type"] == "linkedin"
    ])

    reddit_remaining = len([
        x for x in queue
        if x["type"] == "reddit_post"
    ])


    print(
        """
Status
──────────────────────────────────────────
"""
    )

    print(
        f"Pending Publications\n"
        f"  Today: {len(today)}\n"
        f"  Future: {len(future)}\n"
    )


    print(
        f"Remaining\n"
        f" LinkedIn : {linkedin_remaining}\n"
        f" Reddit   : {reddit_remaining}\n"
    )


    print(
        "──────────────────────────────────────────"
    )


    if not today:

        print(
                """
No Publications due today.
──────────────────────────────────────────
        """
            )

        return


    print(
        "\nGood afternoon.\n"
    )


    print(
        "Publishing Queue\n"
    )


    for job in today:

        platform = (
            "LinkedIn"
            if job["type"] == "linkedin"
            else "Reddit"
        )

        print(
            f" • {platform}\n"
            f"   {job['module']}\n"
        )


    print(
        "──────────────────────────────────────────"
    )


    answer = input(
        "\nPublish today's posts now? [Y/n] "
    )


    if answer.lower() == "n":

        print(
            "\nQueue unchanged.\n"
        )

        return


    publish_today(today, queue)



def publish_today(today, queue):

    completed = []


    try:

        for job in today:

            publish_job(job)

            print(
                f"\n✓ {job['type']} published"
            )

            completed.append(job)


    finally:

        shutdown_browser()



    remaining = [
        job for job in queue
        if job not in completed
    ]


    for job in remaining:

        if job["days"] > 0:
            job["days"] -= 1


    save_queue(
        remaining
    )


    print(
        """
──────────────────────────────────────────

Today's queue complete.

Next publish:
Tomorrow

──────────────────────────────────────────
"""
    )