from supbotserver.controller import looper
from supbotserver.sharedstates import action_buffer, event, system
import threading

from supbotserver.webserver import WebServer


def run():
    _action_buffer = action_buffer.ActionBuffer()
    _event = event.EventHandler()
    _system = system.System()

    looper_thread = threading.Thread(target=looper.start_looper, args=(_action_buffer, _event, _system,))
    looper_thread.start()

    _webserver = WebServer(_action_buffer)

    _webserver.start()
    _system.set_status(False)

    looper_thread.join()


if __name__ == '__main__':
    run()
