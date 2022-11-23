from time import sleep
from os import getenv

from requests import get, post
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
                        "permalink", "/r/" + getenv("SUBREDDIT", "all") + "/new"
                    )

        if getenv("POST_TITLE") and not link:
            for title in getenv("POST_TITLE").split(";"):
                if title.lower() in post["data"].get("title", "").lower():
                    link = "https://reddit.com" + post["data"].get(
                        "permalink", "/r/" + getenv("SUBREDDIT", "all") + "/new"
                    )

        if getenv("POST_TEXT") and not link:
            for text in getenv("POST_TEXT").split(";"):
                if text.lower() in post["data"].get("selftext", "").lower():
                    link = "https://reddit.com" + post["data"].get(
                        "permalink", "/r/" + getenv("SUBREDDIT", "all") + "/new"
                    )

        if getenv("POST_AUTHOR") and not link:
            for author in getenv("POST_AUTHOR").split(";"):
                if author.lower() in post["data"].get("author", "").lower():
                    link = "https://reddit.com" + post["data"].get(
                        "permalink", "/r/" + getenv("SUBREDDIT", "all") + "/new"
                    )

        if not link:
            continue

        if getenv("WEBHOOK_URL"):
            for webhook_url in getenv("WEBHOOK_URL", "").split(";"):
                webhook = DiscordWebhook(url=webhook_url, content=link)

                response = webhook.execute()

                if response.status_code == 200:
                    posts_db.insert({"id": post["data"]["id"]})
                    print("sent " + post["data"]["id"])
                else:
                    print("discord fail: " + post["data"]["id"])

        if getenv("PUSHOVER_APP") and getenv("PUSHOVER_USER"):
            resp = post(
                "https://api.pushover.net/1/messages.json",
                json={
                    "token": getenv("PUSHOVER_APP"),
                    "user": getenv("PUSHOVER_USER"),
                    "title": "r/" + getenv("SUBREDDIT", "all"),
                    "message": link,
                },
            )

            try:
                resp.raise_for_status()
            except:
                print("pushover fail: " + post["data"]["id"])
            else:
                posts_db.insert({"id": post["data"]["id"]})
                print("sent " + post["data"]["id"])

        sleep(5)
