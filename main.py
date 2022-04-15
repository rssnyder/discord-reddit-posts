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
        SUBREDDIT_URL + subreddit + ".json",
        headers={
            "User-Agent": "linux:github.discord-reddit-posts:v0.0.1 (by /u/Optimus_Banana)"
        },
    )

    response.raise_for_status()

    return response.json().get("data", {}).get("children", [])


if __name__ == "__main__":

    if getenv("WEBHOOK_URL"):
        db_name = getenv("DB") or "posts.json"
        posts_db = TinyDB(db_name)
        posts = Query()

        for post in get_posts(getenv("SUBREDDIT")):

            if posts_db.search(posts.id == post["data"]["id"]):
                print("already sent post")
                continue

            link = ""
            if getenv("POST_DOMAIN"):
                if (
                    getenv("POST_DOMAIN").lower()
                    in post["data"].get("domain", "").lower()
                ):
                    link = "https://reddit.com" + post["data"].get(
                        "permalink", "/r/" + getenv("SUBREDDIT")
                    )

            if getenv("POST_TITLE"):
                print(post["data"].get("title", ""))
                if (
                    getenv("POST_TITLE").lower()
                    in post["data"].get("title", "").lower()
                ):
                    link = "https://reddit.com" + post["data"].get(
                        "permalink", "/r/" + getenv("SUBREDDIT")
                    )

            if not link:
                continue

            for webhook_url in getenv("WEBHOOK_URL").split(";"):
                webhook = DiscordWebhook(url=webhook_url, content=link)

                response = webhook.execute()

                if response.status_code == 200:
                    posts_db.insert({"id": post["data"]["id"]})
                    print("sent " + post["data"]["id"])

            sleep(5)
