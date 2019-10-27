import zmq
import base64
import serial
from rplidar import RPlidar

#Reads gyro data from IMU and streams it back to the gimbal.

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://192.168.0.100:5555')

with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
    while(True): 
        line = ser.read_until() 
        print(line)

        try:
            footage_socket.send_string(base64.b64encode(line).decode('ascii'))

        except KeyboardInterrupt:
            print ("Ending IMU stream.")
            break
