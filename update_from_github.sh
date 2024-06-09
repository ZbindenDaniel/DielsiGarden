#!/bin/bash

REPO_URL="https://github.com/yourusername/yourrepository.git"
LOCAL_DIR="/home/pi/your_project"

# Navigate to the project directory
cd $LOCAL_DIR

# Pull the latest changes from the repository
git pull $REPO_URL

# Restart the services
sudo systemctl restart bluetooth_sensor.service
sudo systemctl restart relay_control.service

echo "Update completed and services restarted"
