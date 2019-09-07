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

def parsePacket(ts, eth):
    for parser in parsers:
        aspect = parser(ts, eth)
        if aspect:
            yield aspect

def parsePCAP(path, origin):
    with open(path, 'rb') as f:
        reader = dpkt.pcap.Reader(f)
        packets = []
        packetCount = 0
        for ts, buf in reader:
            eth = dpkt.ethernet.Ethernet(buf)
            packet = {
                'uuid': 'packet-%s' % uuid.uuid4().hex,
                'time': ts,
                'origin': origin,
                'protocol': None,
                'layer': -1,
                'aspects': []
            }
            for aspect in parsePacket(ts, eth):
                if aspect['layer'] > packet['layer']:
                    packet['layer'] = aspect['layer']
                    packet['protocol'] = aspect['protocol'] 
                packet['aspects'].append(aspect)
            if packet['aspects']:
                packets.append(packet)
    return packets

if __name__ == '__main__':
    inpath = sys.argv[1]
    packets = parsePCAP(inpath, 'test')
    packetsBuffer = {
        'time': time.time(),
        'origin': inpath,
        'numPackets': len(packets),
        'packets': packets
    }
    outfile = sys.argv[2]
    dmp_file = os.path.join(env.output_folder, outfile)
    with open(dmp_file, 'w+') as f:
        json.dump(packetsBuffer,f,indent=4)