from collections import OrderedDict
def loadDevice(dev):
	if not 'isClosed' in dev:
		dev['isClosed'] = False
	if not 'extraData' in dev:
		dev['extraData'] = {}
	if not 'dhcpFingerPrint' in dev:
		dev['dhcpFingerPrint'] = None
	return Device(dev['id'], dev['isClosed'], dev['networkId'], 
				dev['firstTimeSeen'], dev['lastTimeSeen'], 
				dev['ip'], dev['mac'], dev['vendor'], 
				dev['hits'], dev['arpHits'], dev['dhcpHits'], 
				dev['extraData'], dev['dhcpFingerPrint'])
				
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
					extra_data={}, dhcp_fp=None):
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
		self.dhcp_fp = dhcp_fp
		if dhcp_fp:
			self.extra_data.update({"VCI": dhcp_fp[1], "Hostname": dhcp_fp[2]})
	def serialize(self):
		dct = OrderedDict()
		dct['id'] = self.id
		dct['isClosed'] =  self.is_closed
		dct['networkId'] =  self.network_id
		dct['firstTimeSeen'] =  self.first_time
		dct['lastTimeSeen'] =  self.last_time
		dct['ip'] = self.ip
		dct['mac'] = self.mac
		dct['vendor'] = self.vendor
		dct['hits'] = self.hits
		dct['arpHits'] = self.arp_hits
		dct['dhcpHits'] = self.dhcp_hits
		dct['extraData'] = self.extra_data
		dct['dhcpFingerPrint'] = self.dhcp_fp
		return dct
