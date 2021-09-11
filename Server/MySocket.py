from os import stat
import socket

class MySocket:
	"""
		Client-Socket - socket.create_connection - connects to IPv4 and IPv6
		The socket sends the data with a header, which specifies, how big the afterwards comming message is.
		The header is obviously a constant and therefore we have a limit how much we can send at once.
	"""
	def __init__(self, client_socket:socket.socket = None):
		self.header = 2048
		if client_socket == None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = client_socket
	
	def connect(self, host:str, port:int):
		self.sock.connect((host, port))

	def recv(self) -> bytes:
		data_size = int(self.sock.recv(self.header))
		data = self.sock.recv(data_size)
		return data
	
	def send(self, data: bytes):
		data_size = len(data)
		data_size_str = str(data_size)
		data_size_bytes = bytes(data_size_str, "utf-8")

		# fill up the space we not used in the length of headers
		while len(data_size_bytes) < self.header:
			data_size_bytes = data_size_bytes + b' '
		
		self._send(data_size_bytes)
		self._send(data)

	def close(self):
		# Maybe send close to the other side
		self.sock.close()

	def shutdown(self):
		# Maybe send shutdown to the other side
		self.sock.shutdown()

	
	def _send(self, data: bytes):
		sent_bytes = 0
		data_size = len(data)
		while sent_bytes < data_size:
			sent = self.sock.send(data)
			if sent == 0:
				raise RuntimeError("Socket connection broken")
			else:
				sent_bytes = sent_bytes + sent

	def _recv(self) -> bytes:
		recv_bytes_size_str = str(self.sock.recv(self.header), "utf-8")
		recv_bytes_size = int(recv_bytes_size_str)
		recv_bytes = self.sock.recv(recv_bytes_size)

		if recv_bytes_size == 0 or recv_bytes == 0:
			raise RuntimeError("Socket connection broken")
		else:
			return recv_bytes

