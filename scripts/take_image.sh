#!/bin/bash

LOCAL_DIR="/home/pi/repos/DielsiGarden"
# exec 3>&1 1>"$LOCAL_DIR/logs/take_image.log" 2>&1

# https://www.raspberrypi.com/documentation/computers/camera_software.html#rpicam-still

DATE=$(date +"%Y-%m-%d_%H%M")
echo $Date - Taking image > $LOCAL_DIR/logs/take_image.log # >&3

rpicam-still -o $LOCAL_DIR/img/$DATE.jpg