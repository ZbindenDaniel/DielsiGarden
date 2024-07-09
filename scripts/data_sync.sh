#!/bin/bash

echo 'connected to network syncing data...'

REPO_URL="https://github.com/ZbindenDaniel/DielsiGarden.git"
LOCAL_DIR="/home/pi/repos/DielsiGarden"

# Navigate to the project directory
cd $LOCAL_DIR

# Pull the latest changes from the repository
git pull $REPO_URL

git stage logs/*
git stage img/*
msg='fromPi '$(date +"%Y-%m-%d_%H%M")
git commit -m $msg
git push
 
echo "sync completed"