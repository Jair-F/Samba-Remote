from MySocket import *
import time
import json
import socket   # https://docs.python.org/3/howto/sockets.html
import os
import threading
import signal
import subprocess
import sys
from utils import *

os.system("clear")

SAMBA_USERS_GROUP = "sambausers"
CONFIG_FILE_PATH = "/etc/SambaRemote/config.config"
EXECUTABLE_PATH = "/usr/bin/SambaRemote"
VERSION = 1.0


Message_Types = {
	"Command": "Command",
	"User_List": "User_List",
	"Open_Connection_Message": "Open_Connection_Message",
	"Close_Connection_Message": "Close_Connection_Message"
}
Commands = {
	"Change_Password": "Change_Password",
	"Reboot": "Reboot",
	"Shutdown": "Shutdown",
	"Add_User": "Add_User",
	"Delete_User": "Delete_User",
	"Update_System": "Update_System"
}
User_Types = {
	"Super_User": "SuperUser",
	"Normal_User": "Normal_User"
}


message_handler = {
	"Command": {
		"Change_Password": change_samba_password,
		"Shutdown": shutdown_system,
		"Reboot": reboot_system
	}

}

def terminate_handler():
	"""
		the handler, if the proccess gets the signal SIGTERM
	"""
	# Shutdown the connections with the clients(maybe send message, that the server will restart) and exit
	pass

user_list = get_linux_users_list()
for user in user_list:
	print(user)



class client_handler(threading.Thread):
	"""
		Handles the socket-connection with the client and runs the requested commands/actions
	"""
	def __init__(self, client_sock:MySocket, client_addr):
		self.client_sock = client_sock
		self.client_addr = client_addr

	def run(self):
		"""
			handles connection and command execution
		"""

		# open the connection and send the version
		send_msg = {}
		send_msg["MessageType"] = Message_Types["Open_Connection_Message"]
		send_msg["Version"] = VERSION
		self.client_sock.send(json.dumps(send_msg).encode(FORMAT))	# Load the message into a json-string and convert this string to a byte-sequence

		try:
			while True:
				recv_msg = str(client_socket.recv(), FORMAT)
				recv_msg = json.loads(recv_msg)
				try:
					if recv_msg["Message_Type"] == Message_Types["Command"]:
						if recv_msg["Message"]["Command"] == Commands["Change_Password"]:
							pass
						elif recv_msg["Message"]["Command"] == Commands["Add_User"]:
							pass
					elif recv_msg["Message_Type"] == Message_Types["Close_Connection_Message"]:
						print("the connection was closed by the client")
				
				except KeyError as err:
					print("Value is missing in client-message:")
					print(err.args)

		
		except BrokenPipeError as err:
			print("Connection to the client is broken")
		except...:
			print("An Unknown error occurd")




#client_handler_threads = list()





#if __name__ == "__main__":
#	while True:
#
#		# Check if we have threads, which finished to run
#		for thread in client_handler_threads:
#			if not thread.is_alive():
#				thread.join()
#				client_handler_threads.remove(thread)
#		
#
#		# if the server is closed, handle the still active clients and then exit
#		if server.server_is_running == False:
#			for thread in client_handler_threads:
#				thread.join()
#				exit()


PORT = 9090
SERVER = ""
FORMAT = "utf-8"
ADDRESS = (SERVER, PORT)    # tuple


if __name__ == "__main__":
	pass

print("The system supports IPv6?: " + str(socket.has_ipv6))  # Has IPv6?
print("Platform supports both IPv4 and IPv6 socket stream connections: " + str(socket.has_dualstack_ipv6()))

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind(ADDRESS)
socket_server.listen()



while True:
	print("Listening for client connections....")
	(client_socket, client_addr) = socket_server.accept()
	mysocket = MySocket(client_socket)

	send_data = input("Eingabe: ")
	send_data_bytes = send_data.encode("utf-8")
	mysocket.send(send_data_bytes)
	print(f"sent {len(send_data_bytes)} bytes of data")
	print("waiting for a message")
	
	recv_data = mysocket.recv()
	print(f"recived {len(recv_data)} bytes of data")
	#recv_data = recv_data.decode("utf-8")
	print(recv_data)
	if recv_data == "exit":
		mysocket.shutdown(socket.SHUT_RDWR)
		mysocket.close()
		break

socket_server.shutdown(socket.SHUT_RDWR)
socket_server.close()

