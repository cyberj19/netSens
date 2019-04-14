class Listener:
	id 			= -1
	agent_active= False
	agent_mac	= ''
	agent_port	= 0
	network_id	= -1
	mac			= ''
	interface	= ''
	connected 	= False
	num_packets	= 0
	last_packet	= 0
	last_error	= ''
	default_gtw = None
	def __init__(self, id, agent_active, agent_mac, agent_port, network_id, mac, interface, connected, num_packets, last_packet, last_error, default_gtw):
		self.id = id
		self.agent_active = agent_active
		self.agent_mac = agent_mac
		self.agent_port = agent_port
		self.network_id = network_id
		self.mac = mac
		self.interface = interface
		self.connected = connected
		self.num_packets = num_packets
		self.last_packet = last_packet
		self.last_error = last_error
		self.default_gtw = default_gtw
	
	def serialize(self):
		return {
			'id': self.id,
			'agentActive': self.agent_active,
			'agentMAC': self.agent_mac,
			'agentPort': self.agent_port,
			'networkId': self.network_id,
			'mac': self.mac, 
			'interface': self.interface,
			'connected': self.connected,
			'numPackets': self.num_packets,
			'lastPacketTime': self.last_packet,
			'lastError': self.last_error,
			'defaultGTW': self.default_gtw
		}

def loadListener(lstr):
	return Listener(lstr['id'],
					lstr['agentActive'],
					lstr['agentMAC'], lstr['agentPort'],
					lstr['networkId'], 
					lstr['mac'], lstr['interface'], 
					lstr['connected'], lstr['numPackets'], 
					lstr['lastPacketTime'],
					lstr['lastError'], lstr['defaultGTW'])