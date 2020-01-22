from supbotserver.controller import looper
from supbotserver.shared_states import action_buffer, event, system
import threading


def run():
    queue = action_buffer.ActionBuffer()
    _event = event.EventHandler()
    _system = system.System()

    looper_thread = threading.Thread(target=looper.start_looper, args=(queue, _event, _system,)).start()

    _system.wait()
    _system.set_status(False)

    looper_thread.join()


if __name__ == '__main__':
    run()
