from supbotserver import server
from supbotserver.controller import looper
from supbotserver.sharedstates import action_buffer, system
import threading
import loguru


def run():
    _action_buffer = action_buffer.ActionBuffer()
    _system = system.System(loguru.logger)

    looper_thread = threading.Thread(target=looper.start, args=(_action_buffer, _system,))
    looper_thread.start()

    server_thread = threading.Thread(target=server.start, args=(_action_buffer, _system,))
    server_thread.start()

    server_thread.join()
    looper_thread.join()


if __name__ == '__main__':
    run()
