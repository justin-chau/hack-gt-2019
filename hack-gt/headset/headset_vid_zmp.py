import sys
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq

import numpy as np
import cv2
import imagezmq

image_hub = imagezmq.ImageHub()

print('Waiting for video stream...')

while True:  # show streamed images until Ctrl-C
    msg, jpg_buffer = image_hub.recv_jpg()
    image = cv2.imdecode(np.fromstring(jpg_buffer, dtype='uint8'), -1)
    # see opencv docs for info on -1 parameter
    cv2.imshow(msg, image)  # 1 window for each RPi
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')