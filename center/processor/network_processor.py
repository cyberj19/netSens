from device_processor import DeviceProcessor
from link_processor import LinkProcessor
from models import LogItem
import logging
import threading
import time

logger = logging.getLogger('processor')

class NetworkProcessor:
	def __init__(self, network, broker):
		self.lock = threading.Lock()
		self.network = network
		self.broker = broker
		self.devProc = DeviceProcessor(network, broker) 
		self.linkProc = LinkProcessor(network, broker)
		
		self.broker.on('networkLog-%d' % self.network.id,
						self.addLog)

	def findDevice(self, deviceId):
		for dev in self.network.devices:
			if dev.id == deviceId:
				return dev
		return None
		
	def addLog(self, item):
		with self.lock:
			self.network.log.append(item)
		self.broker.emit('networkUpdate', self.network)

	def clearNetwork(self):
		logger.info('Network %d is being cleared', self.network.id)
		with self.lock:
			self.network.devices = []
			self.network.links = []
			self.network.packets = []
			self.network.device_count = 0
			self.network.link_count = 0
			self.network.log = []
			self.broker.emit('networkUpdate', self.network)
	
	def addDeviceData(self, deviceId, data):
		with self.lock:
			for device in self.network.devices:
				if device.id == deviceId:
					device.extra_data.update(data)
					self.broker.emit('deviceUpdate', device)
					break

	def closeDevice(self, deviceId):
		with self.lock:
			for device in self.network.devices:
				if device.id == deviceId:
					logger.info('Device %d/%d was closed by user', self.network.id, device.id)
					device.is_closed = True
					self.broker.emit('deviceUpdate', device)
					break
					# log = LogItem(self.network.id, time.time(), 'manual', '', 'Device %d was closed' % device.id, 'MEDIUM')
					# self.addLog(log)

	def commentDevice(self, deviceId, comment):
		logger.debug('User added comment to device %d/%d', self.network.id, deviceId)
		self.addDeviceData(deviceId, {'comment': comment})

	def matchListener(self, listener):
		for lstr in self.network.listeners:
			if lstr.mac == listener.mac and lstr.interface == listener.interface:
				return True
		return False
		
	def matchPacket(self, packet):
		for lstr in self.network.listeners:
			if lstr.mac == packet.listener_mac and lstr.interface == packet.listener_iface:
				return True
		return False
	
	def processPacket(self, packet):
		with self.lock:
			if packet.type == 'arp':
				self.processARPPacket(packet)
			elif packet.type == 'dhcp':
				self.processDHCPPacket(packet)
		self.broker.emit('networkUpdate', self.network)
		self.broker.emit('packetProcessed', packet)
			
	def processDHCPPacket(self, packet):
		source_match = self.devProc.findDHCPMatch(packet)
		
		if source_match:
			source_dev_id = source_match.id
			self.devProc.updateDevice(source_match, 'dhcp', packet.time, packet.source_ip, packet.source_mac)
		else:
			source_dev_id = self.getDeviceId()
			dev = self.devProc.createDevice(source_dev_id, self.network.id, 'dhcp', packet.time, packet.source_ip, packet.source_mac)
			self.network.devices.append(dev)

		packet.update_match(self.network.id, source_dev_id)
		self.network.packets.append(packet)
		self.network.last_update_time = packet.time
		
	def processARPPacket(self, packet):
		logger.debug('[NET-%d] Handling arp packet %d', self.network.id, packet.id)
		self.updateDevicesARP(packet)
		self.updateLinksARP(packet)
		self.network.packets.append(packet)
		self.network.last_update_time = packet.time
		if self.network.default_gtw_ip == packet.source_ip:
			self.network.default_gtw_mac = packet.source_mac
			self.broker.emit('networkMajorChange', self)
		
	def updateDevicesARP(self, packet):
		source_match, target_match = self.devProc.findARPMatch(packet)
		logger.debug('naga src_m: %s tar_m: %s', packet.source_ip, packet.target_ip)
		if source_match:
			logger.debug('naga source match %s %d',source_match.id, packet.time)
			source_dev_id = source_match.id
			dev=self.devProc.updateDevice(source_match, 'arp', packet.time, packet.source_ip, packet.source_mac)
			self.network.devices.append(dev)
		else:
			logger.debug("naga ELSE SOURCE MATCH sdi %s",self.getDeviceId())
			source_dev_id = self.getDeviceId()
			dev = self.devProc.createDevice(source_dev_id, self.network.id, 'arp', packet.time, packet.source_ip, packet.source_mac)
			self.network.devices.append(dev)
		if target_match:
			logger.debug("naga TARGET MATCH %s",target_match.id)
			target_dev_id = target_match.id
			self.devProc.updateDevice(target_match, 'arp', packet.time, packet.target_ip)
		else:
			logger.debug("naga ELSE TARGET MATCH %s",self.getDeviceId())
			target_dev_id = self.getDeviceId()
			#dev = self.devProc.createDevice(target_dev_id, self.network.id, 'arp', packet.time, packet.target_ip)
			#self.network.devices.append(dev)
		
		packet.update_match(self.network.id, source_dev_id, target_dev_id)
	
	def updateLinksARP(self, packet):
		match = self.linkProc.findARPMatch(packet)
		if match:
			self.linkProc.updateLink(match, packet.time)
		else:
			link = self.linkProc.createLink(packet)
		
	def getDeviceId(self):
		dev_id = self.network.device_count
		self.network.device_count += 1
		return dev_id
