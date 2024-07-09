#!/bin/bash

REPO_URL="https://github.com/ZbindenDaniel/DielsiGarden.git"
LOCAL_DIR="/home/pi/repos/DielsiGarden"

# Updatin
sudo apt-get update && sudo apt-get upgrade -y

# Navigate to the project directory
cd $LOCAL_DIR

# Pull the latest changes from the repository
git pull $REPO_URL

echo "pull completed"