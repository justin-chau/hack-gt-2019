import sys
sys.path.insert(0, '../imagezmq')

import socket
import time
import cv2
from imutils.video import VideoStream
import imagezmq
from rplidar import RPLidar

print('Connecting to webcam...')

stream = cv2.VideoCapture(4) #2

print("Connecting to lidar...")
lidar = RPLidar('/dev/ttyUSB0')
print("")
print("-------------------LiDAR-------------------")
print(lidar.get_info())
print("-------------------------------------------")
print("")
print('Connecting to headset - streaming using ZMQ...')

min_angle = 39
max_angle = 360-min_angle

# The IP address below is the IP address of the headset computer.
sender = imagezmq.ImageSender(connect_to='tcp://localhost:5556') #tcp://192.168.0.101:5556

time.sleep(2.0)
jpeg_quality = 35 #0 to 100

resolution_width = 640
resolution_height = int(0.75*resolution_width)
field_of_view = 2 *min_angle
degree_pixels = resolution_width/field_of_view

iterator = lidar.iter_scans(max_buf_meas=200)

while True:
    scan = next(iterator)

    (grabbed, frame) = stream.read()
    frame = cv2.resize(frame, (resolution_width, resolution_height))
    frame = cv2.flip( frame, -1 )

    for measurement in scan:
        angle = int(measurement[1]) + 39
        angle = angle % 360
        distance = int(measurement[2])
        
        if(angle > 0 and angle < min_angle * 2):
            if distance > 10 and distance < 500:
                print(angle)
                print (distance)
                cv2.circle(frame,(int(angle*degree_pixels),int(resolution_height/2)),int(1000/distance),(0,255,0),5)

    if not grabbed:
        break

    ret_code, jpg_buffer = cv2.imencode(
        ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    sender.send_jpg("Gimbal Camera",jpg_buffer)