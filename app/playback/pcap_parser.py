import socket
import binascii
import dpkt
import logging
import uuid
import sys
import json
import os
import env
import time
from parsers import parsers

logger = logging.getLogger('parser')

def parsePacket(eth):
    for parser in parsers:
        aspect = parser(eth)
        if aspect:
            yield aspect

def parsePCAP(path, file):
    with open(path, 'rb') as f:
        reader = dpkt.pcap.Reader(f)
        packets = []
        packetCount = 0
        for ts, buf in reader:
            eth = dpkt.ethernet.Ethernet(buf)
            packet = {
                'uuid': 'packet-%s' % uuid.uuid4().hex,
                'time': ts,
                'origin': file,
                'protocol': None,
                'aspects': []
            }
            highest_layer = -1
            for aspect in parsePacket(eth):
                if aspect['layer'] > highest_layer:
                    highest_layer = aspect['layer']
                    packet['protocol'] = aspect['protocol'] 
                packet['aspects'].append(aspect)
            if packet['aspects']:
                packets.append(packet)
    return packets

if __name__ == '__main__':
    path = sys.argv[1]
    packets = parsePCAP(path, 'test')
    packetsBuffer = {
        'time': time.time(),
        'origin': path,
        'numPackets': len(packets),
        'packets': packets
    }
    dmp_file = os.path.join(env.output_folder, 'pb-test.json')
    with open(dmp_file, 'w') as f:
        json.dump(packetsBuffer,f,indent=4)