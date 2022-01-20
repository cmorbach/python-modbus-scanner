# modbus-scanner
Scans a modbus for any devices
- using Python 3 and lib minimalmodbus
- tested on Linux and Windows

# installation
```
pip install minimalmodbus
```

# usage
edit parameters what you want to scan in the tail of the file

```python
scanModbus(device="COM7",		# or like /dev/ttyUSB0 on Linux
	baudrates=[1200, 9600],		# scan baud rates 1200 and 9600
	devAddresses=range(1, 10+1),	# scan device addresses 1 to 10
	regAddresses=range(1, 3+1),	# test registers 1 to 3
	timeout=0.2)			# device not present if no reply within 0.2s (fine for 1200 bauds)
```
start the scan


```
# python main.py
modbus scanner
..XX..XX..XX..XX..XX..XXX...X...X.......................................................................................
[{'baudrate': 9600, 'devAddress': 1, 'registers': {1, 2, 3}},
 {'baudrate': 9600, 'devAddress': 2, 'registers': {1, 2, 3}},
 {'baudrate': 9600, 'devAddress': 3, 'registers': {1, 2, 3}}]
scan is quite reliable
```
