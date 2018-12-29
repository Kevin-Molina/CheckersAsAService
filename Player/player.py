from Messages.messages import Messages

class PlayerState:
    USERNAME_SELECTION = 1
    IN_LOBBY = 2
    IN_QUEUE = 3
    SENDING_CHALLENGE = 4
    BEING_CHALLENGED = 5
    IN_GAME = 6

class Player:

    def __init__(self, socket):
        self.name = None
        self.game = None
        self.socket = socket
        self.state = PlayerState.USERNAME_SELECTION

    @property
    def lower_name(self):
        return self.name.lower()

    def move_to_lobby(self):
        self.state = PlayerState.IN_LOBBY
