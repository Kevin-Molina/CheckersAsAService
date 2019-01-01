import asyncio
import json
import websockets
import logging

from Server.server import Server
from Player.player import Player, PlayerState


async def disconnect(player):
    await SERVER.disconnect_player(player)
    # Todo - Check if player was in a game


async def on_connect(websocket, path):
    player = Player(websocket)

    try:
        async for message in player.socket:
            logging.info("Msg received: ", message)
            data = json.loads(message)

            if player.state == PlayerState.USERNAME_SELECTION:

                if 'username' in data:
                    name = data['username']
                    if SERVER.is_valid_name(name) and not SERVER.name_in_use(name):
                        player.name = name
                        SERVER.register_player(player)

                        await SERVER.send_valid_username(player)
                    else:
                        await SERVER.send_invalid_username(player)

            elif player.state == PlayerState.IN_LOBBY:

                if 'challengePlayer' in data:
                    opponent_name = data['challengePlayer']
                    if SERVER.name_in_use(opponent_name) and opponent_name.lower() != player.lower_name:
                        await SERVER.send_challenge_by_name(player, opponent_name)
                    else:
                        pass

                elif 'joinQueue' in data:
                    do_join = data['joinQueue']
                    if do_join:
                        await SERVER.join_queue(player)

                elif 'leaveQueue' in data:
                    SERVER.leave_queue(player)
            elif player.state == PlayerState.IN_GAME:

                if 'move' in data:
                    move = data['move']
                    await SERVER.handle_turn(player, move)
    finally:
        await disconnect(player)

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
SERVER = Server()

asyncio.get_event_loop().run_until_complete(
    websockets.serve(on_connect, 'localhost', 6789))
asyncio.get_event_loop().run_forever()
