import threading
import logging
import env
import adapters
import sys
import signal


from network_db import NetworkDB
from device_db import DeviceDB
from packet_db import PacketDB
from link_db import LinkDB
from listener_db import ListenerDB

logger = logging.getLogger('db')


class DB:
	def __init__(self, broker):
		try:
			self.lock = threading.Lock()
			self.adapter = adapters.getAdapter(env)
		except Exception, e:
			logger.fatal('Unable to connect to db: %s', str(e))
			raise Exception()
		self.deviceDB = DeviceDB(self.adapter, broker)
		self.linkDB = LinkDB(self.adapter, broker)
		self.packetDB = PacketDB(self.adapter, broker)
		self.listenerDB = ListenerDB(self.adapter, broker)
		self.networkDB = NetworkDB(self.adapter, broker, 
					self.deviceDB, self.linkDB, self.packetDB,
					self.listenerDB)
		signal.signal(signal.SIGINT, self._handleKill)

	def _handleKill(self, signal, frame):
		logger.warning(
		    'closing connection to database. some changes may remain unwritten')
		self.adapter.close()
		sys.exit(0)

	def getListeners(self):
		return self.listenerDB.get()
		
	def getNetworks(self, detailed=True):
		return self.networkDB.get(detailed)
		
	def getNetworkById(self, networkId, with_packets=False):
		return self.networkDB.getById(networkId, with_packets)
	
	def getDevicePackets(self, networkId, deviceId):
		return self.packetDB.getByDeviceId(networkId,deviceId)
