import dpkt
from utils import *
name = 'arp_parser'

def parseFunc(eth):
    if hasattr(eth, 'arp'): 
        return parseARPPacket(eth)
    else:
        return None


def parseARPPacket(eth):
    arp = eth.arp
    return {
        'protocol': 'arp',
        'layer': 2,
        'sourceDeviceIP': getIPString(arp.spa),
        'sourceDeviceMAC': getMACString(arp.sha),
        'targetDeviceIP': getIPString(arp.tpa)
    }