import ctypes
import socket
import threading
from threading import Timer


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


def kill_thread(thread):
    thread_id = _get_id(thread)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                     ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')


# noinspection PyProtectedMember
def _get_id(thread):
    # returns id of the respective thread
    if hasattr(thread, '_thread_id'):
        return thread._thread_id
    for id, thread in threading._active.items():
        if thread is thread:
            return id
