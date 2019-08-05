import interface
import os
import time
import logging
from live_source import LiveSource
from playback_source import PlaybackSource

logger = logging.getLogger('SourceManager')
class SourceManager:
    def __init__(self, env, broker):
        self.sources = {}
        self.sources_count = 0
        self.broker = broker
        self.mode = env.mode
        self.env = env
        if env.mode == 'live':
            self.addLiveSources()
        logger.info('source manager is up')
        
    def getPlaybackCatalogue(self):
        files = os.listdir(self.env.pbak_folder)
        return files

    def startPlayback(self, filename):
        source = PlaybackSource(filename, self.broker)
        self.addSource(source)
        source.connect()

    def addPlaybackSource(self, filename):
        files = self.getPlaybackCatalogue()
        if not filename in files:
            raise Exception('Unknown playback file %s' % filename)
        self.addSource(PlaybackSource(filename))

    def connectSource(self, guid):
        if not guid in self.sources:
            raise Exception('Unknown GUID %s' % guid)
        self.sources[guid].connect()

    def disconnectSource(self, guid):
        if not guid in self.sources:
            raise Exception('Unknown GUID %s' % guid)
        self.sources[guid].disconnect()

            
    def removeSources(self):
        self.sources = {}

    def addSource(self, source):
        if source.mode != self.mode:
            raise Exception('Source mode mismatch')

        source.setBroker(self.broker)
        self.sources[source.guid] = source
        self.sources_count += 1

    
    def addLiveSources(self):
        ifaces = interface.getInterfaces()
        for iface in ifaces:
            mac = ifaces[iface]
            source = LiveSource(mac, iface, self.broker)
            self.addSource(source)