#!/bin/bash

# https://www.raspberrypi.com/documentation/computers/camera_software.html#rpicam-still

DATE=$(date +"%Y-%m-%d_%H%M")
rpicam-still -o /home/pi/repos/DielsiGarden/img/$DATE.jpg