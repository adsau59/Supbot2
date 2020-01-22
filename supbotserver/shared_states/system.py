from supbotserver.shared_states import interface


class System(interface.ISystem):

    def __init__(self):
        self.status = True

    def get_status(self) -> bool:
        return self.status

    def set_status(self, status:bool):
        self.status = status

    def wait(self):
        input("enter to quit")
