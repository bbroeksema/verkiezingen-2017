from flask import Flask
from flask import request
from flask import jsonify

import dill
import json
import pickle
import sys

sys.path.append('../')
from src.models import *

app = Flask(__name__)
g_estimator = PartyClassifier()
g_estimator = pickle.load(open( '../models/PartyClassifier.pkl', "rb" ))

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.route('/')
def index():
    return 'Index Page'

@app.route('/fit', methods=['POST'])
def fit():
    """
    Accepts messages with a json post body that looks like:

    { "text": "veiligheid immigratie islam terrorisme"}
    """
    try:
        json_dict = request.get_json()
    except ValueError:
        raise InvalidUsage('Fit request has invalid format')

    probas = g_estimator.predict_proba([json_dict['text']]).tolist()[0]
    return json.dumps(dict(zip(g_estimator.y_labels, probas)))

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
