# email-bot

Simple Discord webhook bot that sends messages on new emails 

## Setup

* `python3 -m venv .venv`
* `./.venv/bin/activate`
* `pip3 install -r requirements.txt`
* `python3 main.py config.json`

## Config

Config is stored in a JSON file. See `example-config.json` for a template.

```
{
    "mailbox": {
        # imap server hostname
        "server": "",
        # imap server port, assumes TLS
        "port": 143,
        "login": "email-bot",
        "password": ""
    },
    # posts messages to different webhooks based on email "to" field
    # note that this does not work for emails sent with "bcc"
    "destinations": {
        "rcpt1@example.com": "https://discord.com/api/webhooks/id/token",
        "rcpt2@example.com": "https://discord.com/api/webhooks/id2/token2"
    },
    # default webhook if none of the destinations match
    "default_destination": "https://discord.com/api/webhooks/id3/token3"
}
```
