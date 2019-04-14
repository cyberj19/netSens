def loadDevice(dev):
	if not 'isClosed' in dev:
		dev['isClosed'] = False
	if not 'extraData' in dev:
		dev['extraData'] = {}
	return Device(dev['id'], dev['isClosed'], dev['networkId'], 
				dev['firstTimeSeen'], dev['lastTimeSeen'], 
				dev['ip'], dev['mac'], dev['vendor'], 
				dev['hits'], dev['arpHits'], dev['dhcpHits'], 
				dev['extraData'])
				
class Device:
	id			= -1
	is_closed	= False
	network_id	= -1
	first_time 	= 0
	last_time	= 0
	ip			= None
	mac			= None
	vendor		= None
	hits		= 0
	arp_hits	= 0
	dhcp_hits	= 0
	comment		= ''
	def __init__(self, id, is_closed, network_id, first_time, last_time, ip, mac, vendor, hits, arp_hits, dhcp_hits,
					extra_data={}):
		self.id = id
		self.is_closed = is_closed
		self.network_id = network_id
		self.first_time = first_time
		self.last_time = last_time
		self.ip = ip
		self.mac = mac
		self.vendor = vendor
		self.hits = hits
		self.arp_hits = arp_hits
		self.dhcp_hits = dhcp_hits
		self.extra_data = extra_data
	def serialize(self):
		return {
			'id': self.id,
			'isClosed': self.is_closed,
			'networkId': self.network_id,
			'firstTimeSeen': self.first_time,
			'lastTimeSeen': self.last_time,
			'ip': self.ip,
			'mac': self.mac,
			'vendor': self.vendor,
			'hits': self.hits,
			'arpHits': self.arp_hits,
			'dhcpHits': self.dhcp_hits,
			'extraData': self.extra_data
		}