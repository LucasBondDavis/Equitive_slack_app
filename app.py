import os
import re
from typing import Callable

from slack_sdk import WebClient
from slack_bolt import App, Say, BoltContext

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

@app.message(re.compile("hi[!.]*", re.IGNORECASE))
def test_message(message, say: Say):
  user_id = message['user']
  say(f'Salutations <@{user_id}> :wave:')

# def post_button_message(respond):
@app.message(re.compile('.*interview guide.*'))
def give_link(say: Say):
  # https://drive.google.com/file/d/1G-J-CbErzt1mEQFJE99n9L8TAUYhEs5s/view?usp=sharing
  say(blocks=[
    {
      "type": "section",
      "block_id": "a",
      "text": {
        "type": "mrkdwn",
        "text": "Here's the interview guide: https://drive.google.com/file/d/1G-J-CbErzt1mEQFJE99n9L8TAUYhEs5s/view?usp=sharing",
      }
    }])

# @app.message(re.compile('.*share.*team'))
# def share_to_team(say: Say, client: WebClient):
#   say("sharing with team!")

def extract_subtype(body: dict, context: BoltContext, next: Callable):
    context["subtype"] = body.get("event", {}).get("subtype", None)
    next()

@app.event(event={"type": "message", "subtype": "file_share"})
def add_reaction(body: dict, client: WebClient, context: BoltContext, say: Say):
  message_ts = body["event"]["ts"]
  client.reactions_add(
      channel=context.channel_id,
      timestamp=message_ts,
      name="eyes",
  )
  say(blocks=[
    {
      "type": "section",
      "block_id": "blk",
      "text": {
        "type": "mrkdwn",
        "text": "Would you like to share this with the team?",
      },
      "accessory": {
        "type": "button",
        "action_id": "button_click",
        "text": {
          "type": "plain_text",
          "text": "yes",
        },
        "value": "yes"
      }
    },
  ])

@app.event("button_click")
def button_click(say: Say):
  say('Uploading')
  # TODO get team id
  # for user in team:
  #   client.chat_meMessage('file', 'channel_id')

@app.message("quiz")
def quiz(say: Say):
  say(blocks=[
    {
      "type": "section",
      "block_id": "blk",
      "text": {
        "type": "mrkdwn",
        "text": "Ready to start the quiz?",
      },
    },
    {
      "type": "section",
      "text": {"type": "plain_text", "text": " "},
      "accessory": {
        "type": "button",
        "text": {"type": "plain_text", "text": "Yes"},
        "action_id": "start_quiz",
      },
    },
    {
      "type": "section",
      "text": {"type": "plain_text", "text": " "},
      "accessory": {
        "type": "button",
        "text": {"type": "plain_text", "text": "No"},
        "action_id": "pass",
      },
    }
  ])

@app.event("start_quiz")
def quiz_start(say: Say):
  say("True or False. Did Grace Hopper coin the term 'debugging'?")
  # TODO add quiz content

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
