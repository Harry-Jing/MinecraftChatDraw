import sys
import asyncio
import websockets
import httpx

import signal
from threading import Thread
from mcdreforged.api.all import *

from .util import *



async def handler(websocket):
    recv: bytes = await websocket.recv()
    data: dict = json.loads(recv)
    print(f'<<< {data}')
    if websocket.path =='/save/url':
        img = httpx.get(data['url'])
        save_image(img, data['file_name'])
    await websocket.send("操作完成")
        


async def server(stop_sign):
    async with websockets.serve(handler, "localhost", 8765):
        while not stop_sign():
            await asyncio.sleep(1)

        

def ws_server(stop_sign):
    asyncio.run(server(stop_sign))

