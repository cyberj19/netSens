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
    return None

def parseDHCPPacket(ts, eth):
    try:
        ip  = eth.data
        udp = ip.data
        dh  = dpkt.dhcp.DHCP(udp.data)
        src = getMACString(eth.src)
        dhcp_type = ord(getDHCPOption(dh,53))
        dhcp_fp = [ord(c) for c in getDHCPOption(dh,55)]
        hostname = getDHCPOption(dh,12)
        VCI = getDHCPOption(dh, 60)
        if dhcp_type == 1:
            description = 'dhcp discover from %s' % src
        elif dhcp_type == 3:
            req_ip = getDHCPOption(dh, 50)
            description = 'dhcp request %s from %s' % (req_ip, src)
        else:
            return None
        
        return {
            'protocol': 'dhcp',
            'layer': 7,
            'time': ts,
            'description': description,
            'source': {
                'mac': src,
                'hostname': hostname,
                'extraData': {
                    'dhcpFingerPrint': dhcp_fp,
                    'VCI': VCI
                }
            }
        }
    except Exception as e:
        return None
