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

### Firewall: Configure the firewall to restrict access to essential ports.

> sudo apt-get install ufw
> sudo ufw allow 22/tcp
> sudo ufw allow 5000/tcp
> sudo ufw enable

### Backup and Recovery

Automated Backups: Set up automated backups for your configuration files and database.

> crontab -e

Add a cron job for backups:


> 0 2 * * * tar -czf /home/pi/backup/your_project_$(date +\%F).tar.gz /home/pi/your_project