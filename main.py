#!/usr/bin/env python3
import minimalmodbus
import serial
from pprint import pprint


lastPrintDot = False
def foundDevice(baudrate, devAddress, regAddress, value):
	global lastPrintDot
	if lastPrintDot:
		print()
		lastPrintDot = False
	print(f"found device(baudrate={baudrate}, devAddress={devAddress}, regAddress={regAddress}, value={value})")


def foundDeviceI(instrument, regAddress, value):
	foundDevice(instrument.serial.baudrate, instrument.address, regAddress, value)


def printDot(dot="."):
	global lastPrintDot
	print(dot, end="")
	lastPrintDot = True


def minimalModbusInstrument(device, baudrate=9600, devAddress=1, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=0.2,
							modbusMode = minimalmodbus.MODE_RTU, clear_buffers_before_each_transaction = True,
							close_port_after_each_call = False, debug = False):
	instrument = minimalmodbus.Instrument(device, devAddress)
	instrument.serial.baudrate = baudrate
	instrument.serial.bytesize = bytesize
	instrument.serial.parity = parity
	instrument.serial.stopbits = stopbits
	instrument.serial.timeout = timeout  # seconds
	instrument.mode = modbusMode
	instrument.clear_buffers_before_each_transaction = clear_buffers_before_each_transaction
	instrument.close_port_after_each_call = close_port_after_each_call
	instrument.debug = debug
	return instrument


def scanInstrument(instrument, regAddress, functioncode, printFindings=False, printDots=True):
	try:
		if functioncode in [1, 2]:
			value = instrument.read_bit(registeraddress=regAddress, functioncode=functioncode)
		elif functioncode in [3, 4]:
			value = instrument.read_register(registeraddress=regAddress, number_of_decimals=0, signed=False, functioncode=functioncode)
		else:
			raise Exception("no such functioncode")
		if printFindings:
			foundDeviceI(instrument, regAddress, value)
		elif printDots:
			printDot("X")
		return True
	except:
		if printDots:
			printDot()
	return False


def scanModbus(device="COM7", baudrates=[1200, 1800, 2400, 4800, 9600, 19200, 115200], devAddresses=range(1, 247+1), regAddresses=range(1, 3+1), timeout=0.2):
	print("modbus scanner")
	foundDevices = []

	for baudrate in baudrates:
		for devAddress in devAddresses:
			instrument = minimalModbusInstrument(device, baudrate=baudrate, devAddress=devAddress, timeout=timeout)
			registers = set()

			for regAddress in regAddresses:
				for functioncode in [1, 2, 3, 4]:
					if scanInstrument(instrument, regAddress, functioncode=functioncode):
						registers.add(regAddress)

			if len(registers) > 0:
				foundDevices.append({"baudrate": baudrate, "devAddress": devAddress, "registers":registers})

	print()
	pprint(foundDevices)

	# final connection test
	try:
		instrument = minimalmodbus.Instrument(device, 0)
		print("scan is quite reliable")
	except:
		print("scan is definitely unreliable")


if __name__ == '__main__':
	scanModbus(device="COM7",
				baudrates=[9600],
				devAddresses=range(1, 10+1),
				regAddresses=range(1, 3+1),
				timeout=0.04)
