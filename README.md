# DielsiGarden

### Create a Script to Pull from GitHub and Restart Services

[update_from_github](update_from_github.sh)

Make the script executable

>chmod +x /home/pi/ota_update/update_from_github.sh
 

### Schedule the Script with a Cron Job

Open the cron table for editing:
> crontab -e


Add a cron job to run the script daily at a specific time (e.g., every day at midnight):

> S0 0 * * * /home/pi/ota_update/update_from_github.sh >> /var/log/update_from_github.log 2>&1
