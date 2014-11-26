__author__ = 'Brian Perrett'
"""
11/23/2014
Basically same as mach1.py, except this uses only
    the zaber transition slides.
"""
import serial, struct, time, glob, sys


class Mach2():
    #  static variables
	cmd = {
	"home": 1,
	"moveAbsolute": 20,
	"moveRelative": 21,
	"setTargetSpeed": 42,
	"storeCurrentPosition": 16,
	"returnStoredPosition": 17,
	"moveToStoredPosition": 18,
	"returnStatus": 54
	}

	translation = {"both": 0, "hor": 1, "ver": 2}
	# microstep in mm
	microstep = 0.00009921875

	def __init__(self, zaberStagePort = 2):
		"""
		initialize variables.
		oscPort - Port for oscilloscope.  COM1 by default.  Could be COM2 or 3 as well.
		zaberStagePort - Port for zaber stage.  2 by default.  Could be 0 or 1.
		"""
		# Serial() input depends on where stage is connected
		self.stage = serial.Serial(zaberStagePort)

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
		device - "hor" or "ver"
		"""
		packet = struct.pack('<BBl', self.translation[device], command, data)
		self.stage.write(packet)
		r = self.zaberReceive()
		return r

	def zaberStoreLocation(self, stage, address):
		"""
		stores location data at given address in the zaber stage.
		__Variables__
		stage - hor or ver
		address - number 0-15
		"""
		self.zaberSend(stage, self.cmd["storeCurrentPosition"], address)

	def zaberMoveToStoredLocation(self, stage, address):
		"""
		Moves to stored location at given address in the zaber stage.
		__Variables__
		stage - hor or ver
		address - number 0-15
		"""
		self.zaberSend(stage, self.cmd["moveToStoredPosition"], address)

	def convertDistance(self, mm):
		"""
		converts mm to microsteps
		__Variables__
		mm - millimeters
		"""
		return mm/(self.microstep)

	def convertSpeed(self, v):
		"""
		Converts v to units that make sense to stage and returns converted
		__Variables__
		v - in mm/s
		"""
		converted = v/(self.microstep * 9.375)
		return converted

	def zaberMove(self, stage, command = None, data = None):
		"""
		Moves horizontal or vertical translation stage data mm.
		__Variables__
		stage - "hor" or "ver"
		command - one of the movement commands from the cmd dictionary.
		data - a distance in mm.
		"""
		if command == None or data == None:
			raise Exception("Method zaberMove must take inputs command, data.")
		else:
			dist = self.convertDistance(data)
			r = self.zaberSend(stage, command, dist)
		return r

	def setSpeed(self, v):
		"""
		Sets both translation stage speeds
		__Variables__
		v - speed to set in mm
		converts to numbers that the stage wants and calls a command in the cmd dictionary
		"""
		converted = self.convertSpeed(v)
		print(converted)
		# set both stage speeds
		self.zaberSend(self.translation["hor"], self.cmd["setTargetSpeed"], data = converted)
		self.zaberSend(self.translation["ver"], self.cmd["setTargetSpeed"], data = converted)

	def wait(self):
		"""
		stops program until both stages return idle statuses
		not sure this is working...
		"""
		while True:
			r1 = self.zaberSend(self.translation["hor"], self.cmd["returnStatus"], data=0)
			r2 = self.zaberSend(self.translation["ver"], self.cmd["returnStatus"], data=0)
			if r1[2] == 0 and r2[2] == 0:
				break
			else:
				time.sleep(.01)