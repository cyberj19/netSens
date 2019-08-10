import dpkt
from utils import *
name = 'dhcp_parser'

def parseFunc(ts, eth):
    if isinstance(eth.data, dpkt.ip.IP):
        ip = eth.data
        if isinstance(ip.data, dpkt.udp.UDP):
            udp = ip.data
            if udp.sport == 67 or udp.sport == 68:
                return parseDHCPPacket(ts, eth)
                
def getDHCPOption(dhcp, opt_code):
    for opt in dhcp.opts:
        if opt[0] == opt_code:
            return opt[1]
def parseDHCPPacket(ts, eth):
    try:
        ip = eth.data
        udp = ip.data
        dh = dpkt.dhcp.DHCP(udp.data)
        src= getMACString(eth.src)
        dhcp_fp = [ord(c) for c in getDHCPOption(dh,55)]
        return {
            'protocol': 'dhcp',
            'layer': 7,
            'time': ts,
            'description': 'dhcp request from %s' % src,
            'source': {
                'mac': src,
                'hostname': getDHCPOption(dh, 12),
                'extraData': {
                    'dhcpFingerPrint': dhcp_fp,
                    'VCI': getDHCPOption(dh, 60)
                }
            }
        }
    except Exception:
        return None