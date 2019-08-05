from collections import OrderedDict
class Packet(object):
	id 				= -1
	time			= 0
	type 			= ''
	source_guid		= ''
	network_id		= -1
	def __init__(self, id, time, type, source_guid, network_id):
		self.id = id
		self.time = time
		self.type = type
		self.source_guid = source_guid
		self.network_id = network_id
		
	def serialize(self):
		dct = OrderedDict()
		dct['id'] = self.id
		dct['time'] = self.time
		dct['type'] = self.type
		dct['sourceGUID'] = self.source_guid
		dct['networkId'] = self.network_id
		return dct

		
class ARPPacket(Packet):
	source_device_id 	= -1
	source_device_ip			= ''
	source_device_mac			= ''
	target_device_id	= -1
	target_device_ip			= ''
	
	def __init__(self, id, time, source_guid, network_id, source_device_id,
				source_device_ip, source_device_mac, target_device_id, target_device_ip):
		super(ARPPacket, self).__init__(id, time, 'arp', source_guid, network_id)
		self.source_device_id = source_device_id
		self.source_device_ip = source_device_ip
		self.source_device_mac = source_device_mac
		self.target_device_id = target_device_id
		self.target_device_ip = target_device_ip
	
	def update_match(self, network_id, source_device_id, target_device_id):
		self.network_id = network_id
		self.source_device_id = source_device_id
		self.target_device_id = target_device_id
		
	def serialize(self):
		packet = super(ARPPacket, self).serialize()
		packet['sourceDeviceId'] = self.source_device_id
		packet['sourceDeviceIP'] = self.source_device_ip
		packet['sourceDeviceMAC'] = self.source_device_mac
		packet['targetDeviceId'] = self.target_device_id
		packet['targetDeviceIP'] = self.target_device_ip
		return packet
		
	
class DHCPPacket(Packet):
	source_device_id	= -1
	source_device_mac	= ''
	dhcp_fp = None
	def __init__(self, id, time, source_guid, network_id, source_device_id, source_device_mac, dhcp_fp):
		super(DHCPPacket, self).__init__(id, time, 'dhcp', source_guid, network_id)
		self.source_device_id = source_device_id
		self.source_device_mac = source_device_mac
		self.source_device_mac = source_device_mac
		self.dhcp_fp = dhcp_fp
		
	def update_match(self, network_id, source_device_id):
		self.network_id = network_id
		self.source_device_id = source_device_id
		
	def serialize(self):
		packet = super(DHCPPacket, self).serialize()
		packet['sourceDeviceMAC'] = self.source_device_mac
		packet['sourceDeviceId'] = self.source_device_id
		packet['dhcpFingerPrint'] = self.dhcp_fp
		return packet

def loadARPPacket(packet):
	if not 'targetDeviceId' in packet:
		packet['targetDeviceId'] = -1
	return ARPPacket(packet['id'],packet['time'],packet['sourceGUID'],
						packet['networkId'],
						packet['sourceDeviceId'],packet['sourceDeviceIP'],packet['sourceDeviceMAC'],
						packet['targetDeviceId'],packet['targetDeviceIP'])
						
def loadDHCPPacket(packet):
	return DHCPPacket(packet['id'],packet['time'],packet['sourceGUID'],
						packet['networkId'], 
						packet['sourceDeviceId'], packet['sourceDeviceMAC'], packet['dhcpFingerPrint'])
		
def loadPacket(packet):
	# set defaults
	if not 'networkId' in packet:
		packet['networkId'] = -1
	if not 'sourceDeviceId' in packet:
		packet['sourceDeviceId'] = -1
	
	if packet['type'] == 'arp':
		return loadARPPacket(packet)
	elif packet['type'] == 'dhcp':
		return loadDHCPPacket(packet)
	else:
		raise Exception('Unknown packet type %s' % packet['type'])