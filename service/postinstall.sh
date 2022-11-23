#!/bin/sh
set -e

# Create discordredditposts group (if it doesn't exist)
if ! getent group discordredditposts >/dev/null; then
    groupadd --system discordredditposts
fi

# Create discordredditposts user (if it doesn't exist)
if ! getent passwd discordredditposts >/dev/null; then
    useradd                        \
        --system                   \
        --gid discordredditposts   \
        --shell /usr/sbin/nologin  \
        discordredditposts
fi

# Update config file permissions (idempotent)
chown root:discordredditposts /etc/discordredditposts.conf
chmod 0640 /etc/discordredditposts.conf

# Reload systemd to pickup discordredditposts service(s)
systemctl daemon-reload