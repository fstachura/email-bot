import logging
from datetime import datetime, timedelta
from json import load
from sys import argv, stdout
from imap_tools.mailbox import MailBoxTls, MailBox
from imap_tools.message import MailMessage
from imap_tools.query import A
from requests import post

logger = logging.getLogger("email-bot")
logging.basicConfig(stream=stdout, level=logging.INFO)

def format_msg(msg: MailMessage):
    subject = msg.subject if len(msg.subject.strip()) != 0 else "(empty)"
    return f"""
From: {msg.from_[:80]}
### {subject[:400]}
```
{msg.text[:1400]}
```
    """

def send_email_webhook(webhook_url: str, msg: MailMessage):
    r = post(webhook_url, json={
        "content": format_msg(msg),
    })
    if len(r.text) != 0:
        try:
            logger.info("subject %s, response from webhook: %s", msg.subject, r.json())
        except:
            logger.exception("failed to parse json response from webhook")
    return r.status_code == 204

def check_mail_and_send_webhooks(mailbox, destinations, default_destination):
    seen_uids = []
    yesterday = datetime.now() - timedelta(days=1)
    for msg in mailbox.fetch(criteria=A(seen=False, date_gte=yesterday.date()), mark_seen=False):
        found = False

        for d in destinations.keys(): 
            if d in msg.to:
                found = True
                logger.info("sending message to " + d)
                if send_email_webhook(destinations[d], msg):
                    seen_uids.append(msg.uid)
                else:
                    logger.error("failed to send webhook")

        if not found:
            logger.info("destination for " + str(msg.to) + " was not found, sending to default")
            if send_email_webhook(default_destination, msg):
                seen_uids.append(msg.uid)

    logger.debug("updating seen flags")
    mailbox.flag(seen_uids, "\\Seen", True)

def idle(mailbox, callback):
    while True:
        logger.debug("idling")
        responses = mailbox.idle.wait(timeout=60*5)
        if responses:
            logger.debug("idle returned responses")
            callback() 

if __name__ == "__main__":
    if len(argv) == 1:
        print("usage: python3", argv[0], "config.json")
        exit(0)

    with open(argv[1]) as config_file:
        config = load(config_file)

    m = config["mailbox"]
    starttls = False if "starttls" not in config else config["starttls"]
    MailboxClass = MailBoxTls if starttls else MailBox

    with MailboxClass(m["server"], port=m["port"]).login(m["login"], m["password"]) as mailbox:
        logger.info("logged in")
        idle(mailbox, lambda: check_mail_and_send_webhooks(mailbox,
                                                           config["destinations"],
                                                           config["default_destination"]))

