import socket


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


def contact_number_equal(from_whatsapp: str, from_request: str):
    if from_whatsapp == from_request:
        return True

    new_number = ""
    for i in from_whatsapp:
        if i.isdigit():
            new_number += i

    if new_number == from_request:
        return True

    return False
