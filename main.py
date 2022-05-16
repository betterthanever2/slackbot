import os
import json
import random
from requests_html import HTMLSession
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
# SLACK_BOT_TOKEN = 'xoxb-2151429001-2484817093683-ilklrYTN3z0kLiAvw1sEh9D5'
# SLACK_APP_TOKEN = 'xapp-1-A02ED9EJGEM-2558938697104-bd8035132157799230fafde32f49cfbc061ef702f4a4a896e2550e24f987ee3b'
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

@app.event("member_joined_channel")
def listen_new(ack, event, client):
    ack()
    print(event)
    if event["channel"] == "C01HFNTSRTJ": # Update
        with open('letters/new_member.json', 'r') as f:
            payload = json.load(f)
        client.views_open(view=payload, user_id=event["user"])

@app.view("view_1")
def handle_submission(ack, body, client, view, logger):
    user = body["user"]["id"]
    superviser_id = "U017RQD58G0" # send info
    # general_id = "C024FCM07"
    general_id = "C024FCM09" # this is random

    errors = {}

    description = view["state"]["values"]["input1"]
    if description is not None and len(description) <= 25:
        errors["input1"] = "Please, write a little more"

    q1 = view["state"]["values"]["input2"]
    if q1 is not None and len(q1) <= 25:
        errors["input2"] = "Please, write a little more"

    q2 = view["state"]["values"]["input3"]
    if q2 is not None and len(q2) <= 25:
        errors["input3"] = "Please, write a little more"

    q3 = view["state"]["values"]["input4"]
    if q3 is not None and len(q3) <= 25:
        errors["input4"] = "Come on already!"

    if errors:
        ack(response_action="errors", errors=errors)
        return

    ack()

    general_blocks = [{
        "type": "section",
        "text": {"type": "plain_text", "text": description},
    }]
    super_blocks = [
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

    client.chat_postMessage(channel=superviser_id, blocks = super_blocks, user=superviser_id, text=f"User {user['name']}'s answers")
    client.chat_postMessage(channel=general_id, blocks= general_blocks, text=f"Please, welcome the newest addition to the engineering team: {user['name']}! "
                                                                                                 f"Here's what they have to say about themselves:")

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