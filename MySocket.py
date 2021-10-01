import socket



class MySocket:
	"""
		Client-Socket - socket.create_connection - connects to IPv4 and IPv6
		The socket sends the data with a header, which specifies, how big the afterwards comming message is.
		The header is obviously a constant and therefore we have a limit how much we can send at once.
	"""
	def __init__(self, client_socket:socket.socket = None, adress_family:socket.AddressFamily = socket.AF_INET, socket_kind:socket.SocketKind = socket.SOCK_STREAM):
		self.header = 128
		if client_socket == None:
				self.sock = socket.socket(adress_family, socket_kind)
		else:
			self.sock = client_socket

	@classmethod
	def create_connection(self, address:tuple):
		"""
			Creates a socket object and already connects only via TCPto it(IPv4 or IPv6)
		"""
		return MySocket(socket.create_connection(address))
	
	def connect(self, address:tuple):
		self.sock.connect(address)

	def recv(self) -> bytes:
		"""
			Ensures, that all the bytes, the header defines are recived.
		"""
		data_size = int(self.sock.recv(self.header))
		data = self.sock.recv(data_size)
		return data
	
	def send(self, data: bytes):
		"""
			Ensures, that all the bytes are sent and the header first.
		"""
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

	def shutdown(self, how:int):
		# Maybe send shutdown to the other side
		self.sock.shutdown(how)

	
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

