#!/usr/bin/python3
import slack
import requests
import sys
import json
from flask import Flask, request
from multiprocessing import Process

app = Flask(__name__)

# configure_slack sets up the web and rtm slack clients
def configure_slack(settings):
    
    # Configure the Slack clients
    global slack_token
    global slack_poster
    global slack_listner
    slack_token = settings["slack"]["token"]
    slack_poster = slack.WebClient(token=slack_token) 
    slack_listner = slack.RTMClient(token=slack_token)
    
    # Record channel<->group mappings
    global group_ids
    global channel_ids
    group_ids = {}
    channel_ids = {}
    for pair in settings["mappings"]:
        group_ids[pair["channel_id"]] = pair["bot_id"]
        channel_ids[pair["group_id"]] = pair["channel_id"]

# send_slack sends a message to Slack
def send_slack(channel, name, message, avatar='http://d3sq5bmi4w5uj1.cloudfront.net/images/brochure/og_image_poundie.png'):
	global slack_poster
	slack_poster.chat_postMessage(
		channel=channel,
		username=name,
		text=message,
		as_user=False,
		icon_url=avatar
	)

# send_slack_file sends a file to Slack
def send_slack_file(channel, name, file_url, comment):
    global slack_poster

    attachment = requests.get(file_url)
    file_name = file_url
    try:
        file_name = attachment.headers['content-disposition']
    except:
        pass

    if len(comment) == 0:
        comment = "[{}] shared a file".format(name)
    else:
        comment = "[{}] {}".format(name, comment)
    
    slack_poster.files_upload(
        channels=channel,
        filename=file_name,
        file=attachment.content,
        initial_comment=comment
    )

# send_groupme sends a message to GroupMe
def send_groupme(group, name, message):
	if name == "GroupMe Sync":
		return
	requests.post(
		'https://api.groupme.com/v3/bots/post', 
		params = {
			"text": "[{}] {}".format(name, message),
			"bot_id": group
		}
	)

# slack_name returs the nice name to a userid
def slack_name(userid):
	global slack_token
	response = requests.get(
		'https://slack.com/api/users.info',
		params = {
			"token": slack_token,
			"user": userid
		}
	).json()
	try:
		return response["user"]["real_name"]
	except:
		return "???"

# TODO -- use the events api instead of the rtm one
# receive_slack listens for messages from Slack
@slack.RTMClient.run_on(event='message')
def receive_slack(**payload):
	message = payload['data']
	global group_ids
	try:
		if len(message['files']) > 0:
			send_groupme(
				group_ids[message['channel']],
				slack_name(message['user']),
				"shared a file on slack"
			)
	except:
		pass
	if len(message['text']) == 0:
	    return
	try:
		send_groupme(
			group_ids[message['channel']],
			slack_name(message['user']), 
			message['text']
		)
	# Innelegant problems require innelegant solutions
	except:
		pass

# receive_groupme listens for messages from GroupMe
@app.route('/groupme', methods=['POST'])
def receive_groupme():
	message = request.get_json()
	if message['sender_type'] == 'bot':
		return 'ok'
	global channel_ids
	if len(message['attachments']) == 0:
		send_slack(
			channel_ids[message['group_id']],
			message['name'],
			message['text'],
			message['avatar_url']
		)
	else:
		for attachment in message['attachments']:
			if attachment['type'] == 'image':
				send_slack_file(
					channel=channel_ids[message['group_id']],
					name=message['name'],
					file_url=attachment['url'],
					comment=message['text']
			)
	return 'ok'

if __name__ == '__main__':
	# Read the settings from the file
	settings = json.load(open(sys.argv[1]))
	
	# Configure and run the Slack handler
	configure_slack(settings)
	Process(
		target=slack_listner.start
	).start()
	
	# Run the Flask server
	Process(
		target=app.run, 
		args=(
			settings["flask"]["ip_address"], 
			settings["flask"]["port"], 
			False
		)
	).start()
