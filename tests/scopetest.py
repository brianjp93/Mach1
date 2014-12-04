# scopetest.py

from PyTektronixScope import PyTektronixScope
from PyTektronixScope.VisaList import VisaObjectList
from pyvisa import visa
import numpy as np
import matplotlib.pyplot as plt

# idk wth this is doing.  not helping, that's for sure
# print(VisaObjectList())

inst_list = visa.get_instruments_list()
print(inst_list)

rLength = 10
dev = PyTektronixScope.TektronixScope("COM1")
y = dev.read_data_one_channel(channel=1, data_start=1, data_stop=rLength, x_axis_out=False, t0=None, DeltaT=None, booster=False)
print(y)

x = np.linspace(1, rLength)
y = np.array(y)

plt.plot(x, y)
plt.show()