import socket   # https://docs.python.org/3/howto/sockets.html
import os
import threading
import signal

from linux import *

os.system("clear")


user_list = get_linux_users_list()
for user in user_list:
	print(user)


class client_handler(threading.Thread):
	"""
		Handles the socket-connection with the client and runs the requested commands/actions
	"""
	def __init__(self, client_sock, client_addr):
		self.client_sock = client_sock
		self.client_addr = client_addr

	def loop(self):
		"""
			handles connection and command execution
		"""
		pass



client_handler_threads = list()


class samba_remote_server:
	def __init__(self, address: tuple, family=socket.AF_INET):
		"""
			*address* is build like this: ("listen_address for the server - empty it should listens to all adresses", listen_port)
		"""
		self.__server = socket.create_server(address, family=family)	# ceates a TCP-socket(SOCK_STREAM)
		self.server_is_running = True
	
	def __del__(self):
		self.__server.shutdown()
		self.server_is_running = False

	def loop(self):
		"""
			This function needs to be called in the main loop - it checks of a new client wants to connect and handles it!
		"""
		(client_sock, client_addr) = self.__server.accept()
		c_handler = client_handler(client_sock, client_addr)
		
		c_handler_thread = threading.Thread(target=c_handler.loop, args=())
		
		client_handler_threads.append(c_handler_thread)
		c_handler_thread.start()



server = samba_remote_server(("", 9090))


if __name__ == "__main__":
	while True:

		# Check if we have threads, which finished to run
		for thread in client_handler_threads:
			if not thread.is_alive():
				thread.join()
				client_handler_threads.remove(thread)
		

		# if the server is closed, handle the still active clients and then exit
		if server.server_is_running == False:
			for thread in client_handler_threads:
				thread.join()
				exit()


PORT = 9090
SERVER = ""
ADDRESS = (SERVER, PORT)    # tuple


print("The system supports IPv6?: " + str(socket.has_ipv6))  # Has IPv6?
print("Platform supports both IPv4 and IPv6 socket stream connections: " + str(socket.has_dualstack_ipv6()))


"""
Same as:
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server_socket.bind(ADDRESS)
server_socket.listen()
"""
server_socket = socket.create_server(ADDRESS, family=socket.AF_INET)	# https://docs.python.org/3/library/socket.html#socket.create_server

while True:
	connection_socket, address = server_socket.accept()
	recv_data = str
	while True:
		recv_data = str(connection_socket.recv(2048), "utf-8")
		print(recv_data)
		if(recv_data == "exit"):
			break
	connection_socket.send(bytes("DISCONNECTING...", "utf-8"))
	connection_socket.close()
	if(recv_data == "quit"):
		break

server_socket.close()
