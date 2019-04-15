import vendors
import logging
from models import LogItem
from models import Device

MATCH_IMPOSSIBLE = 0
MATCH_POSSIBLE = 1
MATCH_CERTAIN = 2

logger = logging.getLogger('processor')
class DeviceProcessor:
	def __init__(self, network, broker):
		self.broker = broker
		self.network = network

	def createDevice(self, device_id, network_id, ptype, ts, ip=None, mac=None, dhcp_fp=None):
		vendor = vendors.getVendor(mac)
		if ptype == 'arp':
			arp = 1
			dhcp = 0
		elif ptype == 'dhcp':
			arp = 0
			dhcp = 1
		device = Device(device_id, False, network_id, ts, ts, ip, mac, vendor, 1, arp, dhcp, dhcp_fp=dhcp_fp)
		logger.debug("paga devproc %s",dhcp_fp)
		self.broker.emit('deviceUpdate', device)
		return device
		
	def updateDevice(self, device, ptype, time, ip=None, mac=None, dhcp_fp=None):
		logger.debug('naga [Device] Device %d has mac %s, ip %s paga %s', device.id, mac, ip, dhcp_fp)
		if time > device.last_time:
			device.last_time = time
		device.hits += 1
		if ptype == 'arp':
			device.arp_hits += 1
		elif ptype == 'dhcp':
			device.dhcp_hits += 1
		if mac:
			vendor = vendors.getVendor(mac)
			if not device.mac:
				logger.info('[Device] Device %d has new mac %s', device.id, mac)

				nlog = LogItem(self.network.id, time, 'SYS', '', 'Device %d has new mac %s' % (device.id, mac), 'LOW')
				self.broker.emit('networkLog-%d' % self.network.id, nlog)
				if vendor:
					logger.info('[Device] Device %d has new vendor %s', device.id, vendor)
			device.mac = mac
			device.vendor = vendor
			
		if ip:
			if device.ip != ip:
				logger.info('[Device] Device %d has new ip %s', device.id, ip)
			device.ip = ip
			
		self.broker.emit('deviceUpdate', device)
		if dhcp_fp:
			logger.debug("paga decproc up %s",dhcp_fp)
			device.dhcp_fp=dhcp_fp
	
	def matchDevice(self, device, time, cand_ip=None, cand_mac=None):
		if device.is_closed:
			return MATCH_IMPOSSIBLE
		if not cand_ip and not cand_mac: # nothing is known about candidate
			return MATCH_IMPOSSIBLE
		elif cand_ip and not cand_mac: # only candidate ip is known
			# TODO: add time test
			if device.ip and device.ip == cand_ip:
				return MATCH_POSSIBLE
			else:
				return MATCH_IMPOSSIBLE
		elif cand_mac and not cand_ip: # only candidate mac is known
			if device.mac:
				if device.mac == cand_mac:
					return MATCH_CERTAIN
				else:
					return MATCH_IMPOSSIBLE
			else:
				return MATCH_IMPOSSIBLE
		else: # ip and mac are known
			if device.mac:
				if device.mac == cand_mac:
					return MATCH_CERTAIN
				else:
					return MATCH_IMPOSSIBLE
			elif device.ip:
				if device.ip == cand_ip:
					return MATCH_POSSIBLE
				else:
					return MATCH_IMPOSSIBLE
	
	def findARPMatch(self, arpPacket):
		targetMatch = None
		bestTargetMatch = MATCH_IMPOSSIBLE
		sourceMatch = None
		bestSourceMatch = MATCH_IMPOSSIBLE

		ts = arpPacket.time
		sip = arpPacket.source_ip
		smac = arpPacket.source_mac
		tip = arpPacket.target_ip
		for dev in self.network.devices:
			score = self.matchDevice(dev, ts, cand_ip=sip, cand_mac=smac)
			if score >= bestSourceMatch:
				bestSourceMatch = score
				sourceMatch = dev

			score = self.matchDevice(dev, ts, cand_ip=tip)
			if score >= bestTargetMatch:
				bestTargetMatch = score
				targetMatch = dev            
		
		if bestTargetMatch > MATCH_IMPOSSIBLE:
			logger.debug('[ADF] Matched packet %d  target to device %d', 
						arpPacket.id, targetMatch.id)
		else:
			logger.debug('[ADF] packet %d target unmatched', arpPacket.id)
			targetMatch = None

		if bestSourceMatch > MATCH_IMPOSSIBLE:
			logger.debug('[ADF] Matched packet %d  source to device %d. Updating...', 
						arpPacket.id, sourceMatch.id)
		else:
			logger.debug('[ADF] packet %d source unmatched', arpPacket.id)
			sourceMatch = None
			
		return sourceMatch, targetMatch
				
	def findDHCPMatch(self, dhcpPacket):
		match = None
		bestMatch = MATCH_IMPOSSIBLE
		for dev in self.network.devices:
			score = self.matchDevice(dev, dhcpPacket.time, cand_mac=dhcpPacket.source_mac)
			if score >= bestMatch:
				match = dev
				bestMatch = score
		return match
