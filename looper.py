import os

import numpy as np
import time
import cv2
import click
from pynput.keyboard import Listener, Key
from rich.console import Console

from pyfakewebcam import FakeWebcam
console = Console()


class LooperState():
    def __init__(self, default_state='live', video_loaded=False):
        self.default_state = default_state
        self.cur_state = self.default_state
        self.prev_state = ''
        self.quit = False
        self.available_states = ['live', 'recording', 'loop', 'quit'
                                 'frozen', 'blank']
        self.video_loaded = video_loaded
        self.status_board()

    def change_state(self, key):
        if hasattr(key, 'char') and self.cur_state == 'live':
            if key.char == 'q':
                self.quit = True
            elif key.char == 'f':
                self.prev_state = self.cur_state
                self.cur_state = 'frozen'
            elif key.char == 'b':
                self.prev_state = self.cur_state
                self.cur_state = 'blank'
            elif key.char == 'l':
                self.prev_state = self.cur_state
                self.cur_state = 'loop'
            elif key.char == 'r':
                self.prev_state = self.cur_state
                self.cur_state = 'recording'
            self.status_board()

        elif key == Key.esc:
            self.cur_state = self.default_state
            self.status_board()

    def status_board(self):
        os.system('clear')
        console.print('[red] LOOPER')
        color = 'green'
        if self.cur_state in ['live']:
            color = 'red'
        console.print('Status: [{color}]{state}\t'
                .format(state=self.cur_state.upper(), color=color))
        if not self.video_loaded:
            console.print('Press [bold]r[/bold] to start recording and press [bold]q[/bold] once done')


def setup_file_stream(path, vid_file=None):
    if vid_file is None:
        return False

    video_file = os.path.join(path, vid_file)
    assert os.path.exists(video_file)
    print('opening: ', video_file)
    file_stream = cv2.VideoCapture(video_file)
    return file_stream


def setup_cam_stream(cam_num):
    cam_stream = cv2.VideoCapture(cam_num)
    return cam_stream


def setup_recording(vid_path=None):
    assert os.path.exists(vid_path)

    # make file format
    t = time.gmtime()
    vid_file = f"{t.tm_year}.{t.tm_mon}.{t.tm_mday}:{t.tm_hour}.{t.tm_min}.avi"
    video_file = os.path.join(vid_path, vid_file)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_file, fourcc, 20.0, (640, 480))
    return out, vid_file


def loop(vid_file=None, vid_path='./videos/'):
    state = LooperState(video_loaded=True)
    cam = FakeWebcam('/dev/video2', 640, 480)
    cam.print_capabilities()

    cam_stream = setup_cam_stream(1)
    # out_stream, vid_file = setup_recording(vid_path)
    file_stream = setup_file_stream(vid_path, vid_file)

    listener = Listener(on_press=state.change_state)
    listener.start()

    while not state.quit:
        if state.cur_state == 'loop':
            ret, frame = file_stream.read()
            if ret:
                frame = cv2.resize(frame, (640, 480))
            else:
                file_stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
        elif state.cur_state == 'live':
            ret, frame = cam_stream.read()
            frame = cv2.resize(frame, (640, 480))

        elif state.cur_state == 'blank':
            frame = np.zeros([480, 640, 3], np.uint8)

        elif state.cur_state == 'frozen':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        elif state.cur_state == 'recording':
            ret, frame = cam_stream.read()
            frame = cv2.resize(frame, (640, 480))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cam.schedule_frame(frame)
        time.sleep(1/30.0)

    print('Closing all streams...')
    file_stream.release()
    cam_stream.release()
    listener.stop()
    listener.join()




def setup_looper():
    default_vid = './videos/'
    console.rule('[red]Welcome to Looper')
    console.print('press [bold]Enter[/bold] to accept default')
    user_vid = console.input(
            f'Directory to save recoded videos [green]({default_vid}): ')
    if not user_vid:
        user_vid = default_vid
    #TODO: add setup for cameras


def startup():
    startup_state = LooperState()

    listener = Listener(on_press=startup_state.change_state)
    listener.start()

    vid_path = './videos/'
    cam_stream = setup_cam_stream(1)
    out_stream, vid_file = setup_recording(vid_path)
    cam = FakeWebcam('/dev/video2', 640, 480)

    while startup_state.prev_state != 'recording':
        if startup_state.cur_state == 'recording':
            ret, frame = cam_stream.read()
            frame = cv2.resize(frame, (640, 480))
            out_stream.write(frame)

        # quit if q is pressed
        elif startup_state.quit:
            break

        else:
            startup_state.cur_state == 'live'
            ret, frame = cam_stream.read()
            frame = cv2.resize(frame, (640, 480))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cam.schedule_frame(frame)
        time.sleep(1/30.0)

    cam_stream.release()
    out_stream.release()
    listener.stop()
    listener.join()

    return vid_file


if __name__ == '__main__':
    vid_file = startup()
    loop(vid_file)
