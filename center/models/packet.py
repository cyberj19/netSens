class Packet(object):
	id 				= -1
	time			= 0
	type 			= ''
	listener_mac 		= ''
	listener_iface 	= ''
	network_id		= -1
	def __init__(self, id, time, type, listener_mac, listener_iface, network_id):
		self.id = id
		self.time = time
		self.type = type
		self.listener_mac = listener_mac
		self.listener_iface = listener_iface
		self.network_id = network_id
		
	def serialize(self):
		return {
			'id': self.id, 
			'time': self.time, 
			'type': self.type, 
			'listenerMAC': self.listener_mac, 
			'listenerInterface': self.listener_iface,
			'networkId': self.network_id
			}
		
class ARPPacket(Packet):
	source_device_id 	= -1
	source_ip			= ''
	source_mac			= ''
	target_device_id	= -1
	target_ip			= ''
	
	def __init__(self, id, time, listener_mac, listener_iface, network_id, source_device_id,
				source_ip, source_mac, target_device_id, target_ip, dhcp_finger_print=None):
		super(ARPPacket, self).__init__(id, time, 'arp', listener_mac, listener_iface, network_id)
		self.source_device_id = source_device_id
		self.source_ip = source_ip
		self.source_mac = source_mac
		self.target_device_id = target_device_id
		self.target_ip = target_ip
		self.dhcp_fp = dhcp_finger_print
	
	def update_match(self, network_id, source_device_id, target_device_id):
		self.network_id = network_id
		self.source_device_id = source_device_id
		self.target_device_id = target_device_id
		
	def serialize(self):
		packet = super(ARPPacket, self).serialize()
		packet['sourceDeviceId'] = self.source_device_id
		packet['sourceIP'] = self.source_ip
		packet['sourceMAC'] = self.source_mac
		packet['targetDeviceId'] = self.target_device_id
		packet['targetIP'] = self.target_ip
		return packet
		
	
class DHCPPacket(Packet):
	source_device_id	= -1
	source_mac			= ''
		
	def __init__(self, id, time, listener_mac, listener_iface, network_id, source_device_id, source_mac, dhcp_fp=None):
		super(DHCPPacket, self).__init__(id, time, 'dhcp', listener_mac, listener_iface, network_id)
		self.source_device_id = source_device_id
		self.source_mac = source_mac
		self.dhcp_fp=dhcp_fp
		
	def update_match(self, network_id, source_device_id):
		self.network_id = network_id
		self.source_device_id = source_device_id
		
	def serialize(self):
		packet = super(DHCPPacket, self).serialize()
		packet['sourceMAC'] = self.source_mac
		packet['sourceDeviceId'] = self.source_device_id
		packet['dhcpFingerPrint'] = self.dhcp_fp
		return packet

def loadARPPacket(packet):
	if not 'targetDeviceId' in packet:
		packet['targetDeviceId'] = -1
	return ARPPacket(packet['id'],packet['time'],packet['listenerMAC'],packet['listenerInterface'],
						packet['networkId'],packet['sourceDeviceId'],packet['sourceIP'],packet['sourceMAC'],
						packet['targetDeviceId'],packet['targetIP'])
						
def loadDHCPPacket(packet):
	dhcp_fp=packet['dhcpFingerPrint'] if 'dhcpFingerPrint' in packet else None
	return DHCPPacket(packet['id'],packet['time'],packet['listenerMAC'],packet['listenerInterface'],
						packet['networkId'], packet['sourceDeviceId'], packet['sourceMAC'], dhcp_fp)
		
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
