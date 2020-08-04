import os

import numpy as np
import time
import cv2
import click
from pynput.keyboard import Listener, Key
import rich

from pyfakewebcam import FakeWebcam
state = 'cam_rec'

def clear():
    os.system('clear')
    print("We've got your back homie!")

def reverse():
    global state
    if state == 'cam_rec':
        state = 'cam_rt'
        print('Now Playing: Real-time video from Web Cam')
    elif state == 'cam_rt':
        state = 'cam_rec'
        print('Now Playing: Straight from File')

    else:
        state = 'cam_rec'
        print('Now Playing: Straight from File')

def change_state(key):
    global state
    clear()
    if key == Key.esc:
        reverse()
    elif hasattr(key, 'char'):
        if key.char == 'q':
            print('Bye !')
            state = 'quit'
            return False
        elif key.char == 'f':
            state = 'freeze'
            print('The video is Frozen')
        elif key.char == 'b':
            state = 'blank'
            print('Screen is set Blank')

@click.command()
@click.argument('video-file', type=click.Path())
def loop(video_file):
    global state

    clear()
    cam = FakeWebcam('/dev/video1', 640, 480)
    cam.print_capabilities()

    file_stream = cv2.VideoCapture(video_file)
    cam_stream = cv2.VideoCapture(0)
    listener = Listener(on_press=change_state)
    listener.start()
    while state !=  'quit':
        if state == 'cam_rec':
            ret, frame = file_stream.read()
            frame = cv2.resize(frame, (640, 480))
        elif state == 'cam_rt':
            ret, frame = cam_stream.read()
            frame = cv2.resize(frame, (640, 480))

        print(frame.shape)
        cam.schedule_frame(frame)
        time.sleep(1/30.0)

    print('Closing all streams...')
    file_stream.release()
    cam_stream.release()

if __name__ == '__main__':
    loop()
