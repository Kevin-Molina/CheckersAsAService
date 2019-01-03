import re
from Messages.messages import Messages
from Game.game import Game
from Player.player import PlayerState, Player
import asyncio
import websockets
import json
import logging


class Server:
    LOGFILE = 'log.txt'

    def __init__(self, ip, port):
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO,
                            filename=self.LOGFILE)
        self._players = {}
        self._queue = None
        self.ip = ip
        self.port = port

    def run(self, ip, port):
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self._dispatcher, ip, port))
        asyncio.get_event_loop().run_forever()

    async def _dispatcher(self, websocket, path):
        player = Player(websocket)

        try:
            async for message in player.socket:
                data = json.loads(message)

                if player.state == PlayerState.USERNAME_SELECTION:

                    if 'username' in data:
                        name = data['username']
                        if self._is_valid_name(name):
                            player.name = name
                            self.register_player(player)

                            await self.send_valid_username(player)
                        else:
                            await self.send_invalid_username(player)

                elif player.state == PlayerState.IN_LOBBY:

                    if 'challengePlayer' in data:
                        opponent_name = data['challengePlayer']
                        if self.name_in_use(opponent_name) and opponent_name.lower() != player.lower_name:
                            await self.send_challenge_by_name(player, opponent_name)
                        else:
                            pass

                    elif 'joinQueue' in data:
                        do_join = data['joinQueue']
                        if do_join:
                            await self.join_queue(player)

                    elif 'leaveQueue' in data:
                        self.leave_queue(player)
                elif player.state == PlayerState.IN_GAME:

                    if 'move' in data:
                        move = data['move']
                        await self.handle_turn(player, move)

        finally:
            await self.disconnect_player(player)

    def _is_valid_name(self, name):
        return re.match(r'^[a-zA-Z0-9_.-]{1,20}$', name) and name.lower() not in self._players

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
        logging.info(msg)

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

    async def send_invalid_move(self, player):
        await self._send(player.socket, Messages.INVALID_MOVE)

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
            self._queue = player
            await self.send_estimated_wait_time(player)
        else:
            player_two = self._queue
            self._queue = None
            await self._start_game(player, player_two)

    async def _start_game(self, player_one, player_two):
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

        try:
            game.do_turn(player, move)
        except:
            await self.send_invalid_move(player)
        else:
            opponent = game.get_opponent(player)
            winner = game.get_winner_or_none()
            await self.send_move(opponent, move)
            await self.send_valid_move(player)





