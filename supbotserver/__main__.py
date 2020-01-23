from supbotserver import webserver
from supbotserver.controller import looper
from supbotserver.shared_states import action_buffer, event, system
import threading
from multiprocessing import Process

from supbotserver.shared_states.client import Client


def run():
    _action_buffer = action_buffer.ActionBuffer()
    _event = event.EventHandler()
    _system = system.System()
    client = Client(_action_buffer)

    looper_thread = threading.Thread(target=looper.start_looper, args=(_action_buffer, _event, _system,))
    web_thread = Process(target=webserver.start_flask, args=(client,))
    looper_thread.start()
    web_thread.start()

    _system.wait()
    _system.set_status(False)

    looper_thread.join()
    web_thread.terminate()
    web_thread.join()


if __name__ == '__main__':
    run()
