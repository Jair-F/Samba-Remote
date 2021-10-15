#! /bin/bash

if [ $UID -ne 0 ]
then
	echo "This script must to be run as root"
	exit -1
fi

echo "Stoping Samba_Remote-Server"
systemctl stop SambaRemote.service
systemctl disable SambaRemote.service

echo "Deleting files"

rm -rfd /usr/bin/Samba_Remote
rm /etc/systemd/system/samba_remote.service
