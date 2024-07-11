#!/bin/bash

LOCAL_DIR="/home/pi/repos/DielsiGarden"
exec 3>&1 1>"$LOCAL_DIR/logs/update_from_github.log" 2>&1

REPO_URL="https://github.com/ZbindenDaniel/DielsiGarden.git"
DATE=$(date +"%Y-%m-%d_%H%M")

echo $DATE " - update from github"
# Updatin
sudo apt-get update && sudo apt-get upgrade -y

# Navigate to the project directory
cd $LOCAL_DIR

# Pull the latest changes from the repository
git pull $REPO_URL

git stage logs/*
git stage img/*
echo 'fromPi '$DATE
git commit -m 'fromPi '$DATE
git push
 
echo "sync completed" >&3
