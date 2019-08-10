import dpkt
from utils import *
name = 'dhcp_parser'

def parseFunc(eth):
    if isinstance(eth.data, dpkt.ip.IP):
        ip = eth.data
        if isinstance(ip.data, dpkt.udp.UDP):
            udp = ip.data
            if udp.sport == 67 or udp.sport == 68:
                return parseDHCPPacket(eth)
                
def getDHCPOption(dhcp, opt_code):
    for opt in dhcp.opts:
        if opt[0] == opt_code:
            return opt[1]
def parseDHCPPacket(eth):
    try:
        ip = eth.data
        udp = ip.data
        dh = dpkt.dhcp.DHCP(udp.data)
        dhcp_fp = (
            [ord(c) for c in getDHCPOption(dh,55)],
            getDHCPOption(dh,60),
            getDHCPOption(dh,12)
        )

        return {
            'protocol': 'dhcp',
            'layer': 7,
            'sourceDeviceMAC': getMACString(eth.src),
            'dhcpFingerPrint': dhcp_fp
        }
    except Exception,e:
        return None