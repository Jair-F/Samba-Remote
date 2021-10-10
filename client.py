from typing import Any
from MySocket import *
import socket
import sys
import os
import json
import argparse
import configparser
import random


os.system("clear")

Message_Types = {
	"Command": "Command",
	"ServerResponse": "ServerResponse",
	"Close_Connection_Message": "Close_Connection_Message"
}
Commands = {
	"Change_Samba_Password": "Change_Samba_Password",
}

PORT = 9090
server = input("Server-IP/Domain: ")
ADDRESS = (server, PORT)    # tuple
FORMAT = "utf-8"
VERSION = 1.0

client_socket = MySocket.create_connection(ADDRESS)
print(f"Connection established to {server}")



if __name__ == "__main__":
	print("\nChange Samba-Password")
	user_name = input("Username: ")
	old_password = input("Old password: ")
	new_password = input("New password: ")
	verify_new_password = input("Retype your new password: ")
	if new_password != verify_new_password:
		print("New Passwords doesnt match", file=sys.stderr)
		exit(0)

	send_msg = {
		"Message_Type": Message_Types["Command"],
		"Message": {
			"Command": Commands["Change_Samba_Password"],
			"Username": user_name,
			"OldPassword": old_password,
			"NewPassword": new_password
		},
		"Version": VERSION
	}
	client_socket.send(json.dumps(send_msg).encode(FORMAT))

	recv_msg = json.loads(client_socket.recv())
	print(recv_msg["ServerResponse"]["Message"])
	
	client_socket.send(json.dumps({"Message_Type" : Message_Types["Close_Connection_Message"]}).encode(FORMAT))

	client_socket.shutdown(socket.SHUT_RDWR)
	client_socket.close()
