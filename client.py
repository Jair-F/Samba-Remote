import MySocket
import socket
import sys
import os
import json
import configparser


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
FORMAT = "utf-8"
VERSION = 1.0
DEFAULT_CONFIG_FILE_PATH = "default_config.ini"



if __name__ == "__main__":
	# Check Python-Version
	if sys.version_info.major < 3:
		print("Please use Python 3 or higher", file=sys.stderr)
		exit(-1)

	if os.path.exists(DEFAULT_CONFIG_FILE_PATH):
		conf_parser = configparser.ConfigParser()
		try:
			conf_parser.read(DEFAULT_CONFIG_FILE_PATH)
		except configparser.ParsingError as err:
			print(f"Error while parsing {DEFAULT_CONFIG_FILE_PATH} - no default values: " + err.message)

		try:
			PORT = conf_parser["DEFAULT"]["Port"]
			SERVER = conf_parser["DEFAULT"]["Server"]
		except KeyError as err:
			print("KeyError: " + str(err.args))

	user_input = input(f"Server-IP/Domain[ENTER={SERVER}]: ")
	SERVER = SERVER if len(user_input) == 0 else user_input

	user_input = input(f"Server-Port[ENTER={PORT}]: ")
	PORT = PORT if len(user_input) == 0 else user_input

	ADDRESS = (SERVER, PORT)

	try:
		client_socket = MySocket.MySocket.create_connection(ADDRESS)
	except ConnectionRefusedError as err:
		print("Connection was refused by the server", file=sys.stderr)
		input("Press ENTER to exit...")
		exit(-1)
	except socket.gaierror as err:	# get-address-info-error
		print("Wrong Address - Address could not be resolved", file=sys.stderr)
		exit(-1)

	print(f"Connection established to {SERVER}")


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
	try:
		client_socket.send(json.dumps(send_msg).encode(FORMAT))

		recv_msg = json.loads(client_socket.recv())
		print(recv_msg["ServerResponse"]["Message"])

		if not client_socket.connection_closed:
			client_socket.close()
		
	except BrokenPipeError as err:
		print("The pipe to the Server is broken", file=sys.stderr)
	except ConnectionResetError as err:
		print("The Connection was reseted by the peer", file=sys.stderr)
	except ConnectionAbortedError as err:
		print("The Connection to the server aborted", file=sys.stderr)
	except ConnectionResetError as err:
		print("The connection was refused by the server", file=sys.stderr)

input("Press Enter to exit...")