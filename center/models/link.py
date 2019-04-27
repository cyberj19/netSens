from collections import OrderedDict

def loadLink(link):
	return Link(link['id'],link['networkId'],link['firstTimeSeen'],link['lastTimeSeen'],
				link['sourceDeviceId'],link['targetDeviceId'],link['hits'])
class Link:
	id					= -1
	network_id			= -1
	first_time			= 0
	last_time			= 0
	source_device_id 	= -1
	target_device_id	= -1
	hits				= 0
	
	def __init__(self, id, network_id, first_time, last_time, source_device_id, target_device_id, hits):
		self.id = id
		self.network_id = network_id
		self.first_time = first_time
		self.last_time = last_time
		self.source_device_id = source_device_id
		self.target_device_id = target_device_id
		self.hits = hits
		
	def serialize(self):
		dct = OrderedDict()
		dct['id'] = self.id
		dct['networkId'] = self.network_id
		dct['firstTimeSeen'] = self.first_time
		dct['lastTimeSeen'] = self.last_time
		dct['source'] = self.source_device_id
		dct['target'] = self.target_device_id
		dct['hits'] = self.hits
		return dct
