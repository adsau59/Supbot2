from __future__ import annotations

import json
import socket
import typing
if typing.TYPE_CHECKING:
    from supbotclient import EventHandler


def send_request(_request: dict):
    host = '127.0.0.1'
    port = 8423

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps(_request).encode('utf-8'))
        data = s.recv(1024).decode('utf-8')

    return data


def receive_event(event: EventHandler):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 3248))
    s.settimeout(10)
    s.listen(1)

    while event.is_on:
        try:
            conn, addr = s.accept()
            data = json.loads(conn.recv(1024).decode('utf-8'))

            if data["function"] == "event":
                event.call_event(data["data"]["name"], data["data"]["params"])

            conn.send(json.dumps({"success": True}).encode('utf-8'))
        except socket.timeout:
            pass
