from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from builtins import str
from flask import Blueprint, request, jsonify

from rasa_core.channels.channel import UserMessage, OutputChannel
from rasa_core.channels.rest import HttpInputComponent

from lib import ChatBotConfigParser
from lib import ChatBotLogging

logger = logging.getLogger("ChatBotBase.RasaSlackConnector")

class SlackBot(OutputChannel):
	def __init__(self, slack_verification_token, channel):
		logger.info("slack_verification_token : %s" %(slack_verification_token))
		self.slack_verification_token = slack_verification_token
		logger.info("channel : %s" %(channel))
		self.channel = channel
		logger.info("SlackBot object creation completed")
		
	def send_text_message(self, recipient_id, message):
		from slackclient import SlackClient
		text = message
		recipient = recipient_id
		logger.info("text = %s, recipient = %s" %(text,recipient))
		CLIENT = SlackClient(self.slack_verification_token)
		CLIENT.api_call('chat.postMessage', channel = self.channel, text = text, as_user = True)
		logger.info("slack bot send text_message completed.")

class SlackInput(HttpInputComponent):
	def __init__(self, slack_dev_token, slack_verification_token, slack_client, debug_mode):
		self.slack_dev_token = slack_dev_token
		self.debug_mode = debug_mode
		self.slack_client = slack_client
		self.slack_verification_token = slack_verification_token
		
	def blueprint(self, on_new_message):
		from flask import Flask, request, Response
		slack_webhook = Blueprint('slack_webhook', __name__)
		
		@slack_webhook.route('/', methods = ['GET'])
		def health():
			logger.info("SlackInput : Got a root level GET query")
			return jsonify({'status':'ok'})
			
		@slack_webhook.route('/slack/events', methods = ['POST'])
		def event():
			if request.json.get('type') == 'url_verification':
				logger.info("SlackInput : Got a url_verification POST method call")
				return request.json.get('challenge'), 200
				
			if request.json.get('token') == self.slack_client and request.json.get('type') == 'event_callback':
				data = request.json
				messaging_events = data.get('event')
				channel = messaging_events.get('channel')
				user = messaging_events.get('user')
				text = messaging_events.get('text')
				bot = messaging_events.get('bot_id')
				logger.info("actual query from slack channel:\ndata=%s\messaging_event=%s\nchannel=%s\nuser=%s\ntext=%s\nbot=%s" %(str(data),str(messaging_events),str(channel),str(user),str(text),str(bot)))
				if bot == None:
					on_new_message(UserMessage(text, SlackBot(self.slack_verification_token, channel)))
				
			return Response(), 200
		return slack_webhook