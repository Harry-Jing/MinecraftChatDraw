import os
import sys
import json
import httpx
import asyncio
import websockets

from threading import Thread
from PIL import Image
from itertools import product
from fastapi import FastAPI
from mcdreforged.api.all import *

from .network import *
from .util import *


def on_load(server: PluginServerInterface, prev_module):
    global stop_threads
    server.register_command(
        Literal('!!draw')
        .then(Literal('list').runs(show_saved))
        .then(Literal('from')
            .then(Literal('url')
                .then(Text('url')
                    .runs(url2cmd)
                )
            )
            .then(Literal('saved')
                .then(Text('file_name')
                    .runs(file2cmd)
                )
            )
        )
        .then(Literal('save')
           .then(Literal('url')
                .then(Text('url')
                    .runs(lambda : ...)
                )
            )
        )
    )

    server.register_help_message('!!draw', '用滑稽的方式在mc的聊天栏输出图片')
    plug_config = server.load_config_simple()
    if plug_config['enabel_ws_server']:
        stop_threads = False
        ws_server_task = Thread(target=ws_server, args=(lambda: stop_threads, ), daemon=True)
        ws_server_task.start()

def on_unload(server: PluginServerInterface):
    global stop_threads
    from time import sleep
    stop_threads = True
    sleep(1.5)







       

    