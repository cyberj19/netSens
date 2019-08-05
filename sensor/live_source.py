import source
import time
import env
import subprocess
import threading
import logging
import os
import interface
logger = logging.getLogger('liveSource')

class LiveSource(source.Source):
    proc = None
    file = None
    def __init__(self, mac, iface, broker):
        self.mac = mac
        self.iface = iface
        self.mode = 'live'
        self.guid = '%s-%s-%s-%d' % (self.mode, self.mac, self.iface, time.time())
        self.cmd = source.getBinaryName('live') + ' ' + iface
        source.Source.__init__(self, logger, broker)
		
        logger.info('Listener %s is ready', iface)

    def getStatus(self):
		status = source.Source.getStatus(self)
		return status
		
    def _decoratePacket(self, packet):
        return packet