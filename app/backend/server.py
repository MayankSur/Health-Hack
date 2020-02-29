from flask import Flask, request
import json
import sys
from flask import jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
# Allows for cross platform communication
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/greet')
def say_hello():
  return 'Hello from Server'

@app.route('/incoming_request', methods=['POST'])
def incoming_request():
    if request.method == 'POST':
        print(request.json, file=sys.stderr)
        # Here we print the data coming from the request
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        # Need to create a correct error message
        #error = 'Invalid username/password'
        return jsonify(success=False)
    