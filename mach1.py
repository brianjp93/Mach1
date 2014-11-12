"""
mach1.py
"""
import serial, struct, time, glob, sys
from pytek import TDS3k
import matplotlib.pyplot as plt
import numpy as np

class Mach1():
	# static variables
	cmd = {
	"home": 1, 
	"moveAbsolute": 20, 
	"moveRelative": 21,
	"setTargetSpeed": 42,
	"storeCurrentPosition": 16
	}

	translation = {"hor": 0, "ver": 1}
	# microstep in mm
	microstep = 0.00009921875

	def __init__(self):
		# Serial() input depends on where stage is connected
		self.stage = serial.Serial(2)
		self.osc = TDS3k(serial.Serial("COM1", 9600, timeout=1))

	def convertSpeed(self, v):
		"""
		v - in mm/s
			converts v to units that make sense to stage and returns converted
		"""
		converted = 1/(Mach1.microstep*9.375)
		return converted

	def zaberMove(self, command = None, data = None):
		if command == None or data == None:
			Exception("Method zaberMove must take inputs command, data.")

	def setSpeed(self, v):
		"""
		v - speed to set in mm
		converts to numbers that the stage wants and calls a command in the cmd dictionary
		"""
		converted = self.convertSpeed(v)
		# set both stage speeds
		self.zaberSend(Mach1.translation["hor"], self.cmd["setTargetSpeed"], data = converted)
		self.zaberSend(Mach1.translation["ver"], self.cmd["setTargetSpeed"], data = converted)

	def zaberReceive(self):
		# return 6 bytes from the receive buffer
		# there must be 6 bytes to receive (no error checking)
		r = [0,0,0,0,0,0]
		for i in range (6):
			r[i] = ord(self.stage.read(1))
			return r

	def zaberSend(self, device, command, data=0):
		"""
		send a packet using the specified device number, command number, and data
		The data argument is optional and defaults to zero
		"""
		packet = struct.pack('<BBl', device, command, data)
		self.stage.write(packet)
		r = self.zaberRecieve()
		return r

	def getSingleMeasurement(self, ch = "CH1"):
		"""
		ch - "CH1" or "CH2"
			input which channel you want data from.
		returns y value from get_waveform() aka Voltage Reading from oscilloscope
		"""
		counter = 1
		# added try except block to take care of times when get_waveform() has a problem.
		while True:
			try:		
				waveform = self.osc.get_waveform(source = ch, start = 0, stop = 0)
				break
			except:
				print("Retry: " + str(counter))
				counter += 1
		for x,y in waveform:
			voltage = y
		return voltage