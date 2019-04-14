import logging 

logger = logging.getLogger('sensor')

def parse(line):
    line = line.split(',')
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
    pkt['sourceMAC'] = line[2]
    pkt['sourceIP'] = line[3]
    pkt['targetIP'] = line[4]
    return pkt

def dhcpParse(line):
    pkt = dict()
    pkt['type'] = 'dhcp'
    pkt['time'] = float(line[1])
    pkt['sourceMAC'] = line[2]
    return pkt