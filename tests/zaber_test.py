import serial, struct, time, glob, sys

def send(device, command, data=0):
   # send a packet using the specified device number, command number, and data
   # The data argument is optional and defaults to zero
   packet = struct.pack('<BBl', device, command, data)
   ser.write(packet)
   
def receive():
   # return 6 bytes from the receive buffer
   # there must be 6 bytes to receive (no error checking)
   r = [0,0,0,0,0,0]
   for i in range (6):
       r[i] = ord(ser.read(1))
   return r

cmd = {"home": 1, "move absolute": 20, "move relative": 21}
stage = {"vertical": 0, "horizontal": 1}
   
if __name__ == "__main__":

	ser = serial.Serial(2)
	print ("You are connected to " + ser.name)

	device = stage["horizontal"]
	command = cmd["move relative"] 
	data = 500000
	
	send(device, command, data)
	
	r = receive()
	print("receive data: " + str(r))

	ser.close()