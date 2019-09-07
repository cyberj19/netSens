import dpkt
from utils import *
name = 'arp_parser'

def parseFunc(ts, eth):
    if hasattr(eth, 'arp'): 
        return parseARPPacket(ts, eth)
    else:
        return None


def parseARPPacket(ts, eth):
    arp = eth.arp
    sha = getMACString(arp.sha)
    spa = getIPString(arp.spa)
    tpa = getIPString(arp.tpa)
    return {
        'protocol': 'arp',
        'layer': 2,
        'time': ts,
        'description': 'arp request from (%s,%s) to %s' % (sha,spa,tpa),
        'source': {
            'ip': spa,
            'mac': sha
        },
        'target': {
            'ip': tpa
        }
    }