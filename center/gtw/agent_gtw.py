import flask
import threading
import time
import logging
import json
from connection import Connection
from models import loadPacket
logger = logging.getLogger('gtw')

class GTW:
	def __init__(self, env, broker):
		self.broker = broker
		self.env = env
		self.agents = {}
		self.playback_agent = None
		self.http = flask.Flask('SensorGTW')
		self._setupAPI()

		flask_thread = threading.Thread(target=self._flaskThread)
		flask_thread.setDaemon(True)
		flask_thread.start()

		
		agent_thread = threading.Thread(target=self.purgeAgents)
		agent_thread.setDaemon(True)
		agent_thread.start()
		
	def startPlayback(self, filename):
		logger.debug(self.agents)
		for smac in self.agents:
			logger.info('Start playback %s on agent %s', filename, smac)
			self.agents[smac].startPlayback(filename)
			break
		
	def connectSource(self, smac, guid):
		if smac in self.agents:
			logger.info('Connecting agent %s on source %s', smac, guid)
			self.agents[smac].connect(guid)
		else:
			raise Exception('Unknown sensor with this mac')
	
	def disconnectInterface(self, smac, guid):
		if smac in self.agents:
			logger.info('Disconnecting agent %s on source %s', smac, guid)
			self.agents[smac].disconnect(guid)
		else:
			raise Exception('Unknown sensor with this mac')
		
	def purgeAgents(self):
		while True:
			for smac in self.agents:
				self.agents[smac].updateActivity()
			time.sleep(5)			
	def _flaskThread(self):
		self.http.run(host='0.0.0.0',port=self.env.gtw_port)
		
	def _setupAPI(self):
		@self.http.route('/status', methods=['POST'])
		def status():
			data = flask.request.get_json()
			data['ip'] = flask.request.environ.get('HTTP_X_REAL_IP', flask.request.remote_addr)   
			smac = data['mac']
			if smac in self.agents:
				self.agents[smac].update(data)
			else:
				logger.info('New agent detected from ip %s', data['ip'])
				if data['mode'] != self.env.mode:
					logger.warning('Connection from agent in %s mode dropped', data['mode'])
					return json.dumps({'success': False, 'error': 'Illegal environment'}), 404
				self.agents[smac] = Connection(data, self.broker)
			return json.dumps({'success':True}),200
				
		@self.http.route('/packets', methods=['POST'])
		def packets():
			data = flask.request.get_json()
			smac = data['mac']
			if smac in self.agents:
				self.agents[smac].handlePackets(data)
			else:
				logger.warning('Received packets from unknown agent %s', smac)
			return json.dumps({'success':True}),200		
if __name__ == '__main__':
	gtw = GTW(7000, None)