"""
machScript.py
Brian Perrett
11/12/2014
Script for moving the zaber stage and making measurements with the mach zehnder interferometer
"""
import mach1
# relevant variables

opticDiameter = 0 # mm
numScans = 0 # number of scans to do across the optic
dx = opticDiameter/numScans # distance to move horizontally each time a scan finishes

dev = mach1.Mach1(oscPort = "COM1", zaberStagePort = 2)

x = [] # x-position
y = [] # y-position
v1 = [] # voltage ch1
v2 = [] # voltage ch2

def snake(diameter, dx, dev):
	"""
	does a single vertical scan, moves over dx, does another vertical scan, ends at new position
	returns x, y, v1, v2 for first scan and then reversed x_2, y_2, v1_2, v2_2 of second scan
	"""
	startX = # get current x value
	startY = # get current y value
	currentX = startX
	currentY = startY
	total_dist = 0
	x = []
	x_2 = []
	y = []
	y_2 = []
	v1 = []
	v1_2 = []
	v2 = []
	v2_2 = []
	while total_dist < diameter:
		x.append(startX)
		y.append(currentY)
		v1.append(dev.getSingleMeasurement(ch = "CH1"))
		v2.append(dev.getSingleMeasurement(ch = "CH2"))
		dev.zaberMove("ver", command = dev.cmd["moveRelative"], data = dx)
		currentY = startY + dx
		total_dist += dx

	dev.zaberMove("hor", command = dev.cmd["moveRelative"], data = dx)
	currentX = startX + dx
	while total_dist > 0:
		x_2.append(currentX)
		y_2.append(currentY)
		v1_2.append(dev.getSingleMeasurement(ch = "CH1"))
		v2_2.append(dev.getSingleMeasurement(ch = "CH2"))
		dev.zaberMove("ver", command = dev.cmd["moveRelative"], data = -dx)
		total_dist -= dx

	dev.zaberMove("hor", command = dev.cmd["moveAbsolute"], data = StartX)
	dev.zaberMove("ver", command = dev.cmd["moveAbsolute"], data = StartY)

	# ready to recall function
	dev.zaberMove("hor", command = dev.cmd["moveRelative"], data = 2*dx)
	y_2 = reversed(y_2)
	v1_2 = reversed(v1_2)
	v2_2 = reversed(v2_2)
	return x, y, v1, v2, x_2, y_2, v1_2, v2_2

traversed = 0
while traversed < opticDiameter:
	temp_x, temp_y, temp_v1, temp_v2, temp_x_2, temp_y_2, temp_v1_2, temp_v2_2 = snake(opticDiameter, dx, dev)
	x.append(temp_x)
	x.append(temp_x_2)
	y.append(temp_y)
	y.append(temp_y_2)
	v1.append(temp_v1)
	v1.append(temp_v1_2)
	v2.append(temp_v2)
	v2.append(temp_v2_2)
	