# import libraries
from vidgear.gears import NetGear
import cv2

stream = cv2.VideoCapture(2)

options = {'flag' : 0, 'copy' : False, 'track' : False}

server = NetGear(address = '192.168.0.101', port = '5454', protocol = 'tcp',  pattern = 0, receive_mode = False, logging = True, **options) #Define netgear server at your system IP address.


while True:
	try: 
		(grabbed, frame) = stream.read()
		
		if not grabbed:

			break

		server.send(cv2.resize(frame, (160,120)))
	
	except KeyboardInterrupt:

		break

stream.release()
server.close()