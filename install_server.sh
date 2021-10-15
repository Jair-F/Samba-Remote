#! /bin/bash

if [ $UID -ne 0 ]
then
	echo "This script must to be run as root"
	exit -1
fi

echo "Copy files"

mkdir /usr/bin/Samba_Remote

install -o root server_modules server.py modules /usr/bin/Samba_Remote
install -o root default_configs/samba_remote.service /etc/systemd/system

echo "Starting and enabling Samba_Remote service"
systemctl enable SambaRemote.service
systemctl start SambaRemote.service
