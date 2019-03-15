# base import #
import os
from datetime import datetime
import logging
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
from rasa_nlu import config
from rasa_nlu.components import ComponentBuilder

#builder = ComponentBuilder(use_cache=True)
from lib import ChatBotConfigParser
from lib import ChatBotLogging

logger = logging.getLogger("ChatBotBase.NluModel")

class NluModel(object):
	def __init__(self):
		try:
			self.builder = ComponentBuilder(use_cache=True)
			self.config = ChatBotConfigParser().parser
		except Exception as e:
			logger.error("Unable to build NluModel Obj, exception : %s" %(str(e)))
			raise(e)

	def train_nlu(self):
		try:
			nlu_data_json = "./" + self.config.get('inputData','nluData')
			nlu_spacy_json = "./" + self.config.get('inputData','spacyConfig')
			logger.info("Building NLU model with data_json : %s, spacy_json : %s" %(nlu_data_json,nlu_spacy_json))
			training_data = load_data(nlu_data_json)
			trainer = Trainer(config.load(nlu_spacy_json), self.builder)
			trainer.train(training_data)
			model_name = "model_" + datetime.now().strftime("%Y%m%dT%H%M%S")
			model_location = "./models/ourgroup/nlu/" + model_name
			model_directory = trainer.persist(model_location, fixed_model_name = 'restaurantnlu')
			model_directory = os.path.realpath(model_directory)
			logger.info("NLU model_directory returned : %s" %(str(model_directory)))
			#return ("NLU model training completed, see details above")
			self.config.set('nluModel','model_location',value=model_directory)
			with open("./etc/config.ini","w+") as f:
				self.config.write(f)
			return ("NLU model training completed, see details above")
		except Exception as e:
			logger.error("Unable to build NLU model, exception : %s" %(str(e)))
			raise(e)