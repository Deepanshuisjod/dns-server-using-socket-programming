#!/usr/bin/env python3
import socket
from DNSmessage import DNSanswerSection
import ipaddress
SERVER, PORT = 'localhost', 2053

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Created a UDP socket for IPv4
    server.bind((SERVER, PORT))

    while True:
        data, client_address = server.recvfrom(1024)
        print(f"Connection from client: {client_address[0]}")
        print(f"Request (binary): {data}")
        int_client_address = int(ipaddress.IPv4Address(client_address[0]))
        dns_answer_instance = DNSanswerSection(TTL=60, RDATA=int_client_address, RDLENGTH=4)
        server.sendto(data + dns_answer_instance.get_values(), client_address)
