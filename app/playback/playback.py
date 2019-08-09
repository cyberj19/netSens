import env
import sys
sys.path.append(env.infra_path)
import os
import mlog
import logging
import json
import time
from mqtt_client import MQTTClient
from pcap_parser import parsePCAP
import keepalive

mlog.configLoggers(['main', 'mqtt', 'parser'], env.logs_folder, env.debug_mode)
logger = logging.getLogger('main')

def onPlaybackRequest(req):
    logger.info('New playback request')
    filepath = os.path.join(env.pbak_folder, req['file'])
    mqtt.publish('job', {'name': req['file'], 'progress': 0, 'finished': False})
    packets = parsePCAP(filepath, req['file'])
    mqtt.publish('job', {'name': req['file'], 'progress': 30, 'finished': False})

    packetsBuffer = {
        'time': time.time(),
        'origin': req['file'],
        'numPackets': len(packets),
        'packets': packets
    }
    dmp_file = os.path.join(env.output_folder, 'pb-%s.json' % req['file'])
    with open(dmp_file, 'w') as f:
        json.dump(packetsBuffer,f,indent=4)
    mqtt.publish('packetsBuffer', packetsBuffer)

    
try:
    mqtt = MQTTClient(env)
    mqtt.on_topic('playbackRequest', onPlaybackRequest)
    keepalive.start(mqtt, 'playback')
except KeyboardInterrupt:
    pass
except Exception,e:
    logger.fatal(str(e))