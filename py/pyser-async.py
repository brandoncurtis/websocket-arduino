# from: https://pyserial-asyncio.readthedocs.io/en/latest/api.html
# basically identical to:
# "Register an open socket to wait for data using a protocol"
# https://docs.python.org/dev/library/asyncio-protocol.html#asyncio-register-socket

import serial.aio
import asyncio

class serPort(asyncio.Protocol):
    msg = ""

    def connection_made(self, transport):
        self.transport = transport
        transport.serial.flush()
        if transport.flushed():
            print('port opened', transport)
        transport.serial.rts = False
        #transport.write(b'hello world\n')

    def data_received(self, data):
        datastr = data.decode('utf-8')
        print("msg is currently: {}".format(self.msg))
        self.msg += datastr
        if '\n' in self.msg:        
            print("complete string: {!s}".format(self.msg))
            self.msg = ""
        #self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()

loop = asyncio.get_event_loop()
coro = serial.aio.create_serial_connection(loop, serPort, '/dev/arduino', 
baudrate=38400,timeout=0.2)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
