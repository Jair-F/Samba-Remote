from MySocket import *
from utils import *
import time
import json
import socket   # https://docs.python.org/3/howto/sockets.html
import os
import threading
import signal
import subprocess
import sys
import pwd
import grp

os.system("clear")

MIN_PYTHON_VERSION = (3, 9)

CONFIG_FILE_PATH = "/etc/SambaRemote/config.config"
EXECUTABLE_PATH = "/usr/bin/SambaRemote"
SUDO_GROUP = "sudo"
VERSION = 1.0


Message_Types = {
	"Command": "Command",
	"ServerResponse": "ServerResponse",
	"Close_Connection_Message": "Close_Connection_Message"
}
Commands = {
	"Change_Samba_Password": "Change_Samba_Password",
}


message_handler = {
	"Command": {
		"Change_Samba_Password": change_samba_password,
	}
}

class linux_user:
	def __init__(self, user_name:str):
		# Check if the username exist on the system
		try:
			pwd.getpwnam(user_name)
		except KeyError as err:
			self.user_exists = False
		else:	# if no exception was raised - user exists
			self.user_exists = True
		self.user_name = user_name

class client_handler(threading.Thread):
	"""
		Handles the socket-connection with the client and runs the requested commands/actions
	"""
	def __init__(self, client_sock:MySocket, client_addr):
		threading.Thread.__init__(self)
		self.client_sock = client_sock
		self.client_addr = client_addr

	def run(self):
		"""
			handles connection and command execution
		"""
		# recieve firstly the data, the client sent
		recv_msg = str(self.client_sock.recv(), FORMAT)
		recv_msg = json.loads(recv_msg)
		send_msg = None
		self.user = linux_user(recv_msg["Message"]["Username"])
		if self.user.user_exists == False:
			send_msg = {
				"Message_Type": Message_Types["ServerResponse"],
				"ServerResponse": {
					"Message": f"User \"{self.user.user_name}\" does not exist"
				}
			}
			self.client_sock.send(json.dumps(send_msg).encode(FORMAT))
			client_socket.send(json.dumps({"Message_Type" : Message_Types["Close_Connection_Message"]}).encode(FORMAT))
			client_socket.shutdown(socket.SHUT_RDWR)
			client_socket.close()
			return	# Exit the thread - user does not exist
		
		try:
			while True:
				return_message = {
					"Message_Type": Message_Types["ServerResponse"],
					"ServerResponse": {
						
					}
				}
				try:
					if recv_msg["Message_Type"] == Message_Types["Command"]:
						if recv_msg["Message"]["Command"] == Commands["Change_Samba_Password"]:
							username = recv_msg["Message"]["Username"]
							old_password = recv_msg["Message"]["OldPassword"]
							new_password = recv_msg["Message"]["NewPassword"]

							print(f"[RUNNING COMMAND] Changing password for user {username}")

							(returncode, command_output) = change_samba_password(username, old_password, new_password)
							if "NT_STATUS_LOGON_FAILURE" in command_output:
								return_message["ServerResponse"]["Message"] = "Either the Server is not running or your password/username is not correct"
							elif "NT_STATUS_CONNECTION_REFUSED" in command_output:
								return_message["ServerResponse"]["Message"] = "Connection refused - The Server is not running"
							elif returncode != 0:
								return_message["ServerResponse"]["Message"] = "An unknown error occured - your password didnt changed..."
							else:
								return_message["ServerResponse"]["Message"] = f"Password successfully changed for user {username}"
						return_message = json.dumps(return_message)
						self.client_sock.send(return_message.encode(FORMAT))	# Send a response to the client


					elif recv_msg["Message_Type"] == Message_Types["Close_Connection_Message"]:
						print("[CONNECTION CLOSED] the connection was closed by the client.")
						self.client_sock.shutdown(socket.SHUT_RDWR)
						self.client_sock.close()
						return
				
				except KeyError as err:
					print("[ERROR] A required parameter/value is missing in clients-message:")
					print(err.args)

				# Wait for the clients next message
				recv_msg = str(self.client_sock.recv(), FORMAT)
				recv_msg = json.loads(recv_msg)

		
		except BrokenPipeError as err:
			print("[BROKEN PIPE]Connection to the client is broken")
		except ConnectionResetError as err:
			print("[CONNECTION RESET] Connection reseted by the client")
		except ConnectionError as err:
			print("[CONNECTION ERROR] " + str(err.args))
	



PORT = 9090
SERVER_BIND_ADDRESS = ""
FORMAT = "utf-8"
ADDRESS = (SERVER_BIND_ADDRESS, PORT)    # tuple

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind(ADDRESS)
socket_server.listen()

client_handler_threads = list()

def terminate_handler(signa_lnumber, stack_frame):
	"""
		the handler, if the proccess gets the signal SIGTERM
	"""
	print("Called terminate_handler")
	# Shutdown the server - dont accept new connections
	socket_server.shutdown(socket.SHUT_RDWR)
	socket_server.close()

	# Force Close all current connections
	for thread in client_handler_threads:
		pass
	print("everything is closed...exciting")
	exit(0)

terminate_handler = signal.signal(signal.SIGTERM, terminate_handler)


if __name__ == "__main__":
	# Check the version, we are running
	if sys.version_info.major < MIN_PYTHON_VERSION[0] or sys.version_info.minor < MIN_PYTHON_VERSION[1]:
		print("[ERROR] Please use a Python-Interpreter-Version higher than " + str(MIN_PYTHON_VERSION))
		exit(-1)
	
	while True:
		print(f"[LISTENING] Server is listening at the port {PORT} for client-connections....")
		(client_socket, client_addr) = socket_server.accept()
		client_thread = client_handler(MySocket(client_socket), client_addr)
		client_thread.start()
		client_handler_threads.append(client_thread)

		print(f"[NEW CONNECTION] Client {client_addr} connected to the Server")

		# Check if we have threads, which finished to run
		for thread in client_handler_threads:
			if not thread.is_alive():
				thread.join()
				client_handler_threads.remove(thread)
		
		print("Num of running threads: " + str(len(client_handler_threads)))



print("The system supports IPv6?: " + str(socket.has_ipv6))  # Has IPv6?
print("Platform supports both IPv4 and IPv6 socket stream connections: " + str(socket.has_dualstack_ipv6()))


socket_server.shutdown(socket.SHUT_RDWR)
socket_server.close()

