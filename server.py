#!/usr/bin/env python3
import socket

SERVER , PORT = 'localhost' , 2053

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Created a UDP socket for IPv4
    server.bind((SERVER,PORT))
    data, client_address = server.recvfrom(1024) 
    request = data.decode('utf-8')
    print(f"Connection from client : {data}")
    response = "Hi from the server side !!"
    server.sendto(response.encode('utf-8'), client_address)
    