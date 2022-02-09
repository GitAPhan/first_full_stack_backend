import dbinteractions as db
from flask import Flask, request, Response
import json
import sys

app = Flask(__name__)



if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    print("You must pass a mode to run this python script. Either 'testing' or 'production'")
    exit() 

if mode == 'testing':
    from flask_cors import CORS
    CORS(app)
    print("running in testing mode")
    app.run(debug=True)
else:
    print("Invalid mode: Please run using either 'testing' or 'production'")
    exit()