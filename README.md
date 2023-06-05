# discord-reddit-posts

send new posts from reddit via title, text, or domain

powered (optionally) by github's generosity

## usage

```env
SUBREDDIT=hardwareswap                            # subreddit to watch
WEBHOOK_URL=https://discord.com/api/webhooks/xxx  # discord webhook url (supports multiple seperated by ;)
PUSHOVER_APP=XXX...YYY                            # pushover token for an application
PUSHOVER_USER=ZZZ                                 # pushover user id
POST_DOMAIN=cnn.com                               # domain of a link posted (supports multiple seperated by ;)
POST_TITLE=keyboard                               # keyword to look for in post title (supports multiple seperated by ;)
POST_TEXT=keyboard                                # keyword to look for in post selftext (supports multiple seperated by ;)
LOOP_SECONDS=60                                   # seconds between searching for new posts
```
