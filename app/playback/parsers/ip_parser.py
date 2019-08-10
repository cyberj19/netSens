import dpkt
from utils import *

name = 'ip_parser'

def parseFunc(eth):
    if getMACString(eth.dst) == 'FF:FF:FF:FF:FF:FF':
        return None
    if isinstance(eth.data, dpkt.ip.IP):
        return parseIPPacket(eth)


def parseIPPacket(eth):
    ip = eth.data
    return {
        'protocol': 'ip',
        'layer': 3,
        'targetDeviceIP': getIPString(ip.dst),
        'targetDeviceMAC': getMACString(eth.dst),
    }