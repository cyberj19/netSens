import logging
import json
import httplib
import time
from models import loadAgent, loadPacket

logger = logging.getLogger('gtw')
def sendJson(ip, port, url, data):
	encoded_data = json.dumps(data).encode('utf-8')
	headers = {
		"Content-type": "application/json", 
		"Accept": "text/plain"
	}
	conn = httplib.HTTPConnection(ip, port=port)
	conn.request("POST",url,encoded_data,headers)
	conn.getresponse()

class Connection:
	def __init__(self, agent, broker):
		self.broker = broker
		self.agent = loadAgent(patchAgent(agent))
		self.sendUpdate()

	def sendJson(self, url, data):
		sendJson(self.agent.ip, self.agent.port, url, data)		
	def updateActivity(self):
		if self.agent.active and \
						self.agent.time < time.time() - 10:
			self.agent.active = False
			for lstr in self.agent.listeners:
				lstr.agent_active = False
				lstr.connected = False
			self.sendUpdate()

	def create(self, intr):
		self.sendJson('/%s/create' % intr, {})
	
	def connect(self, intr):
		self.sendJson('/%s/connect' % intr, {})
		
	def disconnect(self, intr):
		self.sendJson('/%s/disconnect' % intr, {})
		
	def handlePackets(self, data):
		self.agent.time = data['time']
		self.sendUpdate()

		for packet in data['packets']:
			self.broker.emit('packet', loadPacket(packet))
			
	def update(self, agent):
		self.agent = loadAgent(patchAgent(agent))
		self.sendUpdate()
	
	def sendUpdate(self):
		self.broker.emit('agentStatus', self.agent)

def patchAgent(agent):
	agent['active'] = True
	for lstr in agent['listeners']:
		lstr['networkId'] = -1
		lstr['agentActive'] = True
	return agent
