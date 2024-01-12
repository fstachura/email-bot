# email-bot

Simple Discord webhook bot that sends messages on new emails 

## Setup

* `python3 -m venv .venv`
* `source .venv/bin/activate`
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
        "password": "",
        # optional - use starttls for imap connection. false if ommitted
        "starttls": false
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

## Usage notice

This software is licensed under the MIT license. As stated in the LICENSE file:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

A fair warning: If the bot posts something that breaks the Discord TOS, the creator of the webhook URL (user of the bot) is liable. This specifically means, that if something that breaks the Discord TOS is sent to an email address, and then forwarded to a Discord channel by an instance of this bot, the owner of the account that was used to create the webhook could be banned (or maybe even held liable in other ways, in very extreme cases). So it's important to be careful - I personally wouldn't connect this bot to a public, busy email address. Not to mention work accounts (or any other account that could receive sensitive/protected data). At the very least, please make sure that you have a good spam filter that bypasses the Inbox if a received email is classified as SPAM.
The author of this bot is not responsible for any damages caused by the bot.

