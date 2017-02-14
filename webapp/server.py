from flask import Flask
from flask import request
from flask import jsonify

from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.pipeline import make_pipeline, Pipeline
from nltk import word_tokenize

app = Flask(__name__)
g_model_filename='../models/party_classifier.pkl'
g_estimator = joblib.load(g_model_filename)

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
        return g_estimator.predict_proba(json_dict['text'])
    except ValueError:
        raise InvalidUsage('Fit request has invalid format')

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
