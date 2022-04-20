from time import sleep
from os import getenv

from requests import get
from discord_webhook import DiscordWebhook, DiscordEmbed
from tinydb import TinyDB, Query

SUBREDDIT_URL = "https://reddit.com/r/"


def get_posts(subreddit: str) -> dict:
    """
    Get recent posts from reddit
    """

    response = get(
        SUBREDDIT_URL + subreddit + "/new.json",
        headers={
            "User-Agent": f"linux:github.discord-reddit-posts:v0.0.1 (by github.com/{getenv('GITHUB_ACTOR', 'rssnyder')})"
        },
    )

    response.raise_for_status()

    return response.json().get("data", {}).get("children", [])


if __name__ == "__main__":

    db_name = getenv("DB", "posts.json")
    posts_db = TinyDB(db_name)
    posts = Query()

    for post in get_posts(getenv("SUBREDDIT", "all")):

        if posts_db.search(posts.id == post["data"]["id"]):
            print("already sent post")
            continue

        link = ""

        if getenv("POST_DOMAIN"):
            for domain in getenv("POST_DOMAIN").split(";"):
                if domain.lower() in post["data"].get("domain", "").lower():
                    link = "https://reddit.com" + post["data"].get(
                        "permalink", "/r/" + getenv("SUBREDDIT") + "/new"
                    )

        if getenv("POST_TITLE"):
            for title in getenv("POST_TITLE").split(";"):
                if title.lower() in post["data"].get("title", "").lower():
                    link = "https://reddit.com" + post["data"].get(
                        "permalink", "/r/" + getenv("SUBREDDIT", "all") + "/new"
                    )

        if not link:
            continue

        for webhook_url in getenv("WEBHOOK_URL", "").split(";"):
            webhook = DiscordWebhook(url=webhook_url, content=link)

            response = webhook.execute()

            if response.status_code == 200:
                posts_db.insert({"id": post["data"]["id"]})
                print("sent " + post["data"]["id"])

        sleep(5)
