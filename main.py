import os
import json
import random
from requests_html import HTMLSession
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app_token = os.environ.get('SLACK_APP_TOKEN')
bot_token = os.environ.get('SLACK_BOT_TOKEN')
giphy_rating = ['g', 'pg', 'pg-13', 'r']
giphy_url = 'https://api.giphy.com/v1/gifs/random'
giphy_payload = {'tag': 'cat', 'rating': giphy_rating[random.randint(0, 3)], 'api_key': '3kXXQ0wQ7k3QhgKfW8IRfi1EpN1qec89'}


app = App(token=bot_token)

@app.command("/docs")
@app.event("app_mention")
def send_links(ack, command, client):
    ack()
    with open('letters/maindocs.json', 'r') as f:
        payload = json.load(f)

    if command['channel_name'] == 'directmessage':
        client.chat_postEphemeral(channel=command['user_id'], blocks=payload['blocks'], user=command['user_id'])
    else:
        client.chat_postEphemeral(channel=command['channel_id'], blocks=payload['blocks'], user=command['user_id'])

@app.command("/aboutdocs")
def send_info(ack, command, client):
    ack()
    with open('letters/aboutdocs.json', 'r') as f:
        payload = json.load(f)

@app.command("/aboutbottleneck")
def send_bottleneck_links(ack, command, client):
    ack()
    with open('letters/bottleneck.json', 'r') as f:
        payload = json.load(f)

@app.command("/aboutppm")
def send_ppm_links(ack, command, client):
    ack()
    with open('letters/ppm.json', 'r') as f:
        payload = json.load(f)

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

@app.command("/sharecat")
def send_silent_cat_gif(ack, command, client):
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
    SocketModeHandler(app, app_token).start()