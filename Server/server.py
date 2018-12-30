import re
from Messages.messages import Messages
from Game.game import Game

class Server:

    def __init__(self):
        self._players = {}
        self._queue = None

    @staticmethod
    def is_valid_name(name):
        if re.match(r'^[a-zA-Z0-9_.-]*$', name):
            return True
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

    async def join_queue(self, player):
        if not self._queue:
            self._queue = player
        else:
            player_two = self._queue
            self._queue = None
            await self._start_game(player, player_two)

    async def _start_game(self, player_one, player_two):
        game = Game(player_one, player_two)
        if game.players_turn == player_one:

            player_one_msg = Messages.game_start(player_two.name, True)
            await self._send(player_one.socket, player_one_msg)

            player_two_msg = Messages.game_start(player_one.name, False)
            await self._send(player_two.socket, player_two_msg)




