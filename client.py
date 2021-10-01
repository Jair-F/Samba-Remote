from MySocket import *
import socket
import os
import argparse

os.system("clear")


PORT = 9090
SERVER = "localhost"
ADDRESS = (SERVER, PORT)    # tuple

client_socket = MySocket.create_connection(ADDRESS)
client_socket.header = 8192

user_input = str

while True:
	recv = str(client_socket.recv(), "utf-8")
	print(recv)
	print(len(recv))
	user_input = input("Eingabe: ")
	client_socket.send(user_input.encode("utf-8"))
	if user_input == "exit":
		break



client_socket.shutdown(socket.SHUT_RDWR)
client_socket.close()
