from models import Link

class LinkProcessor:
	def __init__(self, network, broker):
		self.broker = broker
		self.network = network
		
	def findARPMatch(self, packet):
		for link in self.network.links:
			if link.source_device_id == packet.source_device_id and \
				link.target_device_id == packet.target_device_id:
				return link
		return None

	def updateLink(self, link, time):
		link.last_time = time
		self.broker.emit('linkUpdate', link)
		
	def createLink(self, packet):
		lid = self.getLinkId()
		link = Link(lid,
					self.network.id, 
					packet.time, 
					packet.time, 
					packet.source_device_id, 
					packet.target_device_id, 
					1)
		self.network.links.append(link)
		self.broker.emit('linkUpdate', link)
		return link

	def getLinkId(self):
		link_id = self.network.link_count
		self.network.link_count += 1
		return link_id
