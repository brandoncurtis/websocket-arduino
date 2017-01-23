#!/usr/bin/env python

import asyncio
import serial.aio
import websockets
import random
import time

class serPort(asyncio.Protocol):
    msg = ""

    def connection_made(self, transport):
        self.transport = transport
        transport.serial.flush()
        print('port opened', transport)
        transport.serial.rts = False
        #transport.write(b'hello world\n')

    def data_received(self, data):
        datastr = data.decode('utf-8')
        #print("msg is currently: {}".format(self.msg))
        self.msg += datastr
        if '\n' in self.msg:
            #print("complete string: {!s}".format(self.msg))
            message = self.msg
            self.msg = ""
            return message
        #self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()

"""
loop = asyncio.get_event_loop()
coro = serial.aio.create_serial_connection(loop, serPort, '/dev/arduino',
baudrate=38400,timeout=0.2)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
"""


async def listener(websocket, path):
    name = await websocket.recv()
    return name

async def consumer(websocket, path, message):
    print("< {}".format(message))
    greeting = "Hello, {}!".format(message)
    await websocket.send(greeting)
    print("> {}".format(greeting))

async def producer():
    await asyncio.sleep(2)
    mstime = int(time.time()*1000)
    val = 15+10*random.random()
    message = "{:d},{:0.2f}".format(mstime, val)
    return message

async def handler(websocket, path):
    loop = asyncio.get_event_loop()
    listener_task = asyncio.ensure_future(listener(websocket, path))
    #producer_task = asyncio.ensure_future(producer())
    ser_coro = serial.aio.create_serial_connection(loop, serPort, '/dev/arduino',
                                                   baudrate=38400)
    producer_task = asyncio.ensure_future(ser_coro)

    while True:
        tasks = [listener_task, producer_task]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        if listener_task in done:
            print("listener_task triggered!")
            message = listener_task.result()
            await consumer(websocket, path, message)
        else:
            listener_task.cancel()

        if producer_task in done:
            print("producer_task triggered!")
            message = producer_task.result()
            print("producer_task: {}".format(message))
            #await websocket.send(message)
        else:
            producer_task.cancel()

def main():
    start_server = websockets.serve(handler, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
