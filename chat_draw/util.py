import os
import re
import sys
import json
import httpx
import hashlib
import asyncio
import websockets

from io import BytesIO
from hashlib import sha256
from multiprocessing import Process
from PIL import Image
from itertools import product
from fastapi import FastAPI
from mcdreforged.api.all import *



def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]


def img2cmd(img):
    img = Image.open(img)
    width, height = img.width, img.height
    img = img.resize((320, int(height/(img.width*9/320))))
    img = img.convert('RGB')
    data = []
    for h, w in product(range(img.height), range(img.width)):
        r,g,b = img.getpixel((w,h))
        data.append({'text':'|', 'color':f'#{r:0>2X}{g:0>2X}{b:0>2X}'})

    return ['tellraw @a '+json.dumps(i) for i in cut(data, 320)]


def url2cmd(src: CommandSource, ctx: dict):
    server = src.get_server()
    img = httpx.get(ctx['url'])
    cmd_list = img2cmd(img)
    for i in cmd_list:
        server.execute(i)


def show_saved(src: CommandSource, ctx: dict):
    for root,dirs,files in os.walk('config/chat_draw/data'):
        for file in files:
            src.reply(file.rstrip('.png'))
        



def file2cmd(src: CommandSource, ctx: dict):
    server = src.get_server()
    file = f'config/chat_draw/data/{ctx["file_name"]}.png'
    try:
        cmd_list = img2cmd(file)
    except FileNotFoundError as exc:
        src.reply(RText(text='没有此文件', color=RColor.red))
        raise exc

    for i in cmd_list:
        server.execute(i)

def save_image(img: bytes, file_name: str):
    img_data = Image.open(img)
    img_data.convert('RGB')
    img_data.save(f'config/chat_draw/data/{file_name}.png')


def help_message(src: CommandSource, ctx: dict):
    pass