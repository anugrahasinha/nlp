import os
import sys
import logging
import traceback
from datetime import datetime
# project specific imports #
from lib import ChatBotConfigParser
from lib import ChatBotLogging
from lib import ChatBotLib
from nlu import NluModel
from core import RasaCoreTrain
from core import RunChatBotLocal
from core import RasaTrainOnline
from slack import RasaSlackApp

logger = logging.getLogger("ChatBotBase.Main")

# We need some warning avoidance here, lots of warnings coming from rasa APIs #
import warnings
warnings.filterwarnings("ignore")

def printStdOutMessage(message):
    """
    Function responsible for printing out STDOUT message when starting CLI program
    
    Arg: message -> "Message required to be printed"
    Return : <None>
    """
    try:
        base_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + " : ChatBot : Message : "
        print(base_str + message)
    except Exception as e:
        raise(e)

def __setupDefaultLocations():
    try:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        return True
    except Exception as e:
        logger.error("Unable to set chatbot library location, exception : %s" %(str(e)))        
        raise(e)

def parseArguments():
    try:
        return ChatBotLib().parseCLIArguments()
    except Exception as e:
        logger.error("Exception in parsing arguments, exception : %s" %(str(e)))
        raise(e)

def execute(userOption):
    try:
        # "train-rasa-nlu","train-rasa-core","run-train-rasa-core-online","run-chatbot-local","run-slack-chatbot" #
        if userOption == "train-rasa-nlu":
            nlu_model_obj = NluModel()
            return(nlu_model_obj.train_nlu())
        elif userOption == "train-rasa-core":
            rasa_core_train_obj = RasaCoreTrain()
            return(rasa_core_train_obj.trainRasaCore())
        elif userOption == "run-train-rasa-core-online":
            rasa_train_online_obj = RasaTrainOnline()
            agent,message = rasa_train_online_obj.runRasaTrainOnline()
            return message
        elif userOption == "run-chatbot-local":
            run_chat_bot_local_obj = RunChatBotLocal()
            agent,message = run_chat_bot_local_obj.run_chat_bot()
            return message
        elif userOption == "run-slack-chatbot":
            rasa_slack_app_obj = RasaSlackApp()
            rasa_slack_app_obj.run_app()
            return "Slack app execution now finished"
        else:
            # Not really possible as we have argparse working to check all of this, however for sanity #
            raise(Exception("Unknown option sent by user %s" %(userOption)))
    except Exception as e:
        logger.error("execution failed, exception : %s" %(str(e)))
        raise(e)

    
if __name__ == "__main__":
    try:
        __setupDefaultLocations()
        printStdOutMessage(str(execute(parseArguments())))
        sys.exit(0)
    except Exception as e:
        logger.error("Exception:\n%s" %(str("\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ]))))
        printStdOutMessage("Unable to start program, exception : %s" %(str(e)))
        printStdOutMessage("For details, please check log file")
        sys.exit(127)