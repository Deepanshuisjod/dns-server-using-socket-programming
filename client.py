#!/usr/bin/env python3
import socket

SERVER_IP , SERVER_PORT = 'localhost' , 2053

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.connect((SERVER_IP,SERVER_PORT))

request = "Hii from client"
client.sendall(request.encode('utf-8'))

response = client.recv(4096).decode('utf-8')
print(response)

client.close()