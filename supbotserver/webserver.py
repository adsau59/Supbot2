from flask import Flask, request, json
import os
import logging

from supbotserver.model import actions
from supbotserver.sharedstates.action_buffer import IActionBuffer


def hello_world():
    return 'Hello, World!'


class WebServer:

    def __init__(self, buffer: IActionBuffer):
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'
        logging.getLogger('werkzeug').disabled = True

        self.app = Flask(__name__)
        self.buffer = buffer

        self.app.add_url_rule('/', view_func=hello_world)
        self.app.add_url_rule('/action/<action_name>', view_func=self.send_message, methods=['GET', 'POST'])

    def send_message(self, action_name):
        self.buffer.add_action(actions[action_name].json_to_action(request.json))
        return json.dumps({"success": True})

    def start(self):
        self.app.run()
