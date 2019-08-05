from infra import ProcessQueue
import logging
logger = logging.getLogger('db')
class NetworkDB:
	def __init__(self, db, broker, deviceDB, linkDB, packetDB, listenerDB):
		self.db = db
		self.deviceDB = deviceDB
		self.linkDB = linkDB
		self.packetDB = packetDB
		self.listenerDB = listenerDB
		self.broker = broker

		ProcessQueue('NetworkUpdate', 
			procFunc=self.writeNetwork, 
			requeueOnFail=True,
			preFunc=self.serializeNetwork,
			broker=self.broker,
			topic='networkUpdate')		
		
	def getById(self, network_id, with_packets):
		network = self.db['networks'].find_one({'id': network_id})
		if not network:
			return None
		network['devices'] = self.deviceDB.getByNetworkId(network_id)
		network['links'] = self.linkDB.getByNetworkId(network_id)
		network['listeners'] = self.listenerDB.getByNetworkId(network_id)
		if with_packets:
			network['packets'] = self.packetDB.getByNetworkId(network_id)
		return network
	
	def get(self, detailed):
		networks = self.db['networks'].find()
		# logger.debug('networks = %s', networks)
		if detailed:
			devices = self.deviceDB.get()
			links = self.linkDB.getLinks()
			packets = self.packetDB.getPackets()
			listeners = self.listenerDB.get()

			for ntw in networks:
				ntw['devices'] = [dev for dev in devices if dev['networkId'] == ntw['id']]
				ntw['links'] = [link for link in links if link['networkId'] == ntw['id']]
				ntw['packets'] = [pkt for pkt in packets if pkt['networkId'] == ntw['id']]
				ntw['listeners'] = [lstr for lstr in listeners if lstr['networkId'] == ntw['id']]
		return networks

	def serializeNetwork(self, network):
		network = network.serialize()
		del network['devices']
		del network['links']
		del network['packets']
		del network['listeners']
		return network
		
	def writeNetwork(self, network):
		self.db['networks'].upsert({'id': network['id']}, network)
	