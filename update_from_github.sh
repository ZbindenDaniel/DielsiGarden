#!/bin/bash

REPO_URL="https://github.com/ZbindenDaniel/DielsiGarden.git"
LOCAL_DIR="/home/pi/repos/DielsiGarden"

# Updatin
sudo apt-get update && sudo apt-get upgrade -y

# Navigate to the project directory
cd $LOCAL_DIR

# Pull the latest changes from the repository
git pull $REPO_URL

# Restart the services
sudo systemctl restart PlanthouseHub.service
sudo systemctl restart relay_control.service
sudo systemctl restart ota_update.service

echo "Update completed and services restarted"
