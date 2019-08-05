class Source:
	guid 		= ''
	mode 		= ''
	agent_active= False
	agent_mac	= ''
	agent_port	= 0
	network_id	= -1
	connected 	= False
	num_packets	= 0
	last_packet	= 0
	last_error	= ''
	def __init__(self, guid, mode, agent_active, 
	agent_mac, agent_port, network_id, 
	connected, num_packets, 
	last_packet, last_error):
		self.guid = guid
		self.mode = mode
		self.agent_active = agent_active
		self.agent_mac = agent_mac
		self.agent_port = agent_port
		self.network_id = network_id
		self.connected = connected
		self.num_packets = num_packets
		self.last_packet = last_packet
		self.last_error = last_error

	def serialize(self):
		return {
			'guid': self.guid,
			'mode': self.mode,
			'agentActive': self.agent_active,
			'agentMAC': self.agent_mac,
			'agentPort': self.agent_port,
			'networkId': self.network_id,
			'connected': self.connected,
			'numPackets': self.num_packets,
			'lastPacketTime': self.last_packet,
			'lastError': self.last_error,
		}

def loadSource(src):
	return Source(src['guid'],
					src['mode'],
					src['agentActive'],
					src['agentMAC'], src['agentPort'],
					src['networkId'], 
					src['connected'], src['numPackets'], 
					src['lastPacketTime'],
					src['lastError'])