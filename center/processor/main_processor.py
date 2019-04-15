import threading
from network_processor import NetworkProcessor
import logging
from models import  Network
from infra import ProcessQueue
logger = logging.getLogger('processor')

class MainProcessor:
	def __init__(self, networks, broker):
		self.serializeLock = threading.Lock()
		self.broker = broker
		self.networkProcs = [NetworkProcessor(ntw, broker) for ntw in networks]
		self.networkLock = threading.Lock()
		self.network_count = len(networks)
		
		ProcessQueue('PacketQueue', 
					self.processPacket,
					broker=broker, 
					topic='packet',
					errorFunc=lambda e: logger.error(str(e)))
		
		
		ProcessQueue('AgentQueue', 
					self.processAgentStatus,
					broker=broker, 
					topic='agentStatus',
					errorFunc=lambda e: logger.error(str(e)))

		ProcessQueue('NetworkQueue', 
					self.processMajorChange,
					broker=broker, 
					topic='networkMajorChange',
					errorFunc=lambda e: logger.error(str(e)))

		ProcessQueue('ManualOperations', 
					self.processManualOperations,
					broker=broker, 
					topic='manualOper',
					errorFunc=lambda e: logger.error(str(e)))

		logger.info('MainProcessor intialized')
	
	def serializeNetworks(self):
		with self.serializeLock:
			return [ntwProc.network.serialize() for ntwProc in self.networkProcs]
	
	def findNetwork(self, netId):
		for ntwProc in self.networkProcs:
			if ntwProc.network.id == netId:
				return ntwProc
		return None

	def processManualOperations(self, oper):
		ntw = self.findNetwork(oper['networkId'])
		if not ntw:
			raise Exception('Unknown network %d' % ntw)
		if oper['type'] == 'deviceClose':
			ntw.closeDevice(oper['deviceId'])
		elif oper['type'] == 'deviceComment':
			ntw.commentDevice(oper['deviceId'], oper['comment'])
		elif oper['type'] == 'clearNetwork':
			ntw.clearNetwork()
		elif oper['type'] == 'addDeviceData':
			logger.debug('add data: %s', str(oper['data']))
			ntw.addDeviceData(oper['deviceId'], oper['data'])
		elif oper['type'] == 'fingerBankRequest':
			logger.debug('fingerBankAnalysis')
			dev = ntw.findDevice(oper['deviceId'])
			self.broker.emit('fingerBankAnalysis', dev)
		elif oper['type'] == 'macVendorsRequest':
			logger.debug('macVendorsLookup')
			dev = ntw.findDevice(oper['deviceId'])
			self.broker.emit('macVendorsLookup', dev)
			
	def processAgentStatus(self, agent):
		for lstr in agent.listeners:
			self.processListener(lstr, agent.time)

	def processListener(self, lstr, time):
		for ntwProc in self.networkProcs:
			if ntwProc.matchListener(lstr):
				logger.info('Matched listener to network %d', ntwProc.network.id)
				lstr.network_id = ntwProc.network.id
				self.broker.emit('listenerUpdate', lstr)
				break
		else:
			with self.serializeLock:
				network = self.createNewNetwork(time, lstr)
			logger.info('Created new network %d', network.id)

	def processPacket(self, packet):
		logger.debug('Matching packet %s', packet.type)
		if packet.type =='dhcp':
			logger.debug('paga DHCP: %s', packet.dhcp_fp)
		for ntwProcessor in self.networkProcs:
			logger.debug('Matching packet %s to network %d', packet.type, ntwProcessor.network.id)
			if ntwProcessor.matchPacket(packet):
				logger.info('Processing %s packet in network %d', packet.type, ntwProcessor.network.id)
				with self.serializeLock:
					ntwProcessor.processPacket(packet)
	
	def createNewNetwork(self, time, listener):
		nid = self.network_count
		self.network_count += 1
		network = Network(id=nid, 
						  create_time=time, 
						  last_update_time=time, 
						  default_gtw_mac=None, 
						  default_gtw_ip=listener.default_gtw, 
						  listener_count=1, listeners=[listener], 
						  device_count=0, devices=[], 
						  link_count=0, links=[], 
						  packets=[],
						  log=[])
		
		self.networkProcs.append(NetworkProcessor(network, self.broker))
		self.broker.emit('networkUpdate', network)

		listener.network_id = nid
		self.broker.emit('listenerUpdate', listener)
		return network
	
	def processMajorChange(self, network):
		return
		for ntwProc in self.networkProcs:
			if ntwProc.network == network:
				continue
			if ntwProc.matchNetwork(network):
				with self.serializeLock:
					ntwProc.mergeNetwork(network)
				# TODO : merge network and delete old network
