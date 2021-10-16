#! /bin/bash

if [ $UID -ne 0 ]
then
	echo "This script must to be run as root"
	exit -1
fi

BIN_DIR="/usr/bin/Samba_Remote"
CONF_DIR="/etc/Samba_Remote"
CONF_FILE_PATH="$CONF_DIR/samba_remote.config"
SYSTEMD_SERVICE_DIR="/etc/systemd/system"
SYSTEMD_SERVICE_FILE_PATH="$SYSTEMD_SERVICE_DIR/samba_remote.service"

echo "Stoping Samba_Remote-Server"
systemctl stop samba_remote.service
systemctl disable samba_remote.service

echo "Deleting files"

rm -rfd $BIN_DIR
rm $SYSTEMD_SERVICE_FILE_PATH
rm -rfd $CONF_DIR
