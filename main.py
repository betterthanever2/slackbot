import os
import json
import random
from requests_html import HTMLSession
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# app_token = os.environ.get('SLACK_APP_TOKEN')
# bot_token = os.environ.get('SLACK_BOT_TOKEN')
app_token = 'xapp-1-A02ED9EJGEM-2522178962054-9df29c691ab1995e4e80770308515cda1054c3b4e82d83008f23507a47e7c6e0'
bot_token = 'xoxb-2151429001-2484817093683-do0BorQoLjiQxwSROs1nJAib'
giphy_rating = ['g', 'pg', 'pg-13', 'r']
giphy_url = 'https://api.giphy.com/v1/gifs/random'
giphy_payload = {'tag': 'cat', 'rating': giphy_rating[random.randint(0, 3)], 'api_key': '3kXXQ0wQ7k3QhgKfW8IRfi1EpN1qec89'}


app = App(token=bot_token)
# payload = [
#     {
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "Hello dear reader! Once upon a time we didn't have this page, and we were miserable. It nearly got to the point of utmost despair, but then this page got compiled and everybody relaxed a little bit."
# 			}
# 		},
# 	{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "We, at the _CompStak Tech Writing Deparment_, hope that you're having a good day. Now, without any further ado, here are your links:"
# 			}
# 		},
# 	{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "1. *<https://compstak.atlassian.net/wiki/spaces/TECH/pages/2096398337/Documentation+Protocol|Documentation Protocol>* is really, really important, you should check it out."
# 			}
# 		},
# 	{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "2. *<https://compstak.atlassian.net/wiki/spaces/ONB/pages/1349419128/Guide+to+CompStak+Confluence|Guide to CompStak Confluence>*."
# 			}
# 		},
# 	{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "3. Our folder with *<https://drive.google.com/drive/u/2/folders/1VV1k9y5eo_rPP6RIuxmLoNnsTkie1sDl|Videos>* and the accompanying <https://docs.google.com/document/d/16YT_yCtajVJP9d4cLNgZ848YzbVlHxA-4pGMkF1G0A0/edit?usp=sharing|ReadMe File>."
# 			}
# 		},
# 	{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "4. *<https://compstak.atlassian.net/wiki/spaces/TECH/overview|TECH space>* in Confluence, just in case."
# 			}
# 		},
# 	{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "5. *<https://compstak.atlassian.net/browse/AP|All Tech Projects>* in Jira, also just in case."
# 			}
# }
# ]

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