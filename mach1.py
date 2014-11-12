"""
mach1.py
"""
import serial, struct, time, glob, sys
from pytek import TDS3k
import matplotlib.pyplot as plt
import numpy as np

class Mach1():

	# static variables
	cmd = {"home": 0, "moveAbsolute": 0, "moveRelative": 0}
	translation = {"hor": 0, "ver": 1}

	def __init__():
		# Serial() input depends on where stage is connected
		stage = serial.Serial(2)
		osc = TDS3k(serial.Serial("COM1", 9600, timeout=1))

	def convertSpeed(v):
		"""
		input
		"""
		converted = 0
		return converted

	def zaberMove(command = None, data = None):
		if command == None or data == None:
			Exception("Method zaberMove must take inputs command, data.")

	def setSpeed(v):
		"""
		v - speed to set in mm
		"""
		converted = 0
		return converted

	def getSingleMeasurement(ch = "CH1"):
		"""
		ch - "CH1" or "CH2"
			input which channel you want data from.
		returns y value from get_waveform() aka Voltage Reading from oscilloscope
		"""
		counter = 1
		# added try except block to take care of times when get_waveform() has a problem.
		while True:
			try:		
				waveform = osc.get_waveform(source = ch, start = 0, stop = 0)
				break
			except:
				print("Retry: " + str(counter))
				counter += 1
		for x,y in waveform:
			voltage = y
		return voltage