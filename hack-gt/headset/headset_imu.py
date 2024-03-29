import zmq
import base64
import serial

#Reads gyro data from IMU and streams it back to the gimbal.


print('Connecting to gimbal using ZMQ...')
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5555')

print('Publishing headset IMU data...')

with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
    print('Connecting to Arduino Nano using serial...')
    while(True):
        b = ser.read_until()
        yaw_pitch = str(b)
        rep=["\\r","b","'","\\n"]
        for r in rep:
            yaw_pitch=yaw_pitch.replace(r,"")

        try:
            # print(yaw_pitch)
            socket.send_string(yaw_pitch)

        except KeyboardInterrupt:
            print ("Ending IMU stream...")
            break
