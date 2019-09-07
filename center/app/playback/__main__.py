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
import base64
logger = logging.getLogger('main')

def onLivePCAP(req):
    try:
        logger.info('New live pcap file')
        filename = '%s-%d.pcap' % (req['origin'], req['time'])
        filepath = os.path.join(env.pbak_folder, filename)
        with open(filepath, 'wb+') as fp:
            logger.debug('writing pcap file to folder')
            fp.write(base64.b64decode(req['data']))
        playFile(filename, req['origin'])
    except Exception as e:
        logger.error(str(e))

def onPlaybackRequest(req):
    logger.info('New playback request')
    playFile(req['file'], req['file'])

def playFile(filename, origin):
    global mqc
    filepath = os.path.join(env.pbak_folder, filename)
    packets = parsePCAP(filepath, origin)

    packetsBuffer = {
        'time': time.time(),
        'origin': origin,
        'numPackets': len(packets),
        'packets': packets
    }
    dmp_file = os.path.join(env.output_folder, 'pb-%s.json' % filename)
    with open(dmp_file, 'w') as f:
        json.dump(packetsBuffer,f,indent=4)
    mqc.publish('packetsBuffer', packetsBuffer)
    logger.info('pcap file parsed and published to processor')
    
    
try:
    mqc = MQClient(env)
    mqc.on_topic('playbackRequest', onPlaybackRequest)
    mqc.on_topic('livePCAP', onLivePCAP)
    keepalive.start(mqc, 'playback')
except KeyboardInterrupt:
    pass
except Exception as e:
    logger.fatal(str(e))