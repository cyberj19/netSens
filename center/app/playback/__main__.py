import env
import sys
sys.path.append(env.infra_path)
import os
import mlog
import logging
mlog.configLoggers(['main', 'mq', 'parser'], env.logs_folder, env.debug_mode)

import json
import time
from mq import MQClient
from pcap_parser import parsePCAP
import keepalive

logger = logging.getLogger('main')

def onPlaybackRequest(req):
    global mqc
    logger.info('New playback request')
    filepath = os.path.join(env.pbak_folder, req['file'])
    packets = parsePCAP(filepath, req['file'])

    packetsBuffer = {
        'time': time.time(),
        'origin': req['file'],
        'numPackets': len(packets),
        'packets': packets
    }
    dmp_file = os.path.join(env.output_folder, 'pb-%s.json' % req['file'])
    with open(dmp_file, 'w') as f:
        json.dump(packetsBuffer,f,indent=4)
    mqc.publish('packetsBuffer', packetsBuffer)
    logger.info('pcap file parsed and published to processor')
    
try:
    mqc = MQClient(env)
    mqc.on_topic('playbackRequest', onPlaybackRequest)
    keepalive.start(mqc, 'playback')
except KeyboardInterrupt:
    pass
except Exception as e:
    logger.fatal(str(e))