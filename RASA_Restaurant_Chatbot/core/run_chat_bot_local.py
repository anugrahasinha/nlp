from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
from datetime import datetime
import ast

from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer, BinarySingleStateFeaturizer)

from lib import ChatBotConfigParser
from lib import ChatBotLogging

logger = logging.getLogger("ChatBotBase.RunChatBotLocal")

class RunChatBotLocal(object):
	def __init__(self):
		try:
			self.config = ChatBotConfigParser().parser
		except Exception as e:
			logger.error("Unable to build RunChatBotLocal Obj, exception : %s" %(str(e)))
			raise(e)
	
	def run_chat_bot(self):
		try:
			nlu_model = os.path.realpath(self.config.get('nluModel','model_location'))
			core_model = os.path.realpath(self.config.get('coreModel','model_location'))
			interpreter = RasaNLUInterpreter(nlu_model)
			agent = Agent.load(core_model, interpreter = interpreter)
			
			if ast.literal_eval(self.config.get('runChatBotLocal','serve_forever')):
				agent.handle_channel(ConsoleInputChannel())
				
			return agent,"Rasa Chatbot local execution completed"
		except Exception as e:
			logger.error("Unable to execute chatbot, exception : %s" %(str(e)))
			raise(e)
