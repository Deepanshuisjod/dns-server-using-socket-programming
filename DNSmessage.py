# All communications inside of the domain protocol are carried in a singlev format called a message.
'''The top level format of message is divided
into 5 sections (some of which are empty in certain cases) shown below:

    +---------------------+
    |        Header       |
    +---------------------+
    |       Question      | the question for the name server
    +---------------------+
    |        Answer       | RRs answering the question
    +---------------------+
    |      Authority      | RRs pointing toward an authority
    +---------------------+
    |      Additional     | RRs holding additional information
    +---------------------+ '''

from dataclasses import dataclass
import struct
@dataclass
class DNSheader :
    id : int    # A random ID assignet to Query packets . A random ID assigned to query packets. Response packets must reply with the same ID. 
    qr : int    # qr is Query/Response indicator . 1 for a reply packet, 0 for a question packet. 
    opcode : int    # opcode is Operation code this specifies the kind of query in a message
    AA : int    # AA is authoritative answer . 1 if the responding server "owns" the domain queried, i.e., it's authoritative. 
    TC : int    # TC is truncation . 1 if the message is larger than 512 bytes. Always 0 in UDP responses. 
    RD : int    # RD is recursion desired . Sender sets this to 1 if the server should recursively resolve this query, 0 otherwise. 
    RA : int    # RA is recursion available . Server sets this to 1 to indicate that recursion is available. 
    Z : int     # Z is reserved . Used by DNSSEC queries. At inception, it was reserved for future use.     
    RCODE : int     # RCODE is response code . Response code indicating the status of the response. 
    QDCOUNT : int   # QDCOUNT is Question count . Number of questions in the Question section. 
    ANCOUNT : int   # ANCOUNT is Answer count . Number of records in the Answer section. 
    NSCOUNT : int   # NSCOUNT is Authority record count . Number of records in the Authority section. 
    ARCOUNT : int   # ARCOUNT is Additional record count . Number of records in the additional section.
    
    def get_values(self) -> bytes:
        flags = (self.qr << 15) | (self.opcode << 11) | (self.AA << 10) | (self.TC << 9) | (self.RD << 8) | (self.RA << 7) | (self.Z << 4) | (self.RCODE)
        packed_header =  struct.pack(">HHHHHH",self.id,flags,self.QDCOUNT,self.ANCOUNT,self.NSCOUNT,self.ARCOUNT)
        return packed_header
    
    def parse_header(recieved_header):
        id, packed_flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT = struct.unpack(">HHHHHH", recieved_header)
        qr = (packed_flags >> 15) & 0x1
        opcode = (packed_flags >> 11) & 0xF
        AA = (packed_flags >> 10) & 0x1
        TC = (packed_flags >> 9) & 0x1
        RD = (packed_flags >> 8) & 0x1
        RA = (packed_flags >> 7) & 0x1
        Z = (packed_flags >> 4) & 0x7
        RCODE = packed_flags & 0xF

        unpacked_header =  DNSheader(id = id, qr = qr, opcode = opcode, AA = AA, TC = TC, RD = RD, RA = RA, 
                         Z = Z, RCODE = RCODE, QDCOUNT = QDCOUNT, ANCOUNT = ANCOUNT, NSCOUNT = NSCOUNT, 
                         ARCOUNT = ARCOUNT) 
        return unpacked_header
@dataclass
class DNSquestionSection:
    Name : str      # Domain Name which is the sequence of label
    type_ : int      # type is the type of record A(address) - 1, NS(name server) - 2, MX(Mail Exchange) - 3, CNAME(Cannonical/Alias Name of server) - 5 
    class_ : int    # Usually set to 1 for internet (IN)

    def encode_question(self) -> bytes:
        labels = self.Name.split('.')
        encoded_labels = [bytes([len(label)]) + label.encode('utf-8') for label in labels]
        encoded_name = b''.join(encoded_labels) + b'\x00'
        type_n_class = struct.pack(">HH", self.type_, self.class_)
        return encoded_name + type_n_class

    def parse_question(data):
        label_length = data[0]
        label = data[1:1 + label_length].decode('utf-8')
        name = label + "." + data[1 + label_length:].split(b'\x00', 1)[0].decode('utf-8')
        type_, class_ = struct.unpack(">HH", data[-4:])
        unpacked_question = DNSquestionSection(Name = name , type_ = type_, class_ = class_)
        return unpacked_question

@dataclass
class DNSanswerSection:
    Name : str      # Domain Name which is the sequence of label
    type_ : int      # type is the type of record A(address) - 1, NS(name server) - 2, MX(Mail Exchange) - 3, CNAME(Cannonical/Alias Name of server) - 5 
    class_ : int    # Usually set to 1 for internet (IN)
    TTL : int       # The duration in seconds a record can be cached before requerying.
    RDLENGTH : int  # Length of the RDATA field in bytes.
    RDATA: int      # IP address

    def get_values(self):
        return struct.pack(">IHI", self.TTL, self.RDLENGTH, self.RDATA)

@dataclass
class DNSauthoritativeSection:
    NS : str    # NS is name servers


