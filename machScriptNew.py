"""
machScriptNew.py
Brian Perrett
11/26/2014
Cleaner script for moving the zaber stage and making measurements with the mach zehnder interferometer
"""
from mach1 import Mach1
# import time
import numpy as np
import matplotlib.pyplot as plt

# relevant variables
print("setting variables")
opticDiameter = 50 # mm
print("optic diameter = " + str(opticDiameter) + " mm.")
numScans = 4 # number of scans to do across the optic
print("# Vertical Scans = " + str(numScans) + ".  " + str(numScans**2) + " measurements to be taken.")
dx = opticDiameter / numScans  # mm distance to move horizontally each time a scan finishes

print("dev = Mach1 object")
dev = Mach1(oscPort="COM1", zaberStagePort=2)
# print("setting speed...")
# dev.setSpeed(.5) # mm/s

x = []  # x-position
y = []  # y-position
v1 = []  # voltage ch1
v2 = []  # voltage ch2

# dev.zaberStoreLocation(dev.translation["hor"], 14)
# dev.zaberStoreLocation(dev.translation["ver"], 15)

# x_loc will be used globally.
x_loc = 0

def snake(dx, dev):
	"""
	does a single vertical scan, moves over dx, does another vertical scan, ends at new position
	returns x, y, v1, v2 for first scan and then reversed x_2, y_2, v1_2, v2_2 of second scan
	"""
	# Storing locations seems finicky...
	# print("storing locations...")
	# dev.zaberStoreLocation("hor", 1)
	# dev.zaberStoreLocation("ver", 2) #different address just in case stage combines memory or something
	global x_loc

	x_array = []
	y_array = []
	v1 = []
	v2 = []
	
	# MOVE UP
	#############################################
	x_temp, y_temp, v1_temp, v2_temp = move_up()
	x_array.append(x_temp)
	y_array.append(y_temp)
	v1.append(v1_temp)
	v2.append(v2_temp)
	#############################################

	#  move horizontal
	print("Moving horizontal dx")
	print dev.zaberMove("hor", command = dev.cmd["moveRelative"], data = dx)
	# time.sleep(10)
	x_loc += dx

	# MOVE DOWN
	#############################################
	x_temp, y_temp, v1_temp, v2_temp = move_down()
	x_array.append(x_temp)
	y_array.append(y_temp)
	v1.append(v1_temp)
	v2.append(v2_temp)
	#############################################

	#  move horizontal
	print("moving horizontal dx")
	print dev.zaberMove("hor", command = dev.cmd["moveRelative"], data = dx)
	x_loc += dx

	return x_array, y_array, v1, v2

def move_up():
	"""
	Moves up the diameter of optic and takes measurement every dx
	returns x array, y array, v array
	"""
	global opticDiameter, x_loc
	x_array = []
	y_array = []
	v1 = []
	v2 = []

	total_dist = 0

	v1.append(dev.getSingleMeasurement(ch = "CH1"))
	v2.append(dev.getSingleMeasurement(ch = "CH2"))
	x_array.append(x_loc)
	y_array.append(total_dist)
	while total_dist < opticDiameter:
		print("getting and appending voltage lists")
		print("Moving vertical stage dx")
		total_dist += dx
		print(dev.zaberMove("ver", command = dev.cmd["moveRelative"], data = dx))
		# time.sleep(10)
		v1.append(dev.getSingleMeasurement(ch = "CH1"))
		v2.append(dev.getSingleMeasurement(ch = "CH2"))
		print("Appending position lists...")
		x_array.append(x_loc)
		y_array.append(total_dist)
	return x_array, y_array, v1, v2

def move_down():
	"""
	Moves down the diameter of optic and takes measurement every dx
	returns x array, y array, v array
	"""
	global opticDiameter, x_loc
	x_array = []
	y_array = []
	v1 = []
	v2 = []

	total_dist = opticDiameter
	while total_dist > 0:
		print("Appending position lists...")
		x_array.append(x_loc)
		y_array.append(total_dist)
		print("getting and appending voltage lists")
		v1.append(dev.getSingleMeasurement(ch = "CH1"))
		v2.append(dev.getSingleMeasurement(ch = "CH2"))
		print("Moving vertical stage dx")
		print dev.zaberMove("ver", command = dev.cmd["moveRelative"], data = -dx)
		# time.sleep(10)
		total_dist -= dx
	# grab last measurement
	x_array.append(x_loc)
	y_array.append(total_dist)
	v1.append(dev.getSingleMeasurement(ch = "CH1"))
	v2.append(dev.getSingleMeasurement(ch = "CH2"))

	# reverse lists so that they are oriented the same way as when moving up.
	x_array.reverse()
	y_array.reverse()
	v1.reverse()
	v2.reverse()

	return x_array, y_array, v1, v2


if __name__ == "__main__":
	traversed = 0
	while traversed < opticDiameter:
		print("Beginning snake function")
		temp_x, temp_y, temp_v1, temp_v2 = snake(dx, dev)
		traversed += 2 * dx
		print("snake finished.")
		print("Appending master lists")
		x.append(temp_x[0])
		x.append(temp_x[1])
		y.append(temp_y[0])
		y.append(temp_y[1])
		v1.append(temp_v1[0])
		v1.append(temp_v1[1])
		v2.append(temp_v2[0])
		v2.append(temp_v2[1])
		
	# print(x)
	# print(y)
	# print(v1)
	# print(v2)

	# return to starting position
	# dev.zaberMoveToStoredLocation(dev.translation["hor"], 14)
	# dev.zaberMoveToStoredLocation(dev.translation["ver"], 15)
	# print dev.zaberMove("hor", command = dev.cmd["moveRelative"], data=(-opticDiameter))

	x = np.array(x)
	y = np.array(y)
	v1 = np.array(v1)
	v2 = np.array(v2)
	vtot = v2-v1
	# Should already be in meshgrid format?
	plt.contourf(x, y, vtot)
	plt.show()