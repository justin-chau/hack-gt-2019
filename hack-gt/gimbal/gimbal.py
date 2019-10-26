import zmq
import base64
import serial

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:5555')

with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
    while(True): 
        line = ser.read_until() 
        print(line)

        try:
            footage_socket.send_string(base64.b64encode(line).decode('ascii'))

        except KeyboardInterrupt:
            print ("Ending IMU stream.")
            break
