#!/bin/bash

# Variables
REPO_DIR="/home/pi/repos/DielsiGarden"

# Ensure the repository is in the correct place
if [ ! -d "$REPO_DIR" ]; then
    echo "Repository directory not found!"
    exit 1
fi

# Ensure all scripts are executable
chmod +x $REPO_DIR/scripts/*.sh

# Setup test cron jobs
CRON_JOB="* * * * * /home/pi/my-repo/scripts/update_from_github.sh" # every minute
(crontab -l 2>/dev/null | grep -v "scripts/test.sh"; echo "$CRON_JOB") | crontab -

# Setup OTA cron jobs
CRON_JOB="0 * * * * /home/pi/my-repo/scripts/update_from_github.sh" # every hour
(crontab -l 2>/dev/null | grep -v "scripts/update_from_github.sh"; echo "$CRON_JOB") | crontab -

#PYTHON_CRON_JOB="$CRON_SCHEDULE /usr/bin/python3 /home/pi/my-repo/scripts/my-python-script.py"
#(crontab -l 2>/dev/null | grep -v "my-python-script.py"; echo "$PYTHON_CRON_JOB") | crontab -


echo "Setup completed successfully."