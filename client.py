#!/usr/bin/env python3
import socket
from DNSmessage import DNSheader , DNSquestionSection

SERVER_IP, SERVER_PORT = socket.gethostbyname(socket.gethostname()), 2053

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Client side socket

dns_header_instance = DNSheader(
    id = 1234, qr = 1, opcode = 0, AA = 0, TC = 0,
    RD = 0, RA = 0, Z = 0, RCODE = 0,
    QDCOUNT = 0, ANCOUNT = 0, NSCOUNT = 0, ARCOUNT = 0
)

dns_question_instance = DNSquestionSection("google.com",1,1)

def dns_query():
    packed_dns_query = dns_header_instance.get_values() + dns_question_instance.encode_question()
    return packed_dns_query

client.sendto(dns_query(),(SERVER_IP,SERVER_PORT))

response_ = client.recvfrom(1024)
print(response_)
client.close()
