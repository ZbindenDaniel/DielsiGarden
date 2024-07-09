sudo systemctl daemon-reload

sudo systemctl enable ota_update.service
sudo systemctl enable relay_control.service
sudo systemctl enable PlanthouseHub.service

sudo systemctl start ota_update.service
sudo systemctl start relay_control.service
sudo systemctl start PlanthouseHub.service

sudo systemctl daemon-reload
