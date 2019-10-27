import zmq
import base64
import numpy as np
import serial

#Receives gyro data from the client and sends commands to the Teensy.

print('Connecting to headset using ZMQ...')
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://192.168.0.101:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, str(''))

print('Subscribing to headset IMU data...')

with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
    print('Connecting to gimbal Teensy using serial...')
    while True:
        try:
            yaw_pitch = socket.recv_string()
            print(yaw_pitch)
            ser.write(bytes(yaw_pitch, 'utf-8'))

        except KeyboardInterrupt:
            print ("Ending IMU stream connection...")
            break