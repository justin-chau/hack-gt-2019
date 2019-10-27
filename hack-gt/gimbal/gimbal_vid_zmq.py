import sys
sys.path.insert(0, '../imagezmq')

import socket
import time
import cv2
from imutils.video import VideoStream
import imagezmq
from rplidar import RPLidar

print('Connecting to webcam...')

stream = cv2.VideoCapture(2)

print("Connecting to lidar...")
lidar = RPLidar('/dev/ttyUSB0')
print("-------------------LiDAR-------------------")
print(lidar.get_info())
print("-------------------------------------------")
print("")
print('Connecting to headset - streaming using ZMQ...')

min_angle = 39
max_angle = 360-min_angle

# The IP address below is the IP address of the headset computer.
sender = imagezmq.ImageSender(connect_to='tcp://192.168.0.101:5556')

time.sleep(2.0)
jpeg_quality = 35 #0 to 100

resolution_width = 640
resolution_height = int(0.75*resolution_width)
field_of_view = max_angle-min_angle
degree_pixels = resolution_width/field_of_view

distances = {}

while True:
    for i, measurement in enumerate(lidar.iter_measurments()):
        angle = int(measurement[2])
        distance = measurement[3]

        (grabbed, frame) = stream.read()
        frame = cv2.resize(frame, (resolution_width, resolution_height))

        if(angle < min_angle or angle > max_angle):
                distances[angle] = distance

        for angle in distances:
            cv2.circle(frame,(angle,int(resolution_height/2)),3,(0,255,0),5)
        
        if not grabbed:
            break

        ret_code, jpg_buffer = cv2.imencode(
            ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
        sender.send_jpg("Gimbal Camera",jpg_buffer)