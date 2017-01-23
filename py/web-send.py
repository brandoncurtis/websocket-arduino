#!/usr/bin/env python

import asyncio
import websockets
import random
import time

async def mysend(websocket, path):
    while True:
        mystr = "{:d},{:0.2f}".format(int(time.time()*1000),15+10*random.random())
        await websocket.send(mystr)
        await asyncio.sleep(2)

start_server = websockets.serve(mysend, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
