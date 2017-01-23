# Remote Control Server


## V1,2

Only perform a subset of the desired message-passing operations (serial-to-websocket, websocket-to-serial).

----

## V3

WORKS - v3.py reads incoming data over the serial port and appends it to a list.  Once per second, the most recent 
value in the list is written to the websocket.

## V4

WORKS - v4.py also has data lookback when the websocket is created.

## V5

WORKS - v5.py adds additional input checking and has support for multiple data inputs.

----

## To Do

+ implement security on write operations
+ using `logging` module to write data to logfile
