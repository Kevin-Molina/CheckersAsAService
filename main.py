import asyncio
import json
import websockets

from Server.server import Server
from Player.player import Player, PlayerState
from Messages.messages import Messages
from Board.board import Board

SERVER = Server()

b = Board()

print(b.board)
print([i for i in range(64)])


async def disconnect(player):
    SERVER.disconnect_player(player)
    # Todo - Check if player was in a game

async def on_connect(websocket, path):
    player = Player(websocket)

    try:
        async for message in player.socket:
            data = json.loads(message)

            if player.state == PlayerState.USERNAME_SELECTION:
                name = data.get('username', None)

                if SERVER.is_valid_name(name) and not SERVER.name_in_use(name):
                    player.name = name
                    SERVER.register_player(player)
                    player.move_to_lobby()

                    await SERVER.send_valid_username(player)
                else:
                    await SERVER.send_invalid_username(player)

            if player.state == PlayerState.IN_LOBBY:

                if 'challengePlayer' in data:
                    opponent_name = data['challengePlayer']
                    if SERVER.name_in_use(opponent_name) and opponent_name.lower() != player.lower_name:
                        await SERVER.send_challenge_by_name(player, opponent_name)
                    else:
                        pass





    finally:
        print(player.name, end='')
        print(' disconnected')
        await disconnect(player)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(on_connect, 'localhost', 6789))
asyncio.get_event_loop().run_forever()

