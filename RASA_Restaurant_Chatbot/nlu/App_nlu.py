from flask import session,flash
import pandas as pd
import numpy as np 
from flask import Response
import os 
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
import tempfile
import simplejson as j
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
import json

app = Flask(__name__)

#modelname="model1"
#modellocation = "C:\\Users\\anugraha.sinha\\OneDrive\\Documents\\Post Graduate ML & AI IIIT-Bangalore Upgrad\\Main Program\\3_NLP\\3_5_ChatBot_Rasa_Stack\\case_study_rest_chatbot\\models\\ourgroup\\nlu\\" + modelname + "\\default\\restaurantnlu"
modellocation="./models/ourgroup/nlu/model_20181026T005019/default/restaurantnlu"
 

@app.route('/')
def index():
    return render_template('index.html')
    
interpreter = Interpreter.load(modellocation)
print("Model Directory = %s" %(str(interpreter.model_metadata.model_dir)))
@app.route('/nlu_parsing', methods=['POST'])
def transform():
    print("In Transfort, point 1")
    if request.headers['Content-Type'] == 'application/json':     
        print("In transform, point 2")
        query = request.json.get("utterance")
        print("showing query here : %s" %(str(query)))
        results=interpreter.parse(query)
        js = json.dumps(results)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

        
if __name__ == '__main__':
    app.run(debug=True)
