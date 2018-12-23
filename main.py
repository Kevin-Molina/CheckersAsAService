import asyncio
import json
import websockets

from Server.server import Server
from Messages.messages import Messages

SERVER = Server()


async def register(websocket):
    pass


async def unregister(websocket):
    pass


async def validate_username(websocket):

    async for message in websocket:
        data = json.loads(message)
        print(data)
        if not data['username']:
            raise Exception
        username = data['username']

        if not SERVER.is_username_free(username):
            return username

        await websocket.send(Messages.INVALID_USERNAME)


async def connect(websocket, path):
    try:
        username = await validate_username(websocket)
    except:
        websocket.send()
    try:
        async for message in websocket:
            data = json.loads(message)
    finally:
        await unregister(websocket)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(connect, 'localhost', 6789))
asyncio.get_event_loop().run_forever()