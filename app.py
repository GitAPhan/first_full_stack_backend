import dbinteractions as db
from flask import Flask, request, Response
import json
import sys

app = Flask(__name__)

@app.get('/candy')
def get_candy():
    candys = db.get_candy_db()

    candys_json = json.dumps(candys, default=str)

    return Response(candys_json, mimetype="application/json", status=200)

# testing/production mode code
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