import zmq
import base64
import serial

#Reads gyro data from IMU and streams it back to the gimbal.

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect('tcp://localhost:5555')

with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
    while(True):
        b = ser.read_until()
        yaw_pitch = str(b)
        rep=["\\r","b","'","\\n"]
        for r in rep:
            yaw_pitch=yaw_pitch.replace(r,"")

        try:
            print(yaw_pitch)
            socket.send_string(yaw_pitch)

        except KeyboardInterrupt:
            print ("Ending IMU stream.")
            break
