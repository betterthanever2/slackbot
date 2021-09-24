import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# app_token = os.environ.get('SLACK_APP_TOKEN')
app_token = 'xapp-1-A02ED9EJGEM-2521907480230-4cac6d00bd60649e815737c7393f4c2ce5cdee3de1bc58c4aa301837c9c7ccec'
# bot_token = os.environ.get('SLACK_BOT_TOKEN')
bot_token = 'xoxb-2151429001-2484817093683-DLJUYA9lgXBpY5tFp0tS4UpB'

app = App(token=bot_token)
payload = [
    {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hello dear reader! Once upon a time we didn't have this page, and we were miserable. It nearly got to the point of utmost despair, but then this page got compiled and everybody relaxed a little bit."
			}
		},
	{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "We, at the _CompStak Tech Writing Deparment_, hope that you're having a good day. Now, without any further ado, here are your links:"
			}
		},
	{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "1. *<https://compstak.atlassian.net/wiki/spaces/TECH/pages/2096398337/Documentation+Protocol|Documentation Protocol>* is really, really important, you should check it out."
			}
		},
	{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "2. *<https://compstak.atlassian.net/wiki/spaces/ONB/pages/1349419128/Guide+to+CompStak+Confluence|Guide to CompStak Confluence>*."
			}
		},
	{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "3. Our folder with *<https://drive.google.com/drive/u/2/folders/1VV1k9y5eo_rPP6RIuxmLoNnsTkie1sDl|Videos>* and the accompanying <https://docs.google.com/document/d/16YT_yCtajVJP9d4cLNgZ848YzbVlHxA-4pGMkF1G0A0/edit?usp=sharing|ReadMe File>."
			}
		},
	{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "4. *<https://compstak.atlassian.net/wiki/spaces/TECH/overview|TECH space>* in Confluence, just in case."
			}
		},
	{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "5. *<https://compstak.atlassian.net/browse/AP|All Tech Projects>* in Jira, also just in case."
			}
}
]

@app.command("/docs")
@app.event("app_mention")
def send_links(ack, command, client):
    ack()
    if command['channel_name'] == 'directmessage':
        client.chat_postEphemeral(channel=command['user_id'], blocks=payload, user=command['user_id'])
    else:
        client.chat_postEphemeral(channel=command['channel_id'], blocks=payload, user=command['user_id'])

if __name__ == "__main__":
    SocketModeHandler(app, app_token).start()