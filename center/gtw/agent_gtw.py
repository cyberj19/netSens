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
		self.http = flask.Flask('SensorGTW')
		self._setupAPI()

		flask_thread = threading.Thread(target=self._flaskThread)
		flask_thread.setDaemon(True)
		flask_thread.start()

		
		agent_thread = threading.Thread(target=self.purgeAgents)
		agent_thread.setDaemon(True)
		agent_thread.start()
		
	def connectInterface(self, smac, sintr):
		if smac in self.agents:
			logger.info('Connecting sensor on %s to interface %s', smac, sintr)
			self.agents[smac].connect(sintr)
		else:
			raise Exception('Unknown sensor with this mac')
	
	def disconnectInterface(self, smac, sintr):
		if smac in self.agents:
			logger.info('Disconnecting sensor on %s from interface %s', smac, sintr)
			self.agents[smac].disconnect(sintr)
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
				if data['mode'] == 'simulation' and not self.env.enable_sim_sensors:
					logger.warning('Connection from agent in simulation mode dropped')
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
	gtw = GTW(7000,None)