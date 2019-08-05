from collections import OrderedDict
from source import loadSource
class Agent:
	time		= 0
	mode 		= ''
	active		= False
	ip			= None
	mac 		= None
	port		= None
	sources 	= []
	
	def __init__(self, time, mode, active, ip, mac, port, sources):
		self.time = time
		self.mode = mode
		self.active = active
		self.ip = ip
		self.mac = mac
		self.port = port
		self.sources = sources
	
	def serialize(self):
		dct = OrderedDict()
		dct['time'] = self.time
		dct['mode'] = self.mode
		dct['active'] = self.active
		dct['ip'] = self.ip
		dct['mac'] = self.mac
		dct['port'] = self.port
		dct['src'] = [src.serialize() for src in self.sources]
		return dct
		
def loadAgent(agnt):
	sources = []
	for src in agnt['sources']:
		src['agentActive'] = agnt['active']
		src['agentMAC'] = agnt['mac']
		src['agentPort'] = agnt['port']
		sources.append(loadSource(src))
	return Agent(agnt['time'],
				agnt['mode'],
					agnt['active'], 
					agnt['ip'],
					agnt['mac'],
					agnt['port'],
					sources)