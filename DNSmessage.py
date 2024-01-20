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
    
@dataclass
class DNSquestionSection:
    Name : str      # Domain Name which is the sequence of label
    type : int      # type is the type of record A(address) - 1, NS(name server) - 2, MX(Mail Exchange) - 3, CNAME(Cannonical/Alias Name of server) - 5 
    class_ : int    # Usually set to 1 for internet (IN)

@dataclass
class DNSanswerSection:
    NTC : DNSquestionSection
    TTL : int       # The duration in seconds a record can be cached before requerying.
    RDLENGTH : int  # Length of the RDATA field in bytes.
    RDATA: int      # IP address

@dataclass
class DNSauthoritativeSection:
    NS : str    # NS is name servers


