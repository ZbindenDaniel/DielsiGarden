#!/bin/bash
# redirect stdout/stderr to a file
LOCAL_DIR="/home/pi/repos/DielsiGarden"

exec >$LOCAL_DIR/logs/data_sync.log 2>&1

DATE=$(date +"%Y-%m-%d_%H%M")
echo 'INFO: '+$DATE+'- connected to network. syncing data...'


REPO_URL="https://github.com/ZbindenDaniel/DielsiGarden.git"

# Navigate to the project directory
cd $LOCAL_DIR

# Pull the latest changes from the repository
git pull $REPO_URL

git stage logs/*
git stage img/*
git commit -m 'fromPi '$(date +"%Y-%m-%d_%H%M")
git push
 
echo "INFO:sync completed"