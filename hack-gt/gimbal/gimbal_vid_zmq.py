import sys
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq

import socket
import time
import cv2
from imutils.video import VideoStream
import imagezmq

stream = cv2.VideoCapture(2) 

# use either of the formats below to specifiy address of display computer
# sender = imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')
sender = imagezmq.ImageSender(connect_to='tcp://192.168.0.101:5556')

time.sleep(2.0)  # allow camera sensor to warm up
jpeg_quality = 50  # 0 to 100, higher is better quality, 95 is cv2 default
while True:  # send images as stream until Ctrl-C
    (grabbed, frame) = stream.read()

    if not grabbed:
        break

    ret_code, jpg_buffer = cv2.imencode(
        ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    sender.send_jpg("Gimbal Camera",jpg_buffer)