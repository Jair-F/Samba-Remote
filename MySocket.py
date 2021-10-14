import socket

STATUS_CLOSE = -1

class MySocket:
	"""
		Client-Socket - socket.create_connection - connects to IPv4 and IPv6
		The socket sends the data with a header, which specifies, how big the afterwards comming message is.
		The header is obviously a constant and therefore we have a limit how much we can send at once.
	"""
	def __init__(self, client_socket:socket.socket = None, adress_family:socket.AddressFamily = socket.AF_INET, socket_kind:socket.SocketKind = socket.SOCK_STREAM):
		self.HEADER_SIZE = 128
		self.HEADER_FORMAT = "utf-8"
		self.connection_closed = True
		if client_socket == None:
				self.sock = socket.socket(adress_family, socket_kind)
		else:
			self.sock = client_socket
			self.connection_closed = False

	@classmethod
	def create_connection(self, address:tuple):
		"""
			Creates a socket object and already connects only via TCPto it(IPv4 or IPv6)
		"""
		return MySocket(socket.create_connection(address))
	
	def connect(self, address:tuple):
		self.sock.connect(address)
		self.connection_closed = False

	def recv(self) -> bytes:
		"""
			Ensures, that all the bytes, the header defines are recived.
		"""
		if self.connection_closed:
			raise BrokenPipeError("Tried to recieve but the Socket has already been closed!")

		header = self.sock.recv(self.HEADER_SIZE)
		if len(header) == 0:	# Check if the connection isnt brokden
			self.connection_closed = True
			raise BrokenPipeError("Socket connection broken")
		header = int(header.decode(self.HEADER_FORMAT))

		if header < 0:	# if we got a status_message
			if header == -1:
				self.connection_closed = True
				return bytes()	# if connection was closed, return nothing

		data = self.sock.recv(header)
		if len(data) == 0:	# Check if the connection isnt brokden
			self.connection_closed = True
			raise BrokenPipeError("Socket connection broken")
		return data

	def send(self, data: bytes):
		"""
			Ensures, that all the bytes are sent and the header first.
		"""
		if self.connection_closed:
			raise BrokenPipeError("Tried to send but the Socket has already been closed!")
		
		header = len(data)
		header_bytes = bytes(str(header), self.HEADER_FORMAT)
		if len(header_bytes) > self.HEADER_SIZE:	# Check if the data we want to send is bigger than the header support
			raise OverflowError("Tried to send to big data through the websocket -> incerase the HEADER_SIZE")

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
		"""
			Will send automaticly shutdown RW to the other side
		"""
		if not self.connection_closed:
			self._send_close_msg()	# Send close message to the other side to close the connection gracefully
		self.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def shutdown(self, how:int):
		# Maybe send shutdown to the other side
		self.sock.shutdown(how)

	def _send_close_msg(self):
		"""
			Send the other side, that we close the connection.
			the header is also a status-code if he is negative.
			For example if the header is -1 the other side has closed the connection...
		"""
		self.connection_closed = True
		self.send_status_msg(STATUS_CLOSE)
		pass

	def send_status_msg(self, status_msg:int):
		"""
			The status message will only be send in the header as negative int value - Therefore
			we will only send the header
		"""
		if status_msg >= 0:
			raise ValueError("status messages are only negative values. Passed value was: " + str(status_msg))
		
		status_msg_bytes = bytes(str(status_msg), self.HEADER_FORMAT)
		if len(status_msg_bytes) > self.HEADER_SIZE:	# Check in case of a coding error the size of the status-message
			raise OverflowError("Status message is to big for sending in the header")
		
		while len(status_msg_bytes) < self.HEADER_SIZE:
			status_msg_bytes += b' '
		
		self._send(status_msg_bytes)
	
	def _send(self, data: bytes):
		sent_bytes = 0
		bytes_to_send = len(data)
		while sent_bytes < bytes_to_send:
			sent = self.sock.send(data[sent_bytes:])
			if sent == 0:
				self.connection_closed = True
				raise BrokenPipeError("Socket connection broken")
			elif sent < 0: # Got a status-code from the other side(connection closed...)
				pass
			else:
				sent_bytes = sent_bytes + sent

