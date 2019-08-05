import source

import env
import subprocess
import threading
import logging
import time
import os

logger = logging.getLogger('playbackSource')


class PlaybackSource(source.Source):
    def __init__(self, filename, broker):
        logger.debug('creating playback source')
        self.mac = "00:00:00:00"
        self.filename = filename
        self.mode = 'playback'
        self.guid = '%s-%s-%d' % (self.mode, self.filename, time.time())
        self.cmd = '%s %s' % (source.getBinaryName('playback'),
                              os.path.join(env.pbak_folder, filename))
        source.Source.__init__(self, logger, broker)

        logger.info('Playback %s is ready', filename)

    def getStatus(self):
      status = source.Source.getStatus(self)
      status['filename'] = self.filename
      return status

    def _decoratePacket(self, packet):
      return packet
