# discord-reddit-posts

[![.github/workflows/run.yml](https://github.com/rssnyder/discord-reddit-posts/actions/workflows/run.yml/badge.svg)](https://github.com/rssnyder/discord-reddit-posts/actions/workflows/run.yml)

send new posts from reddit via title or domain

powered by github's generosity

## usage

```env
SUBREDDIT=hardwareswap                            # subreddit to watch
WEBHOOK_URL=https://discord.com/api/webhooks/xxx  # discord webhook url (supports multiple seperated by ;)
POST_DOMAIN=cnn.com                               # domain of a link posted (supports multiple seperated by ;)
POST_TITLE=keyboard                               # keyword to look for in post title (supports multiple seperated by ;)
POST_TEXT=keyboard                                # keyword to look for in post selftext (supports multiple seperated by ;)
```
