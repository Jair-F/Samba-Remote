from modules import MySocket
import socket
import sys
import os
import json
import configparser

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

os.system("clear")


Message_Types = {
	"Command": "Command",
	"ServerResponse": "ServerResponse",
	"Close_Connection_Message": "Close_Connection_Message"
}
Commands = {
	"Change_Samba_Password": "Change_Samba_Password",
}

PORT = 0
SERVER = ""
ADDRESS = ()    # tuple
VERSION = 1.0
DEFAULT_CONFIG_FILE_PATH = "default_config.ini"

import Samba_Remote_GUI

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon("icon1.ico"))
	mainWindow = Samba_Remote_GUI.Ui_MainWindow()
	mainWindow.show()

	# Check Python-Version
	if sys.version_info.major < 3:
		print("Please use Python 3 or higher", file=sys.stderr)
		mainWindow.show_error_msg_box("Please use Python 3 or higher")
		exit(-1)

	if os.path.exists(DEFAULT_CONFIG_FILE_PATH):
		conf_parser = configparser.ConfigParser()
		try:
			conf_parser.read(DEFAULT_CONFIG_FILE_PATH)
		except configparser.ParsingError as err:
			print(f"Error while parsing {DEFAULT_CONFIG_FILE_PATH} - no default values: " + err.message)
			mainWindow.show_error_msg_box(f"Error while parsing {DEFAULT_CONFIG_FILE_PATH} - no default values: " + err.message)

		try:
			PORT = conf_parser["DEFAULT"]["Port"]
			SERVER = conf_parser["DEFAULT"]["Server"]
		except KeyError as err:
			print("KeyError: " + str(err.args))

	mainWindow.port = PORT
	mainWindow.hostname = SERVER

	sys.exit(app.exec())
