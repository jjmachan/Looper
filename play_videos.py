import pyfakewebcam
import numpy as np
import time
import timeit

import cv2

cam = pyfakewebcam.FakeWebcam('/dev/video1', 1280, 720)

cam.print_capabilities()

cap = cv2.VideoCapture('../../../Music/Before.Sunset.2004.720p.BrRip.x264.YIFY.mp4')
while cap.isOpened():
    ret, frame = cap.read()

    cam.schedule_frame(frame)
    time.sleep(1/30.0)

