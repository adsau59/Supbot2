import json
import socket

from tests.temp_client.main import System


def send_request(_request: dict):
    host = '127.0.0.1'
    port = 8423

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps(_request).encode('utf-8'))
        data = s.recv(1024).decode('utf-8')

    return data


def receive_event(system: System):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 3248))
    s.settimeout(10)
    s.listen(1)

    while system.is_on:
        try:
            conn, addr = s.accept()
            data = conn.recv(1024).decode('utf-8')
            event = json.loads(data)
            print(event)

            conn.send(json.dumps({"success": True}).encode('utf-8'))
        except socket.timeout:
            pass
