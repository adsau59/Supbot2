from flask import Flask, request, json
import os
import logging

from supbotserver.shared_states.client import IClient

app = Flask(__name__)
client: IClient


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    content = request.json
    client.send_message(content["chat"], content["message"])
    print(content)
    return json.dumps({"success": True})


@app.route('/')
def hello_world():
    return 'Hello, World!'


def start_flask(_client: IClient):
    global client

    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    logging.getLogger('werkzeug').disabled = True
    client = _client
    app.run()
