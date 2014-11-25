"""
testing to see how the tekfork.py file works

Possibly Create 1 file for zaber control, 1 file for tektronix oscilloscope control
"""
from pyvisa import visa
# rm = visa.ResourceManager()
# print(rm.list_resources())

# inst = rm.open_resource("ASRL1::INSTR")

# print(inst.query("*IDN?"))

import tekfork
data = tekfork.acquire_samples([1])