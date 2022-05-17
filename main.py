import os
import json
import random
from pathlib import Path
from requests_html import HTMLSession
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
giphy_rating = ['g', 'pg', 'pg-13', 'r']
giphy_url = 'https://api.giphy.com/v1/gifs/random'
# giphy_payload = {'tag': 'cat', 'rating': giphy_rating[random.randint(0, 3)], 'api_key': os.environ.get('GIPHY_API_KEY')}
giphy_payload = {'tag': 'cat', 'rating': giphy_rating[random.randint(0, 3)], 'api_key': '3kXXQ0wQ7k3QhgKfW8IRfi1EpN1qec89'}


app = App(token=SLACK_BOT_TOKEN)

@app.event("app_home_opened")
def show_home(ack, event, client):
    ack()
    with open('letters/hometab.json', 'r') as f:
        payload = json.load(f)
    client.views_publish(view=payload, user_id=event['user'])

@app.shortcut("tech_onboarding")
def listen_new(ack, shortcut, client):
    ack()
    with open('letters/new_member.json', 'r') as f:
        payload = json.load(f)
    client.views_open(trigger_id=shortcut["trigger_id"], view=payload, user_id=shortcut["user"])

@app.view("new_member_modal")
def handle_submission(ack, body, client, view, logger):
    ack()
    user_id = body["user"]["id"]
    superviser_id = "U017RQD58G0" # send info -- Update
    general_id = "C024FCM07"
    # general_id = "C01HFNTSRTJ" # this is virtual_coffee

    errors = {}
    description = view["state"]["values"]["input1"]["plain_text_input-action"]["value"]
    if description is not None and len(description) <= 5:
        errors["input1"] = "Please, write a little more"

    q1 = view["state"]["values"]["input2"]["plain_text_input-action"]["value"]
    if q1 is not None and len(q1) <= 5:
        errors["input2"] = "Please, write a little more"

    q2 = view["state"]["values"]["input3"]["plain_text_input-action"]["value"]
    if q2 is not None and len(q2) <= 5:
        errors["input3"] = "Please, write a little more"

    q3 = view["state"]["values"]["input4"]["plain_text_input-action"]["value"]
    if q3 is not None and len(q3) <= 5:
        errors["input4"] = "Come on already!"

    if errors:
        ack(response_action="errors", errors=errors)
        return

    ack()

    general_blocks = [
        {
            "type": "section",
            "text": {"type": "plain_text", "text": f"Please, welcome the newest addition to the engineering team: {body['user']['name']}! Here's what they have to say about themselves:"},
        },
        {
            "type": "section",
            "text": {"type": "plain_text", "text": description},
        }
    ]
    super_blocks = [
        {
            "type": "section",
            "text": {"type": "plain_text", "text": f"User {body['user']['name']}'s answers"},
        },
        {
            "type": "section",
            "text": {"type": "plain_text", "text": description},
        },
        {
            "type": "section",
            "text": {"type": "plain_text", "text": q1},
        },
        {
            "type": "section",
            "text": {"type": "plain_text", "text": q2},
        },
        {
            "type": "section",
            "text": {"type": "plain_text", "text": q3},
        },
    ]

    client.chat_postMessage(channel=superviser_id, blocks = super_blocks, user=superviser_id, text = f"User {body['user']['name']}'s answers")
    client.chat_postMessage(channel=general_id, blocks= general_blocks, text = f"Please, welcome the newest addition to the engineering team: "
                                                                               f"{body['user']['name']}! Here's what they have to say about themselves:")

@app.command("/docs")
@app.event("app_mention")
def send_links(ack, command, client):
    ack()
    if command['text'] == 'help':
        with open('letters/aboutdocs.json', 'r') as f:
            payload = json.load(f)
    else:
        with open('letters/maindocs.json', 'r') as f:
            payload = json.load(f)

    if command['channel_name'] == 'directmessage':
        client.chat_postEphemeral(channel=command['user_id'], blocks=payload['blocks'], user=command['user_id'])
    else:
        client.chat_postEphemeral(channel=command['channel_id'], blocks=payload['blocks'], user=command['user_id'])

@app.command("/aboutsalescomps")
def send_salescomps_links(ack, command, client):
    ack()
    with open('letters/salescomps.json', 'r') as f:
        payload = json.load(f)
    if command['channel_name'] == 'directmessage':
        client.chat_postEphemeral(channel=command['user_id'], blocks=payload['blocks'], user=command['user_id'])
    else:
        client.chat_postEphemeral(channel=command['channel_id'], blocks=payload['blocks'], user=command['user_id'])

@app.command("/aboutmufa")
def send_multifamily_links(ack, command, client):
    ack()
    with open('letters/multifamily.json', 'r') as f:
        payload = json.load(f)
    if command['channel_name'] == 'directmessage':
        client.chat_postEphemeral(channel=command['user_id'], blocks=payload['blocks'], user=command['user_id'])
    else:
        client.chat_postEphemeral(channel=command['channel_id'], blocks=payload['blocks'], user=command['user_id'])

@app.command("/watchacat")
def send_cat_gif(ack, command, client):
    ack()
    session = HTMLSession()
    r = session.get(giphy_url, params=giphy_payload)
    rj = r.json()
    blocks = [{"type": "image",	"image_url": rj["data"]["image_url"], "alt_text": "cat"}]

    if command['channel_name'] == 'directmessage':
        client.chat_postMessage(channel=command['user_id'], blocks=blocks, user=command['user_id'])
    else:
        client.chat_postMessage(channel=command['channel_id'], blocks=blocks, user=command['user_id'])


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()