class Player:

    def __init__(self, name, socket):
        self._name = name
        self._socket = socket
        self._game = None

    def join_game(self, game):
        self._game = game
