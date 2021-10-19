import sys
import json
import MySocket
import socket

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *




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
FORMAT = "utf-8"
VERSION = 1.0
client_socket:MySocket.MySocket = None


def change_samba_password(username:str, old_password:str, new_password:str):
	"""
		return: a message wether the password was changed or an error-message
	"""
	ret_msg:str = str()
	send_msg = {
		"Message_Type": Message_Types["Command"],
		"Message": {
			"Command": Commands["Change_Samba_Password"],
			"Username": username,
			"OldPassword": old_password,
			"NewPassword": new_password
		},
		"Version": VERSION
	}
	try:
		client_socket.send(json.dumps(send_msg).encode(FORMAT))

		recv_msg = json.loads(client_socket.recv())
		ret_msg = recv_msg["ServerResponse"]["Message"]
		
	except BrokenPipeError as err:
		ret_msg = "The pipe to the Server is broken"
	except ConnectionResetError as err:
		ret_msg = "The Connection was reseted by the peer"
	except ConnectionAbortedError as err:
		ret_msg = "The Connection to the server aborted"
	except ConnectionResetError as err:
		ret_msg = "The connection was refused by the server"
	return ret_msg


class Ui_ChangePassword(QWidget):
	def __init__(self):
		super(Ui_ChangePassword, self).__init__()

	def __del__(self):
		pass
	

	def setupUi(self):
		self.setFixedSize(235, 174)
		self.setWindowTitle("Change Password")

		#self.action_input = QDialogButtonBox(self)  # Ok for change and cancel for abort
		#self.action_input.setGeometry(QRect(20, 100, 201, 32))
		#self.action_input.setOrientation(Qt.Horizontal)
		#self.action_input.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

		self.username_input = QLineEdit(self)
		self.username_input.setGeometry(QRect(110, 10, 113, 21))
		self.username_input.setEchoMode(QLineEdit.Normal)

		self.username_label = QLabel(self)
		self.username_label.setGeometry(QRect(10, 10, 71, 16))
		self.username_label.setText("Username")


		self.old_password_input = QLineEdit(self)
		self.old_password_input.setGeometry(QRect(110, 40, 113, 21))
		self.old_password_input.setEchoMode(QLineEdit.Password)

		self.old_password_label = QLabel(self)
		self.old_password_label.setGeometry(QRect(10, 40, 71, 16))
		self.old_password_label.setText("Old Password")


		self.new_password_input = QLineEdit(self)
		self.new_password_input.setGeometry(QRect(110, 70, 113, 21))
		self.new_password_input.setEchoMode(QLineEdit.Password)

		self.new_password_label = QLabel(self)
		self.new_password_label.setGeometry(QRect(10, 70, 75, 16))
		self.new_password_label.setText("New Password")


		self.retype_new_password_input = QLineEdit(self)
		self.retype_new_password_input.setGeometry(QRect(110, 100, 113, 21))
		self.retype_new_password_input.setEchoMode(QLineEdit.Password)

		self.retype_new_password_label = QLabel(self)
		self.retype_new_password_label.setGeometry(QRect(10, 100, 91, 16))
		self.retype_new_password_label.setText("Retype Password")


		self.trigger_change_password = QPushButton(self)
		self.trigger_change_password.setText("Change Password")
		self.trigger_change_password.move(20, 130)
		self.trigger_change_password.clicked.connect(self.change_password)

		self.trigger_cancel = QPushButton(self)
		self.trigger_cancel.setText("Cancel")
		self.trigger_cancel.move(140, 130)
		self.trigger_cancel.clicked.connect(lambda: self.close())

		#self.Cancel.accepted.connect(self.accept)
		#self.Cancel.rejected.connect(self.reject)

	def show_error_msg_box(self, msg:str):
		error_msg_box = QMessageBox(self)
		error_msg_box.setWindowTitle("ERROR")
		error_msg_box.setText(msg)
		error_msg_box.setIcon(QMessageBox.Warning)
		error_msg_box.addButton(QMessageBox.Ok)
		error_msg_box.show()
	
	def show_info_msg_box(self, msg:str):
		error_msg_box = QMessageBox(self)
		error_msg_box.setWindowTitle("INFO")
		error_msg_box.setText(msg)
		error_msg_box.setIcon(QMessageBox.Information)
		error_msg_box.addButton(QMessageBox.Ok)
		error_msg_box.show()

	def change_password(self):
		if self.new_password_input.text() != self.retype_new_password_input.text():
			self.show_error_msg_box("New passwords dont match!")
		elif self.username_input.text() == '':
			self.show_error_msg_box("Please enter a valid username!")
		elif self.new_password_input.text() == '' or self.retype_new_password_input.text() == '':
			self.show_error_msg_box("You are not allowed to leave the new password-field empty!")
		else:
			username = self.username_input.text()
			old_password = self.old_password_input.text()
			new_password = self.new_password_input.text()
			ret_msg = change_samba_password(username, old_password, new_password)
			self.show_info_msg_box(ret_msg)
			



