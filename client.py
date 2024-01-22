#!/usr/bin/env python3
import socket


SERVER_IP, SERVER_PORT = 'localhost', 2053

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Client side socket

message = "Client Requests IP(IPv4)"
client.sendto(message.encode('utf-8'),(SERVER_IP,SERVER_PORT))

response_ = client.recvfrom(1024)
print(response_)
client.close()
