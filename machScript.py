"""
machScript.py
Brian Perrett
11/12/2014
Script for moving the zaber stage and making measurements with the mach zehnder interferometer
"""
from mach1 import Mach1
import time
import numpy as np
import matplotlib.pyplot as plt
# relevant variables
print("setting variables")
opticDiameter = 50 # mm
numScans = 2 # number of scans to do across the optic
dx = opticDiameter/numScans # distance to move horizontally each time a scan finishes


print("dev = Mach1 object")
dev = Mach1(oscPort = "COM1", zaberStagePort = 2)
# print("setting speed...")
# dev.setSpeed(.5) # mm/s

x = [] # x-position
y = [] # y-position
v1 = [] # voltage ch1
v2 = [] # voltage ch2

dev.zaberStoreLocation(dev.translation["hor"], 14)
dev.zaberStoreLocation(dev.translation["ver"], 15)

def snake(diameter, dx, dev):
	"""
	does a single vertical scan, moves over dx, does another vertical scan, ends at new position
	returns x, y, v1, v2 for first scan and then reversed x_2, y_2, v1_2, v2_2 of second scan
	"""
	print("storing locations...")
	dev.zaberStoreLocation("hor", 1)
	dev.zaberStoreLocation("ver", 2) #different address just in case stage combines memory or something
	currentX = 0
	currentY = 0
	total_dist = 0
	x1 = []
	x_2 = []
	y1 = []
	y_2 = []
	v1_1 = []
	v2_1 = []
	v1_2 = []
	v2_2 = []
	
	v1_1.append(dev.getSingleMeasurement(ch = "CH1"))
	v2_1.append(dev.getSingleMeasurement(ch = "CH2"))
	while total_dist < diameter:
		print("Appending position lists...")
		x1.append(currentX)
		y1.append(currentY)
		print("getting and appending voltage lists")
		print("Moving vertical stage dx")
		print dev.zaberMove("ver", command = dev.cmd["moveRelative"], data = dx)
		# time.sleep(10)
		v1_1.append(dev.getSingleMeasurement(ch = "CH1"))
		v2_1.append(dev.getSingleMeasurement(ch = "CH2"))
		currentY += dx
		total_dist += dx
	
	print("Moving horizontal dx")
	print dev.zaberMove("hor", command = dev.cmd["moveRelative"], data = dx)
	# time.sleep(10)
	currentX += dx
	while total_dist > 0:
		print("Appending position lists...")
		x_2.append(currentX)
		y_2.append(currentY)
		print("getting and appending voltage lists")
		v1_2.append(dev.getSingleMeasurement(ch = "CH1"))
		v2_2.append(dev.getSingleMeasurement(ch = "CH2"))
		print("Moving vertical stage dx")
		print dev.zaberMove("ver", command = dev.cmd["moveRelative"], data = -dx)
		# time.sleep(10)
		total_dist -= dx
	v1_2.append(dev.getSingleMeasurement(ch = "CH1"))
	v2_2.append(dev.getSingleMeasurement(ch = "CH2"))
	# print("returning to beginning position")
	# dev.zaberMoveToStoredLocation(dev.translation["hor"], 1)
	# dev.zaberMoveToStoredLocation(dev.translation["ver"], 2)
	# dev.wait()
	print("moving horizontal 2dx")
	print dev.zaberMove("hor", command = dev.cmd["moveRelative"], data = dx)
	# time.sleep(10)
	print(y_2)
	print(v1_2)
	print(v2_2)
	y2r = []
	v1r = []
	v2r = []
	for i in reversed(y_2):
		y2r.append(i)
	for i in reversed(v1_2):
		v1r.append(i)
	for i in reversed(v2_2):
		v2r.append(i)
	return x1, y1, v1_1, v2_1, x_2, y2r, v1r, v2r

traversed = 0
while traversed < opticDiameter:
	print("Beginning snake function")
	temp_x, temp_y, temp_v1, temp_v2, temp_x_2, temp_y_2, temp_v1_2, temp_v2_2 = snake(opticDiameter, dx, dev)
	traversed += dx
	print("snake finished.")
	print("Appending master lists")
	x.append(temp_x)
	x.append(temp_x_2)
	y.append(temp_y)
	y.append(temp_y_2)
	v1.append(temp_v1)
	v1.append(temp_v1_2)
	v2.append(temp_v2)
	v2.append(temp_v2_2)
	
print(x)
print(y)
print(v1)
print(v2)

# return to starting position
# dev.zaberMoveToStoredLocation(dev.translation["hor"], 14)
# dev.zaberMoveToStoredLocation(dev.translation["ver"], 15)
print dev.zaberMove("hor", command = dev.cmd["moveRelative"], data = -opticDiameter)
x = np.array(x)
y = np.array(y)
v1 = np.array(v1)
v2 = np.array(v2)
vtot = v2-v1
# Should already be in meshgrid format?
plt.contourf(x,y,vtot)
plt.show()
