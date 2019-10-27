from vidgear.gears import NetGear
import cv2

options = {'flag' : 0, 'copy' : False, 'track' : False}

client = NetGear(address = '*', port = '5454', protocol = 'tcp',  pattern = 0, receive_mode = True, logging = True, **options) #Define netgear client at Server IP address.

while True:
	frame = client.recv()

	if frame is None:

		break

	cv2.imshow("Output Frame", cv2.resize(frame,(1920,1080)))

	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):

		break

cv2.destroyAllWindows()