#!/usr/bin/env python3
import socket
from DNSmessage import DNSheader, DNSquestionSection, DNSanswerSection
import ipaddress
SERVER, PORT = 'localhost', 2053

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Created a UDP socket for IPv4
    server.bind((SERVER, PORT))

    while True:
        data, client_address = server.recvfrom(1024)

        dns_header_instance = DNSheader(
            id = 1234, qr = 1, opcode = 0, AA = 0, TC = 0,
            RD = 0, RA = 0, Z = 0, RCODE = 0,
            QDCOUNT = 0, ANCOUNT = 0, NSCOUNT = 0, ARCOUNT = 0
        )

        dns_question_instance = DNSquestionSection("google.com",1,1)
        
        print(f"Connection from client: {client_address}")
        print(f"Request (binary): {data}")
        
        int_client_address = int(ipaddress.IPv4Address(client_address[0]))
        dns_answer_instance = DNSanswerSection(Name = "google.com", type = 1, class_ = 1, TTL = 60, RDATA = int_client_address, RDLENGTH = 4)

        parsed_header = DNSheader.parse_header(dns_header_instance.get_values())
        parsed_question = DNSquestionSection.parse_question(dns_question_instance.domain_name()+dns_question_instance.type_class_())
        dns_header_instance = DNSheader(id = parsed_header.id, qr = 1,
                                        opcode = parsed_header.opcode, AA = 0,
                                        TC = 0, RD = parsed_header.RD,
                                        RA = 0, Z = 0,
                                        RCODE = parsed_header.RCODE, QDCOUNT = 1,
                                        ANCOUNT = 1, NSCOUNT = 0,
                                        ARCOUNT = 0)
        
        server.sendto(dns_header_instance.get_values() + dns_question_instance.domain_name() + dns_question_instance.type_class_() + dns_answer_instance.get_values(), client_address)
