from listener import loadListener

class Agent:
	time		= 0
	active		= False
	ip			= None
	mac 		= None
	port		= None
	listeners 	= []
	
	def __init__(self, time, active, ip, mac, port, listeners):
		self.time = time
		self.active = active
		self.ip = ip
		self.mac = mac
		self.port = port
		self.listeners = listeners
	
	def serialize(self):
		return {
			'time': self.time,
			'active': self.active,
			'ip': self.ip,
			'mac': self.mac,
			'port': self.port,
			'listeners': [lstr.serialize() for lstr in self.listeners]
		}
		
def loadAgent(agnt):
	listeners = []
	for lstr in agnt['listeners']:
		lstr['agentActive'] = agnt['active']
		lstr['agentMAC'] = agnt['mac']
		lstr['agentPort'] = agnt['port']
		listeners.append(loadListener(lstr))
	return Agent(agnt['time'],
					agnt['active'], 
					agnt['ip'],
					agnt['mac'],
					agnt['port'],
					listeners)