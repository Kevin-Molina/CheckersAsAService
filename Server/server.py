import re
from Messages.messages import Messages


class Server:

    def __init__(self):
        self._players = {}
        self._queue = None

    def is_valid_name(self, name):
        if re.match(r'^[a-zA-Z0-9_.-]*$', name):
            return True
        print('fal')
        return False

    def name_in_use(self, name):
        return name.lower() in self._players

    def register_player(self, player):
        self._players[player.lower_name] = player

    def disconnect_player(self, player):
        del self._players[player.lower_name]

        if player == self._queue:
            self._queue = None

    def get_by_name(self, name):
        return self._players.get(name, None)

    async def _send(self, socket, msg):
        await socket.send(msg)

    async def send_valid_username(self, player):
        await self._send(player.socket, Messages.VALID_USERNAME)

    async def send_invalid_username(self, player):
        await self._send(player.socket, Messages.INVALID_USERNAME)

    async def send_challenge_by_name(self, challenger, opponent_name):
        opponent = self.get_by_name(opponent_name)
        msg = Messages.create_invitation(challenger.name)
        await self._send(opponent.socket, msg)