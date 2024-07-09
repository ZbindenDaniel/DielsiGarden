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

# install libs
apt-get install pipx
pipx install numpy

# Setup OTA cron jobs
# CRON_JOB="1 * * * * /home/pi/my-repo/scripts/update_from_github.sh" # every hour, assuming there is a network connection
# (crontab -l 2>/dev/null | grep -v "scripts/update_from_github.sh"; echo "$CRON_JOB") | crontab -

# Setup camera job
CRON_JOB="0 5-22 * * * /usr/bin/python3 /home/pi/repos/DielsiGarden/take_image.py"
(crontab -l 2>/dev/null | grep -v "take_image.py"; echo "$CRON_JOB") | crontab -

# Setup relay job
CRON_JOB="0,15,30,45 * * * * /usr/bin/python3 /home/pi/repos/DielsiGarden/relay_control.py"
(crontab -l 2>/dev/null | grep -v "test.py"; echo "$CRON_JOB") | crontab -

# Setup test job
CRON_JOB="* * * * * /usr/bin/python3 /home/pi/repos/DielsiGarden/test.py"
(crontab -l 2>/dev/null | grep -v "test.py"; echo "$CRON_JOB") | crontab -

# Copy systemd service files to /etc/systemd/system/
cp $REPO_DIR/systemd/*.service /etc/systemd/system/

systemctl daemon-reload
systemctl enable ota_update.service
systemctl start ota_update.service
systemctl daemon-reload

echo "Setup completed successfully."