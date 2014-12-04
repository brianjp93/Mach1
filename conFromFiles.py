"""
conFromFiles.py
reads x, y, v1, and v2 array files and creates contour plots from them
"""
import numpy as np
import matplotlib.pyplot as plt


num = input("What file number would you like to plot?  (integer): ")
num = "_" + str(num) + ".txt"
print("Attempting to read data/x" + num)
print("Attempting to read data/y" + num)
print("Attempting to read data/v1" + num)
print("Attempting to read data/v2" + num)

x = []
y = []
v1 = []
v2 = []

with open("data/x" + num, "r") as f:
	for line in f:
		line = list(map(float, line.rstrip().split()))
		x.append(line)

with open("data/y" + num, "r") as f:
	for line in f:
		line = list(map(float, line.rstrip().split()))
		y.append(line)

with open("data/v1" + num, "r") as f:
	for line in f:
		line = list(map(float, line.rstrip().split()))
		v1.append(line)

with open("data/v2" + num, "r") as f:
	for line in f:
		line = list(map(float, line.rstrip().split()))
		v2.append(line)

x = np.array(x)
# debug by seeing what x_array looks like.  Was appending strings on accident.  Changed to float.
# print(x)
y = np.array(y)
v1 = np.array(v1)
v2 = np.array(v2)
vtot = v2 - v1

# Should already be in meshgrid format?
plt.contourf(x, y, vtot)
plt.show()