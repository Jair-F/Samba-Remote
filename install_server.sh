#! /bin/bash

if [ $UID -ne 0 ]
then
	echo "This script must to be run as root"
	exit -1
fi

echo "Copy files"
mkdir /usr/bin/Samba_Remote

cp -R server_modules modules /usr/bin/Samba_Remote
cp server.py /usr/bin/Samba_Remote
chown -R root /usr/bin/Samba_Remote

cp default_configs/samba_remote.service /etc/systemd/system
chown root /etc/systemd/system/samba_remote.service


echo "Starting and enabling Samba_Remote service"
systemctl enable samba_remote.service
systemctl start samba_remote.service
