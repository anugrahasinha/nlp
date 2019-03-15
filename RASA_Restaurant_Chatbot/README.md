#### Type    : Rasa Chat Bot
#### Author  : Anugraha Sinha
#### Email   : anugraha.sinha[at]gmail[dot]com

#### IMPORTANT NOTE ####
    Slack bot integration is working properly, with this code.
    However, there was problem which is similar to https://github.com/RasaHQ/rasa_core/issues/471
    And therefore, the chat bot integration details are limited in this README file.
    For checking this, please provide appropriate Slack OAuth keys in etc/config.ini file and run
    python chatBotMain.py run-slack-chatbot (Please see details below)
    
#### Models already present #####
    Multiple models were created for rasa-core and rasa-nlu. They are present in models/ directory
    for reference. However, the best models which are mentioned in etc/config.ini are as follows
    1. Rasa - NLU  = models\ourgroup\nlu\model_20181028T231348\default\restaurantnlu
    2. Rasa - Core = models\ourgroup\dialogue\model_20181029T023515
    
    The above models work as the default models for chatbot to run under local execution format
    until, a re-learning is fired. Please check below for detailed explanation.
    
#### Preface:
    This case study submission brings forth following important enhancement over existing framework
    shared for restaurant search
    1. Flexibility to choose budget
    2. Sending details over mail
    3. Responding to complex inquiries and intents.

#### Directory Structure:
    \_
    \_\_chatBotMain.py     # Main execution file, please see details below #
    \_\_core               # Code specific to rasa core training 
    \_\_data               # base data.json, restaurant_domain.yml, stories.md files
    \_\_etc                # config file for running the whole system
    \_\_lib                # custom library code for logging, config reader etc.
    \_\_models             # learnt models (nlu and dialogues)
    \_\_nlu                # code specific to nlu used in the whole system
    \_\_slack              # code specific to slack integration
    
    
#### Usage:
    Please make sure that all requirements mentioned in the requirements file are satisfied.
    The based folder (where this readme file is present) consists of the mail file "chatBotMain.py"
    The code has been made compatible with Python 3.6+ version. The main file will provide a usage help
    itself, if required options are not presented.
    
    <Self help>
    [user@localhost code]~ python chatBotMain.py --help
    usage: chatBotMain.py [-h]
                          {train-rasa-nlu,train-rasa-core,run-train-rasa-core-online,run-chatbot-local,run-slack-chatbot}

    positional arguments:
    Options               {train-rasa-nlu,train-rasa-core,run-train-rasa-core-online,run-chatbot-local,run-slack-chatbot}
    
    optional arguments:
    -h, --help            show this help message and exit
    
    User can choose from the list of options provided above.
    
    1. For using pre-learned models provided by our group
    [user@localhost code]~ python chatBotMain.py run-chatbot-local
    
    This will pick up required NLU and RASA Core models, and provide an interactive chatbot interface.
    
    2. For building customized models in your own location (NLU Model)
    [user@localhost code]~ python chatBotMain.py train-rasa-nlu
    
#### NOTE
    If you run this, a new model would be trained and etc/config.ini would be automatically updated as per directory location of your system.
    
    3. For building customer model in your own location (RASA CORE model)
    [user@localhost code]~ python chatBotMain.py train-rasa-core
    
    # PLEASE NOTE ##
    If you run this, a new model would be trained and etc/config.ini would be automatically updated as per directory location of your system.
    
    4. For running online training for rasa core
    [user@localhost code]~ python chatBotMain.py run-train-rasa-core-online
    
    This would use the existing data/stories.md file and the NLU specific files present in data/ directory and provide an interactive
    interface train rasa core.
    please make that at the end, when you wish to dump the new training data (stories.md) file, specify the location as
    data/stories.md
    This will update the existing stories.md file with new training data.
    
    5. Running slack bot
    [user@localhost code]~ vim data/config.ini
    Update the slack OAuth information present in OAuth information section
    
    [user@localhost code]~ python chatBotMain.py run-slack-chatbot
    This will start the slack chat bot at
    
    PORT 5004
    
#### NOTE
    You will have to start the ngrok extension separately for forwarding port 5004 to public IP.
    Post that the new public URL needs to entered in SLACK APP configuration page also.
    
    
#### IMPORTANT NOTE
    Slack bot integration is working properly, with this code.
    However, we encountered the problem mentioned in https://github.com/RasaHQ/rasa_core/issues/471
    And therefore, chat bot integration video and details are limited in this README file.
    
    
#### Example for local chat bot execution
    [anugraha@localhost ~] python3 chatBotMain.py run-chatbot-local
    Using TensorFlow backend.
    2018-10-28_22:20:47 : ChatBot : Message : Log File = C:\Users\anugraha.sinha\Documents\MobaXterm\slash\tmp\ChatBot.log
    Bot loaded. Type a message and press enter:
    hi
    hey there! How may i help you
    find me a mexican restaurant in bangalore in the range of 300-700 and send details to anugraha.sinha@gmail.com
    -----
    Here are the top  results around bangalore for mexican from Foodie:
    1. Onesta
      in Rooftop, 90/3, Opposite Innovative Multiplex, Beside World of Titan, Outer Ring Road, Marathahalli, Bangalore
     Avg Budget for Two People is 600
      User Rating : 4.7
    2. Serranos Mexican Grill
      in Ground Floor, MFAR, Manyata Tech Park, Phase 4, Nagawara, Bangalore
     Avg Budget for Two People is 400
      User Rating : 3.6
    3. New York Burrito
      in Shop 5, First floor, OMBR Layout, Banaswadi, Bangalore
     Avg Budget for Two People is 400
      User Rating : 3.1
    4. Burrito Boys
      in RMZ Ecoworld, Bellandur, Bangalore
     Avg Budget for Two People is 330
      User Rating : 3.1
    5. Burrito Boys
      in Lower Ground Floor, Food Court, Pritech Park SEZ,  Outer Ring Road, Bellandur, Bangalore
     Avg Budget for Two People is 330
      User Rating : 2.9
    Should I mail you all the details
    yes
    -----
    Email has been sent successfully
    Okay!Bon Appetit!!
