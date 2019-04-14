import env
import subprocess
import packetParser
import threading
import logging
import time
import os
import sys
import interface

logger = logging.getLogger('listener')

class Listener:
	proc = None
	file = None
	def __init__(self, id, mac, iface, channel):
		self.id = id
		self.mac = mac
		self.packetId = 0
		self.iface = iface
		self.default_gtw = interface.getDefaultGTW(iface)
		self.cmd = 'binaries/%s %s' % (getBinaryName(), iface)
		#self.cmd = 'binaries/%s_listener %s' % (sys.platform, iface)
		self.connected = False
		self.record = env.debug_mode
		self.numPackets = 0
		self.lastPacketTime = 0
		self.channel = channel
		self.error = ''
		self.thread = None
		self.threadLock = threading.Lock()
		logger.info('Listener %s is ready', iface)

	def getStatus(self):
		return {
			'id': self.id,
			'interface': self.iface,
			'mac': self.mac,
			'connected': self.connected,
			'numPackets': self.numPackets,
			'lastPacketTime': self.lastPacketTime,
			'lastError': self.error,
			'defaultGTW': self.default_gtw
		}
			
	def connect(self):
		try:
			logger.info('Listener %s is connecting', self.iface)
			self.proc = subprocess.Popen(self.cmd.split(' '), stdout = subprocess.PIPE)
			if self.record:
				filename = getRecordFileName(self.mac, self.iface)
				self.file = open(filename, 'w')
			
			self.connected = True;
			self.thread = threading.Thread(target=self._read)
			self.thread.setDaemon(True)
			self.thread.start()
		except Exception, e:
			logger.error(str(e))
			self.error = str(e)
		
	def disconnect(self):
		logger.info('Listener %s is disconnecting', self.iface)
		self.connected = False
		with self.threadLock:
			self.proc.terminate()
			if self.record:
				self.file.close()
		
	
	def _read(self):
		with self.threadLock:
			while self.connected:
				line = self.proc.stdout.readline()
				logger.debug(line)
				if self.record:
					try:
						self.file.write(line)
					except:
						pass
				parts = line.strip().split(' ')
				if parts[0] == 'ERROR':
					self.error = ' '.join(parts[1:])
					logger.error('Listener %s error: %s', self.iface, self.error)
					break
				elif parts[0] == 'PACKET':
					try:
						packet = packetParser.parse(parts[1])
						packet['id'] = self.numPackets
						packet['listenerInterface'] = self.iface
						packet['listenerMAC'] = self.mac
						self.lastPacketTime = packet['time']
						self.numPackets += 1
					except:
						self.error = 'Parse error'
						logger.error('Unable to parse packet: %s', parts[1])
						continue
					self.channel.send(packet)

def getRecordFileName(mac, interface):
	return '%s/%s_%s_%d.dat' % (env.recs_folder, mac, interface, time.time())
	
def getBinaryName():
	if env.sim_mode:
		return '%s_simulator' % sys.platform
	else:
		return '%s_listener' % sys.platform