"""
pytektest.py
"""
from serial import Serial
from pytek import TDS3k
import matplotlib.pyplot as plt
import numpy as np

port = Serial("COM1", 9600, timeout=1)
tds = TDS3k(port)

# print(tds.identify())

# start=0, stop=0 takes 1 measurement
for i in xrange(10):
	while True:
		try:
			# tds.get_waveform takes a long time...
			waveform = tds.get_waveform(source="CH1", start=0, stop=0)
			break
		except:
			print("trying again")
	for x,y in waveform:
		print(x,y)

a = []
b = []

# for c,d in waveform:
	# print(c,d)

#for x,y in waveform:
#	a.append(x)
#	b.append(y)
	
#plt.plot(a,b)
#plt.show()