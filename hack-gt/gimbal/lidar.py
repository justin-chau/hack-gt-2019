import sys
import cv2
from rplidar import RPLidar


print("Connecting to camera...")
cam = cv2.VideoCapture(5)

PORT_NAME = '/dev/ttyUSB0'

print("Connecting to lidar...")
lidar = RPLidar(PORT_NAME)
print(lidar.get_info())

resolution_width = 640
resolution_height = int(0.75*resolution_width)
min_angle = 39
max_angle = 360-min_angle
field_of_view = max_angle-min_angle
degree_pixels = resolution_width/field_of_view

distances = {}

while True:
    for i, measurement in enumerate(lidar.iter_measurments()):
        

        angle = int(measurement[2])
        distance = measurement[3]
        print(distance)
        try:
            ret_val, frame = cam.read()
            frame = cv2.resize(frame, (resolution_width, resolution_height))

            if(angle < min_angle or angle > max_angle):
                distances[angle] = distance

            for angle in distances:
                cv2.circle(frame,(angle,int(resolution_height/2)),3,(0,255,0),5)
                cv2.imshow('frame', frame)

                cv2.waitKey(1)


        except KeyboardInterrupt:
            cam.release()
            cv2.destroyAllWindows()
            print('Stoping.')
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()


