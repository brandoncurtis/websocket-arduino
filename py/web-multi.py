#!/usr/bin/env python

import asyncio
import websockets
import random
import time

async def listener(websocket, path):
    name = await websocket.recv()
    return name

async def consumer(websocket, path, message):
    print("< {}".format(message))
    greeting = "Hello {}!".format(message)
    await websocket.send(greeting)
    print("> {}".format(greeting))

async def producer():
    await asyncio.sleep(2)
    mstime = int(time.time()*1000)
    val = 15+10*random.random()
    message = "{:d},{:0.2f}".format(mstime, val)
    return message

async def handler(websocket, path):
    while True:
        listener_task = asyncio.ensure_future(listener(websocket, path))
        producer_task = asyncio.ensure_future(producer())
        tasks = [listener_task, producer_task]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        if listener_task in done:
            message = listener_task.result()
            await consumer(websocket, path, message)
        else:
            listener_task.cancel()

        if producer_task in done:
            message = producer_task.result()
            await websocket.send(message)
        else:
            producer_task.cancel()

def main():
    start_server = websockets.serve(handler, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
