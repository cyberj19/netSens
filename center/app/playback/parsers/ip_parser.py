import dpkt
from utils import *

name = 'ip_parser'

def parseFunc(ts, eth):
    if getMACString(eth.dst) == 'FF:FF:FF:FF:FF:FF':
        return None
    if isinstance(eth.data, dpkt.ip.IP):
        return parseIPPacket(ts, eth)


def parseIPPacket(ts, eth):
    ip = eth.data
    tpa = getIPString(ip.dst)
    tha = getMACString(eth.dst)
    return {
        'protocol': 'ip',
        'layer': 3,
        'time': ts,
        'description': 'ip packet to (%s,%s)' % (tha, tpa),
        'target': {
            'ip': tpa,
            'mac': tha
        }
    }