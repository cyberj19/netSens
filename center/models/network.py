from listener import loadListener
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
	
	listener_count 		= 0
	listeners 			= []
	device_count		= 0
	devices				= []
	link_count			= 0
	links				= []
	
	packets 			= []
	
	log					= []
	def __init__(self, id, 
				create_time, last_update_time, 
				default_gtw_mac, default_gtw_ip, 
				listener_count, listeners, 
				device_count, devices, 
				link_count, links, packets, log):
		self.id = id
		self.create_time = create_time
		self.last_update_time = last_update_time
		self.default_gtw_mac = default_gtw_mac
		self.default_gtw_ip = default_gtw_ip
		self.listener_count = listener_count
		self.listeners = listeners
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
		dct['listenerCount'] = self.listener_count
		dct['listeners'] = [lst.serialize() for lst in self.listeners]
		dct['deviceCount'] = self.device_count
		dct['devices'] = [dev.serialize() for dev in self.devices]
		dct['linkCount'] = self.link_count
		dct['links'] = [link.serialize() for link in self.links]
		dct['packets'] = [pkt.serialize() for pkt in self.packets]
		dct['log'] = [item.serialize() for item in self.log]
		return dct


def loadNetwork(network):
	listeners = []
	for lst in network['listeners']:
		listeners.append(loadListener(lst))
	
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

	if not 'createTime' in network:
		network['createTime'] = 0
	if not 'lastUpdateTime' in network:
		network['lastUpdateTime'] = 0
		
	return Network(network['id'], network['createTime'], 
					network['lastUpdateTime'],
					network['defaultGTWMAC'], 
					network['defaultGTWIP'], 
					network['listenerCount'], listeners, 
					network['deviceCount'], devices, 
					network['linkCount'], links, packets,
					log)
