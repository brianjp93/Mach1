"""
testing to see how the tekfork.py file works

Possibly Create 1 file for zaber control, 1 file for tektronix oscilloscope control
"""
import visa
rm = visa.ResourceManager()
rm.list_resources()
