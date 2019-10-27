import sys
sys.path.insert(0, '../imagezmq')

import numpy as np
import cv2
import imagezmq

print('Connecting to gimbal video stream using ZMQ...')

image_hub = imagezmq.ImageHub(open_port='tcp://*:5556')

while True:
    msg, jpg_buffer = image_hub.recv_jpg()
    image = cv2.imdecode(np.fromstring(jpg_buffer, dtype='uint8'), -1)
    cv2.imshow(msg, cv2.resize(image,(1920,1080)))
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')