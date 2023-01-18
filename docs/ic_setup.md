# Integrated Computer Setup

## Usage
```bash
# Update the code
cd ~/Workspace
./update_code.sh

# Reboot (everything starts at startup) or reload the daemons
sudo systemctl daemon-reload
sudo systemctl restart ic-frontend.service
sudo systemctl restart ic-backend.service
```

## Initial Setup

```bash
# Create canacompost2 user
sudo useradd canacompost2

# First, I set the canacompost2 user to automatically login

# I logged in manually, and went to the users settings panel, and changed that user so it did not require a password to login

# Then I ran the following commands as root:
cat <<EOF >/etc/lightdm/lightdm.conf.d/60-autologin.conf
[SeatDefaults]
autologin-guest=false
autologin-user=canacompost2
autologin-user-timeout=0
EOF

groupadd -r autologin
gpasswd -a canacompost2 autologin

reboot now
```

## Setting up the Jetson Nano to run the frontend and backend code

```bash
mkdir -p ~/Workspace

cat <<EOF >workstation_setup.sh
#!/bin/bash

# NOTE: requires ssh is set up with GitHub

sudo apt update -y;
sudo apt upgrade -y;

sudo apt install python3 python3-venv python3-pip source;

# Clone all required repos and pull latest master, if they're already there just pull latest master
git clone git@github.com:Canacompost-Systems-Inc/frontend.git;
git clone git@github.com:Canacompost-Systems-Inc/integrated-computer.git;
find . -type d -mindepth 1 -maxdepth 1 -exec git --git-dir={}/.git --work-tree=$PWD/{} pull origin main \;

# Setup frontend
cd frontend;
npm install;
cd ..;

# Setup backend
cd integrated-computer;
python3 -m venv venv;
source venv/bin/activate;
pip3 install -r requirements.txt;
cd ..;
EOF


cat <<'EOF' >update_code.sh
#!/bin/bash

# NOTE: requires ssh is set up with GitHub

FRONTEND_BRANCH="main";
BACKEND_BRANCH="main";

set -e;

cd frontend;
git fetch;
git checkout "${FRONTEND_BRANCH}";
git reset --hard "origin/${FRONTEND_BRANCH}";
git pull;
cd ..;

cd integrated-computer;
git fetch;
git checkout -- application/config.py;
git checkout "${BACKEND_BRANCH}";
git reset --hard "origin/${BACKEND_BRANCH}";
git pull;
cd ..;
EOF

cat <<EOF >run_backend.sh
#!/bin/bash

set -e;

cd integrated-computer;
source venv/bin/activate;
sed -i 's/TESTING = True/TESTING = False/g' application/config.py
sed -i 's/tty.usbmodem14101/ttyACM0/g' application/config.py
FLASK_ENV=development flask run --no-reload;
cd ..;
EOF

cat <<EOF >run_frontend.sh
#!/bin/bash

set -e;

cd /home/canacompost/Workspace/frontend;
npm start;
cd -;
EOF


chmod u+x run_backend.sh run_frontend.sh  update_code.sh  workstation_setup.sh;

chgrp -R canacompost2 ~/Workspace;
chmod -R g=u ~/Workspace;


./workstation_setup.sh
```

## Pio agent install for remote debugging
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3.9 python3.9-dev python3.9-distutils python3.9-venv libssl-dev libpython3.9-dev

# Get platformio after installing dependencies to make sure the headers are copied
curl -fsSL https://raw.githubusercontent.com/platformio/platformio/master/scripts/get-platformio.py --output get-platformio.py
python3.9 get-platformio.py

# Hacky shit to get around https://github.com/platformio/platformio-vscode-ide/issues/3335
sudo mkdir /snap/bin
sudo ln -s /home/canacompost/.platformio/penv/bin/platformio /snap/bin/platformio

# Generate a token if necessary
#pio account login -u canacompost -p E#X1jQYcwaoE
#pio account token

sudo bash -c 'cat <<'\''EOF'\'' >/etc/systemd/system/pioagent.service
[Unit]
Description=pio remote agent
Requires=network-online.target
After=network-online.target

[Service]
Type=simple
# change to your user of choice
Environment="PLATFORMIO_AUTH_TOKEN=mqtoqm6aqVpgnWNwk6GOnIl8pJNp15Sxm5KqXY+baHCUpIefvHPQkJ2hl9uZlqBeXG9iZpOljpuFeJ6Ua6dpr2uXqF5dc2hw"
WorkingDirectory=/home/canacompost/.platformio/penv
#ExecStart=/bin/bash -c "PATH=/home/canacompost/.platformio/penv/bin:$PATH exec /home/canacompost/.platformio/penv/bin/pio remote agent start"
ExecStart=/home/canacompost/.platformio/penv/bin/pio remote agent start
User=canacompost
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl enable pioagent.service
sudo systemctl daemon-reload
sudo systemctl start pioagent.service
```

## Setup the backend daemon
```bash
sudo bash -c 'cat <<'\''EOF'\'' >/etc/systemd/system/ic-backend.service
[Unit]
Description=Integrated Computer backend
Requires=network-online.target
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/canacompost/Workspace
ExecStart=/home/canacompost/Workspace/run_backend.sh
User=canacompost
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl enable ic-backend.service
sudo systemctl daemon-reload
sudo systemctl start ic-backend.service
```


## Setup the frontend daemon
```bash
sudo bash -c 'cat <<'\''EOF'\'' >/etc/systemd/system/ic-frontend.service
[Unit]
Description=Integrated Computer frontend
Requires=network-online.target
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/canacompost/Workspace
ExecStart=/home/canacompost/Workspace/run_frontend.sh
User=canacompost2
Environment=XAUTHORITY=/home/canacompost2/.Xauthority
Environment=DISPLAY=:0
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl enable ic-frontend.service
sudo systemctl daemon-reload
sudo systemctl start ic-frontend.service

# And also open chromium on startup
sudo bash -c 'cat <<'\''EOF'\'' >/home/canacompost2/.config/lxsession/LXDE/autostart
@lxpanel --profile LXDE
@pcmanfm --desktop --profile LXDE
@xscreensaver -no-splash
@chromium-browser --kiosk http://http://localhost:3000/
EOF'
```
