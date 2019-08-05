from source import loadSource
from device import loadDevice
from link import loadLink
from packet import loadPacket
from logItem import loadLogItem
from collections import OrderedDict
class Network:
	id 					= -1
	create_time			= 0
	last_update_time 	= 0
	default_gtw_mac 	= None
	default_gtw_ip  	= None
	
	source_mode			= ''
	source_count 		= 0
	sources 			= []
	device_count		= 0
	devices				= []
	link_count			= 0
	links				= []
	
	packets 			= []
	
	log					= []
	def __init__(self, id, 
				create_time, last_update_time, 
				default_gtw_mac, default_gtw_ip, 
				source_mode, source_count, sources, 
				device_count, devices, 
				link_count, links, packets, log):
		self.id = id
		self.create_time = create_time
		self.last_update_time = last_update_time
		self.default_gtw_mac = default_gtw_mac
		self.default_gtw_ip = default_gtw_ip
		self.source_mode = source_mode
		self.source_count = source_count
		self.sources = sources
		self.device_count = device_count
		self.devices = devices
		self.link_count = link_count
		self.links = links
		self.packets = packets
		self.log = log
		
	def serialize(self):
		dct =OrderedDict()
		dct['id'] = self.id
		dct['createTime'] = self.create_time
		dct['lastUpdateTime'] = self.last_update_time
		dct['defaultGTWMAC'] = self.default_gtw_mac
		dct['defaultGTWIP'] = self.default_gtw_ip
		dct['sourceMode'] = self.source_mode
		dct['sourceCount'] = self.source_count
		dct['sources'] = [src.serialize() for src in self.sources]
		dct['deviceCount'] = self.device_count
		dct['devices'] = [dev.serialize() for dev in self.devices]
		dct['linkCount'] = self.link_count
		dct['links'] = [link.serialize() for link in self.links]
		dct['packets'] = [pkt.serialize() for pkt in self.packets]
		dct['log'] = [item.serialize() for item in self.log]
		return dct


def loadNetwork(network):
	sources = []
	for src in network['sources']:
		sources.append(loadSource(src))
	
	devices = []
	for dev in network['devices']:
		devices.append(loadDevice(dev))
		
	links 	= []
	for link in network['links']:
		links.append(loadLink(link))
	
	packets 	= []
	for pkt in network['packets']:
		packets.append(loadPacket(pkt))
	
	log = []
	if 'log' in network:
		for item in network['log']:
			log.append(loadLogItem(item))

	if not 'sourceMode' in network:
		network['sourceMode'] = 'live'
	if not 'createTime' in network:
		network['createTime'] = 0
	if not 'lastUpdateTime' in network:
		network['lastUpdateTime'] = 0
		
	return Network(network['id'], network['createTime'], 
					network['lastUpdateTime'],
					network['defaultGTWMAC'], 
					network['defaultGTWIP'], 
					network['sourceMode'], network['sourceCount'], sources, 
					network['deviceCount'], devices, 
					network['linkCount'], links, packets,
					log)