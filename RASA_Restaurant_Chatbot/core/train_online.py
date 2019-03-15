from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
from datetime import datetime

from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter

from lib import ChatBotConfigParser
from lib import ChatBotLogging

logger = logging.getLogger("ChatBotBase.RasaTrainOnline")

class RasaTrainOnline(object):
    def __init__(self):
        try:
            self.config = ChatBotConfigParser().parser
        except Exception as e:
            logger.error("Unable to build RasaTrainOnline Obj, exception : %s" %(str(e)))
            raise(e)
        
    def runRasaTrainOnline(self):
        try:
            input_channel = ConsoleInputChannel()
            interpreter = RasaNLUInterpreter(os.path.realpath(self.config.get('nluModel','model_location')))
            domain_file = os.path.realpath(self.config.get('inputData','coreyml'))
            training_data_file = os.path.realpath(self.config.get('inputData','stories'))
            logger.info("nluModel = %s, domain_file = %s, train_data_file = %s" %(str(os.path.realpath(self.config.get('nluModel','model_location'))),str(domain_file),str(training_data_file)))
            agent = Agent(domain_file,
                          policies=[MemoizationPolicy(), KerasPolicy()],
                          interpreter=interpreter)
        
            agent.train_online(training_data_file,
                               input_channel=input_channel,
                               max_history=2,
                               batch_size=50,
                               epochs=200,
                               max_training_samples=300)
        
            return agent,"Rasa Train Online completed successfully"
        except Exception as e:
            logger.error("Unable to run Rasa Train Online, exception : %s" %(str(e)))
            raise(e)


#if __name__ == '__main__':
#    logging.basicConfig(level="INFO")
#    modelname="model1"
#    modellocation = "C:\\Users\\anugraha.sinha\\OneDrive\\Documents\\Post Graduate ML & AI IIIT-Bangalore Upgrad\\Main Program\\3_NLP\\3_5_ChatBot_Rasa_Stack\\case_study_rest_chatbot\\models\\ourgroup\\nlu\\" + modelname + "\\default\\restaurantnlu"    
#    nlu_interpreter = RasaNLUInterpreter(modellocation)
#    run_restaurant_online(ConsoleInputChannel(), nlu_interpreter)
