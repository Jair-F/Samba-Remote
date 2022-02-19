import sys
import json

import PySide6
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
client_socket: MySocket.MySocket = None


def change_samba_password(username: str, old_password: str, new_password: str):
    """
            return: a message wether the password was changed or an error-message
    """
    ret_msg: str = str()
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
    exit_window = Signal()
    showing_window = Signal()

    def __init__(self):
        super(Ui_ChangePassword, self).__init__()
        self.setupUi()

    def __del__(self):
        pass

    def setupUi(self):
        self.setMinimumSize(235, 174)
        self.setWindowTitle("Change Password")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        layout = QGridLayout(self)

        self.username_input = QLineEdit(self)
        self.username_input.setEchoMode(QLineEdit.Normal)
        self.username_label = QLabel(self)
        self.username_label.setText("Username")

        self.old_password_input = QLineEdit(self)
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.old_password_label = QLabel(self)
        self.old_password_label.setText("Old Password")

        self.new_password_input = QLineEdit(self)
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_label = QLabel(self)
        self.new_password_label.setText("New Password")

        self.retype_new_password_input = QLineEdit(self)
        self.retype_new_password_input.setEchoMode(QLineEdit.Password)
        self.retype_new_password_label = QLabel(self)
        self.retype_new_password_label.setText("Retype Password")

        self.trigger_change_password = QPushButton(self)
        self.trigger_change_password.setText("Change Password")
        self.trigger_change_password.clicked.connect(self.change_password)

        self.trigger_cancel = QPushButton(self)
        self.trigger_cancel.setText("Cancel")
        self.trigger_cancel.clicked.connect(lambda: self.close())
        self.trigger_cancel.clicked.connect(lambda: self.exit_window.emit())

        layout.addWidget(self.username_label, 0, 0)
        layout.addWidget(self.username_input, 0, 1)
        layout.addWidget(self.old_password_label, 1, 0)
        layout.addWidget(self.old_password_input, 1, 1)
        layout.addWidget(self.new_password_label, 2, 0)
        layout.addWidget(self.new_password_input, 2, 1)
        layout.addWidget(self.retype_new_password_label, 3, 0)
        layout.addWidget(self.retype_new_password_input, 3, 1)
        layout.addWidget(self.trigger_change_password, 4, 0)
        layout.addWidget(self.trigger_cancel, 4, 1)

        self.setLayout(layout)
        self.showing_window.emit()

    def show_error_msg_box(self, msg: str):
        error_msg_box = QMessageBox(self)
        error_msg_box.setWindowTitle("ERROR")
        error_msg_box.setText(msg)
        error_msg_box.setIcon(QMessageBox.Warning)
        error_msg_box.addButton(QMessageBox.Ok)
        error_msg_box.show()

    def show_info_msg_box(self, msg: str):
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
            self.show_error_msg_box(
                "You are not allowed to leave the new password-field empty!")
        else:
            username = self.username_input.text()
            old_password = self.old_password_input.text()
            new_password = self.new_password_input.text()
            ret_msg = change_samba_password(
                username, old_password, new_password)
            self.show_info_msg_box(ret_msg)


class Ui_MainWindow(QMainWindow):
    @Slot()
    def change_status_message_label(self):
        if self.change_password_window.isHidden() == False:
            self.status_message_label.setText("Disconnected")
        else:
            self.status_message_label.setText("Connected")

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.change_password_window = Ui_ChangePassword()
        self.change_password_window.exit_window.connect(
            self.change_status_message_label)
        self.change_password_window.showing_window.connect(
            self.change_status_message_label)
        self.setupUi()

    def setupUi(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setFixedSize(294, 151)

        layout = QGridLayout(self)

        self.hostname_input = QLineEdit(self)
        self.port_input = QLineEdit(self)
        self.connect_button = QPushButton(self)
        self.status_message_label = QLabel(self)

        font = QFont()
        font.setPointSize(16)
        self.connect_button.setFont(font)
        self.connect_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.hostname_label = QLabel(self)
        self.port_label = QLabel(self)

        self.setWindowTitle("Samba-Remote")
        self.connect_button.setText("connect")
        self.hostname_label.setText("Hostname/Domain:")
        self.port_label.setText("Port:")

        self.status_message_label.setWordWrap(False)
        self.status_message_label.setText("Disconnected")
        self.status_message_label.show()

        self.connect_button.clicked.connect(lambda: self.connect_to_server())

        layout.addWidget(self.hostname_label, 0, 0)
        layout.addWidget(self.hostname_input, 0, 1)
        layout.addWidget(self.port_label, 1, 0)
        layout.addWidget(self.port_input, 1, 1)
        layout.addWidget(self.status_message_label, 2, 0)
        layout.addWidget(self.connect_button, 2, 1)

        self.central_widget.setLayout(layout)

    def show_error_msg_box(self, msg: str):
        error_msg_box = QMessageBox(self)
        error_msg_box.setWindowTitle("ERROR")
        error_msg_box.setText(msg)
        error_msg_box.setIcon(QMessageBox.Critical)
        error_msg_box.addButton(QMessageBox.Ok)
        error_msg_box.show()

    def set_default_input(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port
        self.hostname_input.setText(hostname)
        self.port_input.setText(str(port))

    def show_info_msg_box(self, msg: str):
        error_msg_box = QMessageBox(self)
        error_msg_box.setWindowTitle("Info")
        error_msg_box.setText(msg)
        error_msg_box.setIcon(QMessageBox.Information)
        error_msg_box.addButton(QMessageBox.Ok)
        error_msg_box.show()

    def connect_to_server(self):
        self.hostname = self.hostname_input.text()
        self.port = self.port_input.text()
        if self.hostname == '':
            self.show_error_msg_box(
                "Hostname has to be a valid IP-Address or domain")
            return
        elif not self.port.isdigit():
            self.show_error_msg_box("Only digits are allowed as ports!")
            return
        elif self.port == '' or int(self.port) <= 0 or int(self.port) >= 65535:
            self.show_error_msg_box(
                "Port has to be a valid port(from 1-65535)")
            return

        try:
            global client_socket
            client_socket = MySocket.MySocket.create_connection(
                (self.hostname, self.port))
        except ConnectionRefusedError as err:
            self.show_info_msg_box("Connection was refused by the server")
            self.status_message_label.setText("Connection refused")
            return
        except socket.gaierror as err:  # get-address-info-error
            self.show_info_msg_box(
                "Wrong Address - Address could not be resolved")
            self.status_message_label.setText("Address not resolved")
            return
        else:
            # self.show_info_msg_box(f"Connection established to {SERVER}")
            self.change_password_window.showing_window.emit()

            self.change_password_window.show()
