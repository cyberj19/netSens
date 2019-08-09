import os
import env
import mlog
import logging
import json
import time
from mqtt_client import MQTTClient
from pcap_parser import parsePCAP

mlog.configLoggers(['main', 'mqtt', 'parser'], env.logs_folder, env.debug_mode)
logger = logging.getLogger('main')

def onPlaybackRequest(request):
    logger.info('New playback request')
    req = json.loads(request)
    filepath = os.path.join(env.pbak_folder, req['file'])
    packets = parsePCAP(filepath, req['file'])
    packetsBuffer = {
        'time': time.time(),
        'origin': req['file'],
        'numPackets': len(packets),
        'packets': packets
    }
    if 'destNetwork' in req and req['destNetwork'] != 'none':
        packetsBuffer['destNetwork'] = req['destNetwork']

    dmp_file = '../../data/runtime/playback/pb-%s.json' % req['file']
    with open(dmp_file, 'w') as f:
        json.dump(packetsBuffer,f,indent=4)
    mqtt.publish('packetsBuffer', json.dumps(packetsBuffer))

    
try:
    mqtt = MQTTClient(env)
    mqtt.on_topic('playbackRequest', onPlaybackRequest)
except Exception,e:
    logger.fatal(str(e))