from datetime import datetime
from flask import Flask
from flask import make_response
from flask import request
import json
from gevent.pywsgi import WSGIServer
import requests
import time
from threading import Timer
import os


APP = Flask(__name__)
BOT_TOKEN = None
PORT = 5001
HANDLING_PATH = "/report_bot"

USER_MAP = None


def main():
    global BOT_TOKEN
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    if BOT_TOKEN is None:
        exit(1)

    load_user_map()

    http_server = WSGIServer(('', PORT), APP)
    http_server.serve_forever()


def load_user_map():
    global USER_MAP
    file = open("user_map.json")

    USER_MAP = json.loads(file.read())


@APP.route(HANDLING_PATH, methods=['POST'])
def endpoint():
    print (request.form)
    if "payload" in request.form:
        # handling form responses
        payload = json.loads(request.form["payload"])
        action = payload["actions"][0]
        action_id = action["action_id"]

        if action_id == "some_action":
            raw_value = action["selected_option"]["value"]
            user_id = payload["user"]["id"]
            channel_id = payload["container"]["channel_id"]

            return something(user_id, action_id)

    # simple requests
    if request.form['text'] == "help":
        return help()

    return help()

def help():
    help_text = """
TBD
"""
    return simple_response_with_text(help_text)

def something(user, action):
    pass


def simple_response_with_text(text):
    body = {"blocks":[
    {
        "type": "section",
        "block_id": "header",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }]}

    resp = make_response(json.dumps(body), 200)
    resp.headers["Content-type"] = "application/json"

    return resp

def post(body_blocks, where):
    body = {"blocks": json.dumps(blocks),
            "as_user": "true",
            "response_type": "in_channel",
            "channel": where,
            "token": BOT_TOKEN}

    url = "https://slack.com/api/chat.postMessage"
    resp = requests.post(url, data=body, headers={"acccept": "application/json"})
    print("Sent a message by POST resp is: %s" % resp.text)
    return resp

if __name__ == "__main__":
    main()
