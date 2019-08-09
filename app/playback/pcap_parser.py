import socket
import binascii
import dpkt
import logging
import uuid

logger = logging.getLogger('parser')
def parsePCAP(path, file):
    with open(path, 'rb') as f:
        reader = dpkt.pcap.Reader(f)
        packets = []
        packetCount = 0
        for ts, buf in reader:
            packet = None
            eth = dpkt.ethernet.Ethernet(buf)
            if hasattr(eth, 'arp'): 
                if eth.arp.op == dpkt.arp.ARP_OP_REQUEST:
                    packet = parseARPPacket(eth)
            elif isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                if isinstance(ip.data, dpkt.udp.UDP):
                    udp = ip.data
                    if udp.sport == 67 or udp.sport == 68:
                        packet = parseDHCPPacket(eth)

            if packet:
                packet['uuid'] = 'packet-%d-%s' % (int(ts), uuid.uuid4().hex)
                packet['time'] = ts
                packet['origin'] = file
                packetCount += 1
                logger.debug(packet)
                packets.append(packet)
    return packets

def getMACString(mac_addr):
        """This function accepts a 12 hex digit string and converts it to a colon
            separated string"""
        mac_addr = binascii.hexlify(mac_addr)
        s = list()
        for i in range(12/2) :  # mac_addr should always be 12 chars, we work in groups of 2 chars
                s.append( mac_addr[i*2:i*2+2] )
        r = ":".join(s)
        return r.upper()

def parseARPPacket(eth):
    arp = eth.arp
    return {
        'type': 'arp',
        'sourceDeviceIP': socket.inet_ntoa(arp.spa),
        'sourceDeviceMAC': getMACString(arp.sha),
        'targetDeviceIP': socket.inet_ntoa(arp.tpa)
    }

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
            'type': 'dhcp',
            'sourceDeviceMAC': getMACString(eth.src),
            'dhcpFingerPrint': dhcp_fp
        }
    except Exception,e:
        logger.warn(str(e))
        return None