#!/usr/bin/env python3
import socket
from DNSmessage import DNSheader, DNSquestionSection, DNSanswerSection
import ipaddress

SERVER, PORT = socket.gethostbyname(socket.gethostname()), 2053

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Created a UDP socket for IPv4
    server.bind((SERVER, PORT))

    while True:
        data, client_address = server.recvfrom(1024)
        
        print(f"Connection from client: {client_address}")
        print(f"Request (binary): {data}")
        int_client_address = int(ipaddress.IPv4Address(client_address[0]))
        print(int_client_address)
        # Parse DNS header and question
        unpacked_header = DNSheader.parse_header(data[0:12])
        unpacked_question = DNSquestionSection.parse_question(data[12:])

        print(data[12:])
        print(unpacked_header)
        print(unpacked_question)
        
        # Create DNS header and question instances
        dns_header_instance = DNSheader(
            id=unpacked_header.id, qr=1, opcode=unpacked_header.opcode, AA=0, TC=0, RD=unpacked_header.RD,
            RA=0, Z=0, RCODE=unpacked_header.RCODE, QDCOUNT=1, ANCOUNT=1, NSCOUNT=0, ARCOUNT=0
        )
        dns_question_instance = DNSquestionSection(
            Name=unpacked_question.Name, type_=unpacked_question.type_, class_=unpacked_question.class_
        )
        dns_answer_instance = DNSanswerSection(
            Name=unpacked_question.Name, type_=1, class_=1, TTL=60, RDATA=int_client_address, RDLENGTH = 4
        )

        print(dns_header_instance.get_values())

        # Send DNS response back to the client
        server.sendto(dns_header_instance.get_values() + dns_question_instance.encode_question() + dns_answer_instance.get_values(), client_address)
