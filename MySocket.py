import socket



class MySocket:
	"""
		Client-Socket - socket.create_connection - connects to IPv4 and IPv6
		The socket sends the data with a header, which specifies, how big the afterwards comming message is.
		The header is obviously a constant and therefore we have a limit how much we can send at once.
	"""
	def __init__(self, client_socket:socket.socket = None, adress_family:socket.AddressFamily = socket.AF_INET, socket_kind:socket.SocketKind = socket.SOCK_STREAM):
		self.HEADER_SIZE = 128
		self.HEADER_FORMAT = "utf-8"
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
		header = self.sock.recv(self.HEADER_SIZE)
		if header == 0:	# Check if the connection isnt brokden
			raise BrokenPipeError("Socket connection broken")
		header = int(header.decode(self.HEADER_FORMAT))

		data = self.sock.recv(header)
		if data == 0:	# Check if the connection isnt brokden
			raise BrokenPipeError("Socket connection broken")
		return data

	def send(self, data: bytes):
		"""
			Ensures, that all the bytes are sent and the header first.
		"""
		
		header = len(data)
		header_str = str(header)
		if len(header_str) > self.HEADER_SIZE:	# Check if the data we want to send is bigger than the header support
			raise OverflowError("Tried to send to big data through the websocket -> incerase the HEADER_SIZE")
		header_bytes = bytes(header_str, self.HEADER_FORMAT)

		# fill up the space we not used in the length of headers
		while len(header_bytes) < self.HEADER_SIZE:
			header_bytes = header_bytes + b' '
		
		# if I make it like this in the three lines bellow it crashes at the input from the server: "hallo wie gehts??"
		#header_bytes = bytes(str(header), self.HEADER_FORMAT)
		#header_bytes = header_bytes + b' ' * (self.HEADER_SIZE - header)
		#print(header_bytes)

		self._send(header_bytes)
		self._send(data)

	def close(self):
		# Maybe send close to the other side
		self.sock.close()

	def shutdown(self, how:int):
		# Maybe send shutdown to the other side
		self.sock.shutdown(how)

	
	def _send(self, data: bytes):
		sent_bytes = 0
		header = len(data)
		while sent_bytes < header:
			sent = self.sock.send(data)
			if sent == 0:
				raise BrokenPipeError("Socket connection broken")
			else:
				sent_bytes = sent_bytes + sent

