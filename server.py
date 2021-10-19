import MySocket
from server_modules import utils
import json
import socket   # https://docs.python.org/3/howto/sockets.html
import os
import threading
import signal
import sys
import configparser
import platform
import logging


os.system("clear")

MIN_PYTHON_VERSION = (3, 9)

CONFIG_FILE_PATH = "/etc/Samba_Remote/samba_remote.config"
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
		"Change_Samba_Password": utils.change_samba_password,
	}
}

class client_handler(threading.Thread):
	"""
		Handles the socket-connection with the client and runs the requested commands/actions
	"""
	def __init__(self, client_sock:MySocket, client_addr):
		threading.Thread.__init__(self)
		self.client_sock = client_sock
		self.client_addr = client_addr
		self._stop_event = threading.Event()

	def set_stop_flag(self):
		self._stop_event.set()

	def run(self):
		"""
			handles connection and command execution
		"""
		self.user = utils.linux_user()	# Stores the user_name and if the user exists on the system
		
		while not self._stop_event.is_set():	# Run untile the threads exit or a external thread has set the stop-Event
			try:
				recv_msg = str(self.client_sock.recv(), FORMAT)
			except BrokenPipeError as err:
				print("[BROKEN PIPE] Connection to the client is broken")
			except ConnectionResetError as err:
				print("[CONNECTION RESET] Connection reseted by the client")
			
			send_msg = None
			if self.client_sock.connection_closed:
				print("Connection was closed by the client")
				return
			
			recv_msg = json.loads(recv_msg)
			if not self.user.user_exists:
				self.user.check_user_exist(recv_msg["Message"]["Username"])
				if self.user.user_exists == False:
					send_msg = {
						"Message_Type": Message_Types["ServerResponse"],
						"ServerResponse": {
							"Message": f"User \"{self.user.user_name}\" does not exist or is not allowed to log in"
						}
					}
					self.client_sock.send(json.dumps(send_msg).encode(FORMAT))
					#self.client_sock.close()
					self.run()	# Give the client another time to authenticate
					return
			
			send_msg = {
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
						(returncode, command_output) = utils.change_samba_password(username, old_password, new_password)
						
						if "NT_STATUS_LOGON_FAILURE" in command_output:
							send_msg["ServerResponse"]["Message"] = "Either the Samba-Server is not running or your password/username is not correct"
						elif "NT_STATUS_CONNECTION_REFUSED" in command_output:
							send_msg["ServerResponse"]["Message"] = "Connection refused - The Server is not running"
						elif returncode != 0:
							send_msg["ServerResponse"]["Message"] = "An unknown error occured - your password didnt changed..."
						else:
							send_msg["ServerResponse"]["Message"] = f"Password successfully changed for user {username}"
					
					send_msg = json.dumps(send_msg)
					self.client_sock.send(send_msg.encode(FORMAT))	# Send a response to the client
			
			except KeyError as err:
				print("[ERROR] A required parameter/value is missing in clients-message:")
				print(err.args)
		
		self.client_sock.close()

	



PORT = 9090
SERVER_BIND_ADDRESS = ""
FORMAT = "utf-8"
ADDRESS = (SERVER_BIND_ADDRESS, PORT)    # tuple

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conf_parser = configparser.ConfigParser()
client_handler_threads = list()


def terminate_handler(signa_lnumber, stack_frame):
	"""
		the handler, if the proccess gets the signal SIGTERM
	"""
	print("Called terminate_handler")
	# Shutdown the server - dont accept new connections
	socket_server.shutdown(socket.SHUT_RDWR)
	socket_server.close()

	if len(client_handler_threads) > 0:
		print(f"Wating for {len(client_handler_threads)} clients to close connection gracefully")

	# Set for threads the stop flag
	for thread in client_handler_threads:
		thread.set_stop_flag()
	
	for thread in client_handler_threads:
		thread.join()
	print("everything is closed...exciting")
	exit(0)

terminate_handler = signal.signal(signal.SIGTERM, terminate_handler)


if __name__ == "__main__":
	# Check the version, we are running
	if sys.version_info.major < MIN_PYTHON_VERSION[0] or sys.version_info.minor < MIN_PYTHON_VERSION[1]:
		print("[ERROR] Please use a Python-Interpreter-Version higher than " + str(MIN_PYTHON_VERSION))
		exit(-1)
		
	if platform.system() != "Linux":
		print("[ERROR] This server-script supports only Linux-based systems...", file=sys.stderr)

	if os.getuid() != 0:	# Check if we run the script as root-sudo
		print("[ERROR] This script must be run as root")
		exit(-1)
	
	if not os.path.exists(CONFIG_FILE_PATH):
		print(f"[ERROR] Config-File \"{CONFIG_FILE_PATH}\" does not exist or is not readable", file=sys.stderr)
		exit(-1)
	try:
		conf_parser.read(CONFIG_FILE_PATH)
	except configparser.ParsingError as err:
		print(f"[ERROR] There was an error by parsing configFile: \"{CONFIG_FILE_PATH}\"", file=sys.stderr)
		exit(-1)

	try:
		default_settings = conf_parser["DEFAULT"]
		SERVER_BIND_ADDRESS = default_settings["ListenAddress"]
		PORT = int(default_settings["Port"])
		ADDRESS = (SERVER_BIND_ADDRESS, PORT)
	except KeyError as err:
		print("[ERROR] KeyError: " + err.args, file=sys.stderr)

	socket_server.bind(ADDRESS)
	socket_server.listen()
	print(f"[LISTENING] Server is listening at the port {PORT} for client-connections....")

	while True:
		(client_socket, client_addr) = socket_server.accept()
		client_thread = client_handler(MySocket.MySocket(client_socket), client_addr)
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

