from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import logging
import os
from datetime import datetime
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer, BinarySingleStateFeaturizer)

from lib import ChatBotConfigParser
from lib import ChatBotLogging

logger = logging.getLogger("ChatBotBase.RasaCoreTrain")

class RasaCoreTrain(object):
	def __init__(self):
		try:
			self.config = ChatBotConfigParser().parser
		except Exception as e:
			logger.error("Unable to build RasaCoreTrain Obj, exception : %s" %(str(e)))
			raise(e)
	
	def trainRasaCore(self):
		try:
			training_data_file = "./" + self.config.get('inputData','stories')
			domain_yml = "./" + self.config.get('inputData','coreyml')
			
			logger.info("Building RASA Core model with stories : %s, domain_yml : %s" %(training_data_file,domain_yml))
			model_name = "model_" + datetime.now().strftime("%Y%m%dT%H%M%S")
			model_location = "./models/ourgroup/dialogue/" + model_name
			
			
			featurizer = MaxHistoryTrackerFeaturizer(BinarySingleStateFeaturizer(), max_history=5)
			agent = Agent(domain_yml, policies = [MemoizationPolicy(max_history = 4), KerasPolicy(featurizer)])
			
			agent.train(training_data_file,
				    augmentation_factor = 50,
				    #max_history = 4,
				    epochs = 500,
				    batch_size = 30,
				    validation_split = 0.2)
			agent.persist(model_location)
			
			model_location = os.path.realpath(model_location)
			logger.info("RASA Core model_location : %s" %(str(model_location)))
			
			self.config.set('coreModel','model_location',value=model_location)
			with open("./etc/config.ini","w+") as f:
				self.config.write(f)
			return ("RASA core model training completed, see details above")
		except Exception as e:
			logger.error("unable to train rasa core model, exception : %s" %(str(e)))
			raise(e)