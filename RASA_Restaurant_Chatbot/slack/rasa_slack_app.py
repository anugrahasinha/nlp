from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
import os
import logging

from lib import ChatBotConfigParser
from lib import ChatBotLogging
from .rasa_slack_connector import SlackInput

logger = logging.getLogger("ChatBotBase.RasaSlackApp")

class RasaSlackApp(object):
    def __init__(self):
        try:
            self.config = ChatBotConfigParser().parser
            self.nlu_interpretor = RasaNLUInterpreter(self.config.get('nluModel','model_location'))
            self.agent = Agent.load(self.config.get('coreModel','model_location'))
            self.input_channel = SlackInput(self.config.get('slack','app_verification'), # app verification token
                                            self.config.get('slack','bot_verification'), # bot verification token
                                            self.config.get('slack','slack_verification'), # slack verification token
                                            True)
        except Exception as e:
            logger.error("Unable to create object for RasaSlackApp, exception : %s" %(str(e)))
            raise(e)
        
    def run_app(self):
        try:
            self.agent.handle_channel(HttpInputChannel(5004,"/",self.input_channel))
        except Exception as e:
            logger.error("Unable to start slack app, exception : %s" %(str(e)))
            raise(e)


#nlu_interpreter = RasaNLUInterpreter('./models/ourgroup/nlu/model_20181027T202656/default/restaurantnlu')
#agent = Agent.load('./models/ourgroup/dialogue/model_20181027T202736', interpreter = nlu_interpreter)

#input_channel = SlackInput('xoxp-460834353523-461984426807-465152376016-227cf68b2f965e85773c3d8c3de2b90c', #app verification token
#							'xoxb-460834353523-467290740166-gSiOoS05TflKL19xb9dix609', # bot verification token
#							'048rGeNtBMmp2ipFkA7BAgiU', # slack verification token
#							True)

#agent.handle_channel(HttpInputChannel(5004, '/', input_channel))