import asyncio
import json
import websockets

from Server.server import Server
from Player.player import Player, PlayerState

SERVER = Server()


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

                if SERVER.is_valid_name(name) and SERVER.is_available_name(name):
                    player.name = name
                    SERVER.register_player(player)
                    player.move_to_lobby()

                    await player.send_valid_username()
                else:
                    await player.send_invalid_username()

            if player.state == PlayerState.IN_LOBBY:
                pass

    finally:
        await disconnect(player)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(on_connect, 'localhost', 6789))
asyncio.get_event_loop().run_forever()