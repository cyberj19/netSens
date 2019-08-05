from abc import ABCMeta, abstractmethod
import time
import env
import subprocess
import packetParser
import threading
import logging
import os
import sys
import interface

class Source:
    __metaclass__ = ABCMeta
    proc = None
    file = None
    mac = None
    iface = None
    cmd = None
    mode = None
    sid = None
    guid = None
    def __init__(self, logger, broker):
        self.packetId = 0
        self.connected = False
        self.record = env.debug_mode
        self.numPackets = 0
        self.connectTime = 0
        self.lastPacketTime = 0
        self.lastStatusTime = 0
        self.error = ''
        self.broker = broker
        self.thread = None
        self.threadLock = threading.Lock()
        self.logger = logger

        self.publishThread = threading.Thread(target=self._publish)
        self.publishThread.start()
		# super().__init__()


    def _publish(self):
        self.logger.info('Starting publish thread for source %s' % self.guid)
        if self.broker:
            while True:
                status = self.getStatus()
                self.logger.debug('source %s sending status: %s', self.guid, status)
                self.broker.emit('status', status)
                time.sleep(5)
        else:
            self.logger.warning('Unavailable broker for publishing')

    def setId(self, sid):
        self.sid = sid	

    def setBroker(self, broker):
        self.broker = broker
        
    @abstractmethod
    def getStatus(self):
        return {
            'guid': self.guid,
            'mode': self.mode,
            'connectTime': self.connectTime,
            'connected': self.connected,
            'numPackets': self.numPackets,
            'lastPacketTime': self.lastPacketTime,
            'lastError': self.error,
        }
			
    def connect(self):
        try:
            self.logger.info('Connecting to: "%s"', self.cmd)
            self.proc = subprocess.Popen(self.cmd.split(' '), stdout = subprocess.PIPE)
            if self.record:
                filename = getRecordFileName(self.mac, self.iface)
                self.file = open(filename, 'w')
            self.connectTime = time.time()
            self.connected = True
            self.thread = threading.Thread(target=self._read)
            self.thread.setDaemon(True)
            self.thread.start()
        except Exception, e:
            self.logger.error(str(e))
            self.error = str(e)
		
    def disconnect(self):
        self.logger.info('Disconnecting', self.iface)
        self.connected = False
        with self.threadLock:
            self.proc.terminate()
            if self.record:
                self.file.close()
		
    @abstractmethod
    def _decoratePacket(self, packet):
        pass
		
    def _read(self):
        with self.threadLock:
            while self.connected:
                line = self.proc.stdout.readline()
                self.logger.debug(line)
                if self.record:
                    try:
                        self.file.write(line)
                    except:
                        pass
                parts = line.strip().split(' ')
                if parts[0] == 'ERROR':
                    self.error = ' '.join(parts[1:])
                    self.logger.error('Error: %s', self.error)
                    break
                elif parts[0] == 'FINISH':
                    self.connected = False
                    if self.mode == 'playback':
                        self.error = 'PCAP file ended'
                    break
                elif parts[0] == 'PACKET':
                    try:
                        packet = packetParser.parse(parts[1])
                        packet['id'] = self.numPackets
                        packet['sourceGUID'] = self.guid
                        self.lastPacketTime = packet['time']
                        self.numPackets += 1
                    except:
                        self.error = 'Parse error'
                        self.logger.error('Unable to parse packet: %s', parts[1])
                        continue
                    self.broker.emit('packet', self._decoratePacket(packet))

def getRecordFileName(mac, interface):
    return '%s/%s_%s_%d.dat' % (env.recs_folder, mac, interface, time.time())
	
def getBinaryName(mode):
    return 'binaries/%s_%s' % (sys.platform, mode)