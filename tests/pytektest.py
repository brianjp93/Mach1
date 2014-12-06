"""
pytektest.py
"""
from __future__ import division
from serial import Serial
from pytek import TDS3k
import matplotlib.pyplot as plt
import numpy as np
import time

# number of points to record
rLength = 2500

port = Serial("COM1", 9600, timeout=1)
tds = TDS3k(port)

# print(tds.identify())

a = []
b = []
c = []
d = []


print tds.trigger_state()

# tds.trigger_auto([False])
# tds.acquire_single([True])

tds.send_command("ACQ:STATE", "RUN")
tds.send_command("ACQ:STOPA", "SEQ")

tds.trigger()
print tds.trigger_state()
while tds.trigger_state() != "save":
	time.sleep(.1)
	print tds.trigger_state()
waveform_acquired = False
while not waveform_acquired:
	try:
		waveform = tds.get_waveform(source="CH1", start=1, stop=rLength)
		waveform2 = tds.get_waveform(source="CH2", start=1, stop=rLength)
		waveform_acquired = True
	except:
		print("Trying again.")
# waveform2 = tds.get_waveform(source="CH2", start=1, stop=2500)
# for c,d in waveform:
	# print(c,d)

for x,y in waveform:
	a.append(x)
	b.append(y)

for x,y in waveform2:
	d.append(y)
	
# for x,y in waveform2:
	# c.append(x)
	# d.append(y)
	
x = np.linspace(0, rLength - 1, rLength)
b = np.array(b)
d = np.array(d)

print(x)
print(b)
plt.figure()
plt.plot(x, b)
# plt.plot(c,d)

plt.figure()
plt.plot(x, d)

plt.show()