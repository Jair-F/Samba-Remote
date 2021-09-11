import socket
import os

os.system("clear")

PORT = 9090
SERVER = "localhost"
ADDRESS = (SERVER, PORT)    # tuple

client_socket = socket.create_connection(ADDRESS)

user_input = str

while user_input != "exit":
	user_input = input("Eingabe: ")
	client_socket.send(bytes(user_input, "utf-8"))

print(client_socket.recv(2048).decode("utf-8"))

client_socket.close()
