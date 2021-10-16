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



echo "Copy files"
if [ ! -d "$BIN_DIR" ]; then
	mkdir "$BIN_DIR"	# Binary-Folder(Python-scripts)
fi
if [ ! -d "$CONF_DIR" ]; then
	mkdir "$CONF_DIR"		# Config-Folder
fi

# Overwrite the files if they exist...
cp -R server_modules modules $BIN_DIR
cp server.py $BIN_DIR
chown -R root $BIN_DIR

cp default_configs/samba_remote.service $SYSTEMD_SERVICE_FILE_PATH
chmod 644 $SYSTEMD_SERVICE_FILE_PATH
chown root $SYSTEMD_SERVICE_FILE_PATH

if [ -f "$CONF_FILE_PATH" ]; then
	read -p "Do you want to overwrite your config-file($CONF_FILE_PATH) with the default_config from this install script[y/n]: " USER_INPUT
	if [ "$USER_INPUT" == "y" -o "$USER_INPUT" == "Y" ]; then
		echo "Overwriting config file"
		cp default_configs/samba_remote.config CONF_FILE_PATH
		chown -R root $CONF_DIR
		chmod -R 544 $CONF_DIR
	else
		echo "Skipping copy default_config_file"
	fi
else
	echo "Copying config file"
	cp default_configs/samba_remote.config "$CONF_FILE_PATH"
	chown -R root $CONF_DIR
	chmod -R 544 $CONF_DIR
fi


echo "Starting and enabling Samba_Remote service"
systemctl enable samba_remote.service
systemctl start samba_remote.service
