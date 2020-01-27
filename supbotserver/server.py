import socket

import json

from supbotserver.model import actions
from supbotserver.sharedstates.action_buffer import IActionBuffer
from supbotserver.sharedstates.system import ISystem


def run_action(buffer: IActionBuffer, action_name: str, json_params: dict):
    buffer.add_action(actions[action_name].json_to_action(json_params))
    return {"success": True}


def send_event(event_type: str, event_data: dict):
    host = '127.0.0.1'
    port = 3248

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps({"function": "event", "data": {"name": event_type, "params": event_data}}).encode('utf-8'))
        data = s.recv(1024).decode('utf-8')

    return json.loads(data)["success"]


def start(buffer: IActionBuffer, system: ISystem):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 8423))

    system.get_logger().info("Waiting for client")
    s.listen(1)

    while system.is_on():
        conn, addr = s.accept()
        system.get_logger().info(f"Receiving  request from {addr}")
        data = conn.recv(1024).decode('utf-8')
        data_json = json.loads(data)
        result = {"success": False}
        if data_json["function"] == "run_action":
            result = run_action(buffer, data_json["data"]["name"], data_json["data"]["params"])
        elif data_json["function"] == "quit":
            system.quit()
            result = {"success": True}

        conn.send(json.dumps(result).encode('utf-8'))

    s.close()
