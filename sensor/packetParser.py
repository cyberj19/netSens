import logging 

logger = logging.getLogger('sensor')

def parse(line):
    line = line.split('|*|')
    if line[0] == 'eth:ethertype:arp':
        logger.debug('parsing arp packet')
        return arpParse(line)
    elif line[0] == 'eth:ethertype:ip:udp:bootp':
        logger.debug('parsing dhcp packet')
        return dhcpParse(line)
    else:
        raise Exception('Unknown protocol')

def arpParse(line):
    pkt = dict()
    pkt['type'] = 'arp'
    pkt['time'] = float(line[1])
    pkt['sourceDeviceMAC'] = line[2]
    pkt['sourceDeviceIP'] = line[3]
    pkt['targetDeviceIP'] = line[4]
    return pkt

def dhcpParse(line):
    pkt = dict()
    pkt['type'] = 'dhcp'
    pkt['time'] = float(line[1])
    pkt['sourceDeviceMAC'] = line[2]
    pkt['dhcpFingerPrint'] = ([ord(c) for c in line[-1]],line[-2],line[-3])
    return pkt