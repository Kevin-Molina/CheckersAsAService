import re


class Server:

    def __init__(self):
        self._players = {}
        self._queue = None

    def is_valid_name(self, name):
        if re.match(r'^[\w.-]+$', name):
            return True
        return False

    def is_available_name(self, name):
        return name.lower() in self._players

    def register_player(self, player):
        self._players[player.lower_name] = player

    def disconnect_player(self, player):
        del self._players[player.lower_name]

        if player == self._queue:
            self._queue = None
