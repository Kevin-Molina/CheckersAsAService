import re
from Messages.messages import Messages
from Game.game import Game
from Player.player import PlayerState


class Server:

    def __init__(self):
        self._players = {}
        self._queue = None

    @staticmethod
    def is_valid_name(name):
        if re.match(r'^[a-zA-Z0-9_.-]{1,20}$', name):
            print('true')
            return True
        return False
        print('false')
    def name_in_use(self, name):
        return name.lower() in self._players

    def register_player(self, player):
        self._players[player.lower_name] = player
        player.state = PlayerState.IN_LOBBY

    async def disconnect_player(self, player):
        del self._players[player.lower_name]

        if player.state == PlayerState.IN_GAME:
            game = player.game
            if game.player_one is player:
                await self.opponent_disconnected(game.player_two)
            else:
                await self.opponent_disconnected(game.player_one)

        elif self._queue is player:
            self._queue = None

    def get_by_name(self, name):
        return self._players.get(name.lower(), None)

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

    async def send_estimated_wait_time(self, player):
        await self._send(player.socket, Messages.ESTIMATED_WAIT_TIME)

    async def send_invalid_move(self, player, error_msg):
        msg = Messages.invalid_move(error_msg)
        await self._send(player.socket, error_msg)

    async def send_valid_move(self, player):
        await self._send(player.socket, Messages.VALID_MOVE)

    async def send_move(self,player, move):
        await self._send(player.socket, Messages.move(move))

    async def opponent_disconnected(self, player):
        player.state = PlayerState.IN_LOBBY
        await self._send(player.socket, Messages.OPPONENT_DISCONNECTED)

    def leave_queue(self, player):
        if self._queue is player:
            self._queue = None
            player.state = PlayerState.IN_LOBBY

    async def join_queue(self, player):
        if self._queue is player:
            pass

        elif not self._queue:
            print(player.name, "has joined")
            self._queue = player
            await self.send_estimated_wait_time(player)
        else:
            print('else')
            player_two = self._queue
            self._queue = None
            await self._start_game(player, player_two)

    async def _start_game(self, player_one, player_two):
        print('started')
        game = Game(player_one, player_two)

        player_one.state = PlayerState.IN_GAME
        player_two.state = PlayerState.IN_GAME

        player_one.game = game
        player_two.game = game

        if game.players_turn is player_one:

            player_one_msg = Messages.game_start(player_two.name, True)
            await self._send(player_one.socket, player_one_msg)

            player_two_msg = Messages.game_start(player_one.name, False)
            await self._send(player_two.socket, player_two_msg)
        else:
            player_one_msg = Messages.game_start(player_two.name, False)
            await self._send(player_one.socket, player_one_msg)

            player_two_msg = Messages.game_start(player_one.name, True)
            await self._send(player_two.socket, player_two_msg)

    async def handle_turn(self, player, move):
        game = player.game
        for i in game.board.board:
            print(i)
        try:
            game.do_turn(player, move)
        except Exception as e:
            await self.send_invalid_move(player, str(e))
        else:
            opponent = game.get_opponent(player)
            await self.send_move(opponent, move)
            await self.send_valid_move(player)



