import binascii
import socket
def getMACString(mac_addr):
        """This function accepts a 12 hex digit string and converts it to a colon
            separated string"""
        mac_addr = binascii.hexlify(mac_addr)
        s = list()
        for i in range(12/2) :  # mac_addr should always be 12 chars, we work in groups of 2 chars
                s.append( mac_addr[i*2:i*2+2] )
        r = ":".join(s)
        return r.upper()

def getIPString(ip_addr):
    return socket.inet_ntoa(ip_addr)