import env
import channel
import json
import listener
import interface
import flask
import threading
import time
import socket
import httplib
import logging
from infra.processQueue import ProcessQueue
logger = logging.getLogger('proxy')

def sendJson(ip, port, url, data):
	logger.debug('Sending data to %s:%d%s', ip, port, url)
	encoded_data = json.dumps(data).encode('utf-8')
	headers = {"Content-type": "application/json", "Accept": "text/plain"}
	conn = httplib.HTTPConnection(ip, port=port)
	conn.request("POST",url,encoded_data,headers)
	response = conn.getresponse()

class Proxy:
	def __init__(self, id, comm_iface, local_port, center_ip, center_port):
		self.id = id
		self.center_ip = center_ip
		self.center_port = center_port
		self.center_url = '%s:%d' % (center_ip, center_port)
		self.local_port = local_port
		self.comm_iface = comm_iface
		self.num_center_failures = 0
		
		interfaces = interface.getInterfaces()
		if comm_iface in interfaces:
			self.mac = interfaces[comm_iface]
		else:
			self.mac = '00:00:00:00'
		
		self.listId = 0
		self.listeners = {}
		for iface in interfaces:
			self.listeners[iface] = listener.Listener(self.listId, interfaces[iface], iface, self)
			self.listId += 1
		
		
		self.packetQueue = ProcessQueue('SendPackets',
										procFunc=self.sendPackets,
										bulkMode=True,
										requeueOnFail=True,
										errorFunc=lambda e: logger.error(str(e)),
										interval=1)
										
		self.statusThread = threading.Thread(target=self._sendStatus)
		self.statusThread.setDaemon(True)
		self.statusThread.start()

		
		self.http = flask.Flask('sensorAPI')
		self._setupAPI()
		self.http.run(host='0.0.0.0', port=local_port)
	
	def _setupAPI(self):
		@self.http.route('/<intr>/connect', methods=['POST'])
		def connect(intr):
			logger.info('connection request for interface %s', intr)
			if not intr in self.listeners:
				return json.dumps({'success': False, 'error': 'Interface not configured'}), 404
			if self.listeners[intr].connected:
				return json.dumps({'success': True}), 200
			self.listeners[intr].connect()
			return json.dumps({'success': True}), 200
		
		@self.http.route('/<intr>/disconnect', methods=['POST'])
		def disconnect(intr):
			logger.info('disconnection request for interface %s', intr)
			if not intr in self.listeners:
				return json.dumps({'success': False, 'error': 'Interface not configured'}), 404
			if not self.listeners[intr].connected:
				return json.dumps({'success': True}), 200
			self.listeners[intr].disconnect()
			return json.dumps({'success': True}), 200

	def send(self, msg):
		if len(self.packetQueue.queue) == env.queue_max_packets:
			logger.warning('Packet queue reached max capacity. Packet is being dropped')
			return
		logger.info('Queueing new packet')
		self.packetQueue.enqueue(msg)
	
	def sendPackets(self, packets):
		payload = {
			'time': time.time(),
			'mac': self.mac,
			'packets': packets
		}
		logger.info('Sending %d new captured packets', len(packets))
		sendJson(self.center_ip, self.center_port, '/packets', payload)

	def _sendStatus(self):
		while True:
			try:
				listeners_status = []
				for key in self.listeners:
					listeners_status.append(self.listeners[key].getStatus())
				
				status = {
					'time': time.time(),
					'mac': self.mac,
					'port': self.local_port,
					'listeners': listeners_status
				}
				if env.sim_mode:
					status['mode'] = 'simulation'
				else:
					status['mode'] = 'realtime'
				
				sendJson(self.center_ip, self.center_port, '/status', status)
				self.num_center_failures = 0
			except Exception, e:
				logger.error('Unable to send status to server: %s', str(e))
				self.num_center_failures += 1
				if self.num_center_failures == 3:
					logger.info('Unable to reach center. Disconnecting all interfaces and purging packet queue')
					for lstr in self.listeners:
						if self.listeners[lstr].connected:
							self.listeners[lstr].disconnect()
					self.packetQueue.purge()
			finally:
				time.sleep(5)
