from flask import Flask
from flask import request
from flask import jsonify

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

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/fit', methods=['POST'])
def fit():
    try:
        json_dict = request.get_json()
        return json_dict['text']
    except ValueError:
        raise InvalidUsage('Fit request has invalid format')

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
