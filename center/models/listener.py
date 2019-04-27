from collections import OrderedDict

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
		dct=OrderedDict()
		dct['id']= self.id
		dct['agentActive'] = self.agent_active
		dct['agentMAC'] = self.agent_mac
		dct['agentPort'] = self.agent_port
		dct['networkId'] = self.network_id
		dct['mac'] = self.mac
		dct['interface'] = self.interface
		dct['connected'] = self.connected
		dct['numPackets'] = self.num_packets
		dct['lastPacketTime'] = self.last_packet
		dct['lastError'] = self.last_error
		dct['defaultGTW'] = self.default_gtw
		return dct

def loadListener(lstr):
	return Listener(lstr['id'],
					lstr['agentActive'],
					lstr['agentMAC'], lstr['agentPort'],
					lstr['networkId'], 
					lstr['mac'], lstr['interface'], 
					lstr['connected'], lstr['numPackets'], 
					lstr['lastPacketTime'],
					lstr['lastError'], lstr['defaultGTW'])
