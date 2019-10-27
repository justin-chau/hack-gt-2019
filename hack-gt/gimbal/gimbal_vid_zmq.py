import sys
sys.path.insert(0, '../imagezmq')

import socket
import time
import cv2
from imutils.video import VideoStream
import imagezmq

print('Connecting to webcam...')

stream = cv2.VideoCapture(4)

print('Connecting to headset - streaming using ZMQ...')

# The IP address below is the IP address of the headset computer.
sender = imagezmq.ImageSender(connect_to='tcp://192.168.0.101:5556')

time.sleep(2.0)
jpeg_quality = 35 #0 to 100

while True:
    (grabbed, frame) = stream.read()

    if not grabbed:
        break

    ret_code, jpg_buffer = cv2.imencode(
        ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    sender.send_jpg("Gimbal Camera",jpg_buffer)