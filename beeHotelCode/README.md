# BeeHotelMonitoring Project

Object: The object of this project is to monitor solitary bee activity in and out of bee hotels

# Manual

## 1. Download Source Code into your desktop
cd ~/Desktop
git clone https://github.com/eai6/BeeHotelMonitoring.git
cd beHotelCode

## 2. Install dependancies using terminal
### Install picamera
sudo apt install -y python3-picamera2
### Install opencv
sudo apt install python3-opencv

## 3. Create program directories
python3 makeDirectories.py

## 4. RunFocus to check and focus camera
python3 runFocus.py

## 5. Set-up a service to run driver for monitoring
### Create Service file
sudo nano /lib/systemd/system/beeHotelRecord.service 


### Paste the code below

'''
[Unit]
Description=beeHotel
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/apis/Desktop/beeHotelCode/driver.py
Restart=always

[Install]
WantedBy=multi-user.target
'''

### Update Deamon
sudo systemctl daemon-reload

## 6. Test BeeHotelMonitoring Service

### Start the beeHotelMonitoring Service
sudo systemctl start beeHotelRecord.service
### Check status of service
sudo systemctl status beeHotelRecord.service
### Command to stop service
sudo systemctl stop beeHotelRecord.service


## 7. Enable BeeHotelMonitoring Service on boot
sudo systemctl enable beeHotelRecord.service

## 8. Set-up WittyPi

### Get WittyPi
wget http://uugear.com/repo/WittyPi3/install.sh
sudo sh install.sh

### Set the recorder to launch at startup
Open /home/apis/wittypi/afterStartup.sh In Geany
Add the following:
sudo python /home/apis/Desktop/beeHotelCode/driver.py


### Test the WittyPi through 1 cycle
Open terminal 
cd wittypi/
sudo ./wittyPi.sh

Schedule next startup (5): suggest something relatively soon like ?? ??:01:00 (one minute past the next hour. Change the minute to something reasonable)

Schedule next shutdown (6): suggest something 60 seconds before the startup like ?? ??:00 (at the next hour)

Wait for Pi to shutdown and restart 60 seconds later

### Set up actual WP script

Make a new file w/ Geany and paste the following:

BEGIN 2024-04-01 07:50:00
END   2024-09-01 00:00:00
ON    H10 M15 # will start recording from 7:50am to 6:05pm
OFF   H13 M45 # will be will be off until the next day

Save this as /home/apis/wittypi/schedules/beeHotel_2023.wpi 

### Select custom WittyPi Schedule
cd wittypi/
sudo ./wittyPi.sh
Choose schedule script (6)
Pick the beeHotel script
Verify that the next power on/off times make sense

