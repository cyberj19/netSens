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
			for src in self.agent.sources:
				src.agent_active = False
				src.connected = False
			self.sendUpdate()

	def startPlayback(self, filename):
		logger.debug('start playback: %s', filename)
		self.sendJson('/playback/%s' % filename, {})

	def create(self, intr):
		self.sendJson('/%s/create' % intr, {})
	
	def connect(self, guid):
		self.sendJson('/%s/connect' % guid, {})
		
	def disconnect(self, guid):
		self.sendJson('/%s/disconnect' % guid, {})
		
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
	for src in agent['sources']:
		src['networkId'] = -1
		src['agentActive'] = True
	return agent
