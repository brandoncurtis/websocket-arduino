# Remote Control Server

## Using `websocketd`

This is BY FAR the easiest way to start playing with websockets TODAY.

`websocketd` is created by Joe Walnes: https://github.com/joewalnes/websocketd/

For example, you can pipe the incoming Arduino serial data into a logfile:

`nice -20 cat /dev/ttyACM0 > current.csv &`

then use `websocketd` to serve the data that comes from tailing this logfile:

`websocketd --port=8080 tail -f -n 1000 current.csv`

The serving script can be pretty much anything that writes to STDOUT and reads from STDIN,
in any language of your choice. With a little Python non-blocking reading, I bet you could
even implement a simple chat server!

----

## Using Python `websocket` and `serial-aio`

You'll need to learn some asynchronous programming in Python, but this is a good starting
point for more complex servers.

### Software Versions

#### V1,2

Only perform a subset of the desired message-passing operations (serial-to-websocket, websocket-to-serial).

#### V3

WORKS - v3.py reads incoming data over the serial port and appends it to a list.  Once per second, the most recent 
value in the list is written to the websocket.

#### V4

WORKS - v4.py also has data lookback when the websocket is created.

#### V5

WORKS - v5.py adds additional input checking and has support for multiple data inputs.

#### V4a

WORKS - v4a.py has some minor refactoring and tweaks for working with 555.html

**THIS** was the point where everything was version controlled in its own repository!

----

## To Do

+ implement security on write operations
+ using `logging` module to write data to logfile
