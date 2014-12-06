from mach1 import Mach1
dev = Mach1(oscPort="COM1", zaberStagePort=2)
dev.setSpeed(2) # mm/s
raw_input()
dev.setSpeed(1) # mm/s
raw_input()
dev.setSpeed(.5) # mm/s
raw_input()
dev.setSpeed(2) # mm/s