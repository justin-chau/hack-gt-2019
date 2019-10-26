import zmq
import base64
import numpy as np

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, str(''))

while True:
    try:
        frame = footage_socket.recv_string()
        line = base64.b64decode(frame)
        print(line)

    except KeyboardInterrupt:
        print ("Ending connection...")
        break