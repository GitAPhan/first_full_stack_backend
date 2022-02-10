import dbinteractions as db
from flask import Flask, request, Response
import json
import sys

app = Flask(__name__)

# clients can read candy posts
@app.get("/candy")
def get_candy():
    candys = db.get_candy_db()
    candys_json = json.dumps(candys, default=str)
    return Response(candys_json, mimetype="application/json", status=200)


# clients can create candy posts
@app.post("/candy")
def post_candy():
    # key error status message
    key_error_message = "KeyError: 'name'"

    try:
        # user input
        name = request.json["name"]
        key_error_message = "KeyError: 'description'"
        description = request.json["description"]
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=400)

    # request from database
    post_status_message, post_status_code = db.post_candy_db(name, description)

    return Response(post_status_message, mimetype="plain/text", status=post_status_code)


# clients can edit candy posts
@app.patch("/candy")
def patch_candy():
    # key error status message
    key_error_message = "KeyError: 'id'"

    try:
        # user input
        id = int(request.json["id"])
        key_error_message = "KeyError: 'name'"
        name = request.json["name"]
        key_error_message = "KeyError: 'description'"
        description = request.json["description"]
        key_error_message = "KeyError: 'loginToken'"
        login_token = request.json["loginToken"]
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=400)
    except ValueError:
        return Response(
            "Input Error: incorrect keyvalue entered for 'id'",
            mimetype="plain/text",
            status=400,
        )
    except:
        return Response(
            "Generic patch request error", mimetype="plain/text", status=400
        )

    # request from database
    patch_status_message, patch_status_code = db.patch_candy_db(id, name, description, login_token)

    return Response(
        patch_status_message, mimetype="plain/text", status=patch_status_code
    )


# clients can delete candy posts
@app.delete("/candy")
def delete_candy():
    # key error status message
    key_error_message = "KeyError: 'id'"

    try:
        # user input
        id = request.json["id"]
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=400)
    except ValueError:
        return Response(
            "Input Error: incorrect keyvalue entered for 'id'",
            mimetype="plain/text",
            status=400,
        )
    except:
        return Response(
            "Generic patch request error", mimetype="plain/text", status=400
        )

    # request from database
    delete_status_message, delete_status_code = db.delete_candy_db(id)

    return Response(
        delete_status_message, mimetype="plain/text", status=delete_status_code
    )


# login check
@app.post("/user")
def login_attempt():
    # key error status message
    key_error_message = "KeyError: 'username'"

    try:
        # user input
        username = request.json["username"]
        key_error_message = "KeyError: 'password'"
        password = request.json["password"]
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=400)
    except:
        return Response(
            "Generic login request error", mimetype="plain/text", status=400
        )

    # request from database
    login_status_message, login_status_code = db.login_attempt_db(username, password)

    # convert to JSON
    login_status_message_json = json.dumps(login_status_message, default=str)

    return Response(
        login_status_message_json, mimetype="application/json", status=login_status_code
    )


@app.delete("/user")
def logout_attempt():
    # key error status message
    key_error_message = "KeyError: 'loginToken'"

    try:
        # user input
        login_token = request.json["loginToken"]
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=400)
    except:
        return Response(
            "Generic logout request error", mimetype="plain/text", status=400
        )

    # request from database
    logout_status_message, logout_status_code = db.logout_attempt_db(login_token)

    return Response(
        logout_status_message, mimetype="plain/text", status=logout_status_code
    )


# testing/production mode code
if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    print(
        "You must pass a mode to run this python script. Either 'testing' or 'production'"
    )
    exit()

if mode == "testing":
    from flask_cors import CORS

    CORS(app)
    print("running in testing mode")
    app.run(debug=True)
else:
    print("Invalid mode: Please run using either 'testing' or 'production'")
    exit()
