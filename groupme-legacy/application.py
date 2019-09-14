#!/usr/bin/python3
import requests
import json
import sys
from flask import Flask, request

app = Flask(__name__)
settings = {}

# get_bot_id returns the mapping of a bot id from a group id
def get_bot_id(group_id):
	for m in settings["mappings"]:
		if m["group_id"] == group_id:
			return m["bot_id"]
	print("idk man")

# send_groupme sends a message to GroupMe
def send_groupme(group, message):
	requests.post(
		'https://api.groupme.com/v3/bots/post', 
		params = {
			"text": message,
			"bot_id": group
		}
	)

# receive_groupme listens for messages from GroupMe
@app.route('/groupme', methods=['POST'])
def receive_groupme():

    # Get messages made by humans
	message = request.get_json()	
	if message['sender_type'] == 'bot':
		return 'ok'

	# Send the automatic message thing
	global settings
	bot_id = get_bot_id(message["group_id"])
	send_groupme(bot_id, settings["message"])
	return 'ok'

if __name__ == '__main__':
	settings = json.load(open(sys.argv[1]))
	app.run(settings["flask"]["ip_address"], settings["flask"]["port"])