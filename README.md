<p align="center">
  <img width="650" height="500" src="static/Looper.jpg">
</p>

<p align="center">
  A video looping tool for escaping those pesky online classes!
</p>

This is an app I created to help be bunk those online-classes so that I can bunk those online classes and do some other interesting stuff. It helped me a lot when the pandamic started and online-classes where mandatory :sigh:

The idea is to create a virtual webcam that you can control and send feed manually into. Your use either a feed coming from your webcam (live mode) or something you have pre-reocorded(loop/evil mode). 

## Setup

This is build on top of @jremmons awesome tool [pyfakewebcam](https://github.com/jremmons/pyfakewebcam). We have build a version on top of that to make using it easier and added a few features to help me navigate easier. 

Make sure you run the following setup to use this package.
```
# python
pip install numpy

# linux
apt-get install v4l2loopback-utils

# linux (optional)
apt-get install python-opencv # 10x performance improvement if installed (see below)
apt-get install ffmpeg # useful for debugging
```

**Note**: Currently this works best on linux since we use [v4l2loopback](https://github.com/umlaeute/v4l2loopback) to create the virtual cams. 

## Usage

This app has 5 modes
1. Live (esc) [Default] - in this mode the feed directly comes from the primary webcam and hence our virtual webcam acts just like your normal webcame.
2. Loop (l) - this model is for playing the recorded file in loop through the virtual cam. This is our evil mode ;)
3. Recording (r) - We can use this mode to record new clips that you want to loop though in the loop model. Press **r** to start recording and **esc** to stop.
4. Blank (b)- This blackens out the screen and in effect blocks the view from your webcam.
5. Freeze (f) - This take the last frame and freezes it. So you see a static feed, I don't know, maybe your net is down...

The Live mode is the default mode. You can access the other modes by pressing any of the other keys for their modes. Once your in any other mode you have to press **esc** again to get out of that mode (kinda like vims normal, insert and visual modes). 
### 1. Starting it
First of all lets get the app running. Git clone this repo and cd into the directory.

Then start a virtual camera which we will be using as our modified feed to the webcam. 

`sudo modprobe v4l2loopback devices=1 video_nr=1 card_label="HD WebCam" exclusive_caps=1`

Run to see all the Cameras. This displays all the cameras that are attached to your system. Note down them. 

`ls -l /dev | grep video`