class Ui_MainWindow(QMainWindow):
	def __init__(self):
		super(Ui_MainWindow, self).__init__()
		self.setupUi()

	def setupUi(self):
		self.setFixedSize(294, 151)

		self.hostname_input = QLineEdit(self)
		self.hostname_input.setGeometry(120, 10, 161, 31)
		
		self.port_input = QLineEdit(self)
		self.port_input.setGeometry(120, 50, 161, 31)

		self.connect_button = QPushButton(self)
		self.connect_button.setGeometry(150, 100, 111, 41)

		font = QFont()
		font.setPointSize(16)
		self.connect_button.setFont(font)
		self.connect_button.setCursor(QCursor(Qt.PointingHandCursor))
		self.hostname_label = QLabel(self)
		self.hostname_label.setGeometry(QRect(10, 20, 111, 16))
		self.hostname_label_2 = QLabel(self)
		self.hostname_label_2.setGeometry(QRect(10, 60, 111, 16))

		self.setWindowTitle("Samba-Remote")
		self.connect_button.setText("connect")
		self.hostname_label.setText("Hostname/Domain:")
		self.hostname_label_2.setText("Port:")

		self.status_message_label = QLabel(self)
		self.status_message_label.setGeometry(QRect(10, 130, 81, 16))
		self.status_message_label.setWordWrap(False)
		self.status_message_label.hide()

		self.connect_button.clicked.connect(lambda: self.connect())

	def show_error_msg_box(self, msg:str):
		error_msg_box = QMessageBox(self)
		error_msg_box.setWindowTitle("ERROR")
		error_msg_box.setText(msg)
		error_msg_box.setIcon(QMessageBox.Critical)
		error_msg_box.addButton(QMessageBox.Ok)
		error_msg_box.show()

	def set_default_input(self, hostname:str, port:int):
		self.hostname = hostname
		self.port = port
		self.hostname_input.setText(hostname)
		self.port_input.setText(str(port))
	
	def show_info_msg_box(self, msg:str):
		error_msg_box = QMessageBox(self)
		error_msg_box.setWindowTitle("Info")
		error_msg_box.setText(msg)
		error_msg_box.setIcon(QMessageBox.Information)
		error_msg_box.addButton(QMessageBox.Ok)
		error_msg_box.show()

	def connect(self):
		self.hostname = self.hostname_input.text()
		self.port = self.port_input.text()
		if self.hostname == '':
			self.show_error_msg_box("Hostname has to be a valid IP-Address or domain")
			return
		elif not self.port.isdigit():
			self.show_error_msg_box("Only digits are allowed as ports!")
			return
		elif self.port == '' or int(self.port) <= 0 or int(self.port) >= 65535:
			self.show_error_msg_box("Port has to be a valid port(from 1-65535)")
			return

		try:
			global client_socket
			client_socket = MySocket.MySocket.create_connection((self.hostname, self.port))
		except ConnectionRefusedError as err:
			self.show_info_msg_box("Connection was refused by the server")
			return
		except socket.gaierror as err:	# get-address-info-error
			self.show_info_msg_box("Wrong Address - Address could not be resolved")
			return
		else:
			pass
			#self.show_info_msg_box(f"Connection established to {SERVER}")
		
		self.status_message_label.setText("Connected")
		self.status_message_label.adjustSize()
		self.status_message_label.show()

		self.change_password_window = Ui_ChangePassword()
		self.change_password_window.setupUi()
		self.change_password_window.show()

