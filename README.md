<p align="center">
  <img width="650" height="500" src="static/Looper.jpg">
</p>

<p align="center">
  A video looping tool for escaping those pesky online classes!
</p>

Start a virtual camera
`sudo modprobe v4l2loopback devices=1 video_nr=1 card_label="HD WebCam" exclusive_caps=1`

To see all the Virtual Cameras
`ls -l /dev | grep video`
