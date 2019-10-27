# hack-gt-2019
Remote FPV Gimbal with LiDAR Overlay for HackGT 2019

# Instructions for starting:

* Run headset_imu.py and headset_vid_zmq.py on the computer running the headset display.

* Run gimbal_imu.py and gimbal_vid_zmq.py on the computer running the gimbal.

* If there is difficulty accessing the Teensy through serial, run the following command: 'sudo chmod a+rw /deve/ttyACM0'.

* The gimbal_vid_stream.py and headset_vid_stream.py files are not needed and use an old uncompressed video stream.
