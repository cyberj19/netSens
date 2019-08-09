from flask import Blueprint, request, send_from_directory
import logging
from bson.json_util import dumps
from db import strip_id
import json
import os
import uuid
logger = logging.getLogger('api')

def create(env, mqttClient, dbClient):
    db = dbClient.db
    app = Blueprint('netSensAPI', __name__)
    @app.route('/<path:path>')
    def send(path):
        return send_from_directory(env.static_files_folder, path)
    
    @app.route('/')
    def sendIndex():
        return send_from_directory(env.static_files_folder, 'index.html')

    
    @app.route('/api/overview', methods=['GET'])
    def getOverview():
        networks = db['networks'].find()
        return dumps({
            'success': True,
            'networks': strip_id(networks)
        }), 200
    
    @app.route('/api/networks/<net_uuid>/devices/<dev_idx>/analyze')
    def analyzeDevice(net_uuid, dev_idx):
        dev_idx = int(dev_idx)
        packets = db['packets'].find({
            'networkId': net_uuid, 
            '$or': [{'sourceDeviceIdx': dev_idx},
                    {'targetDeviceIdx': dev_idx}]
        })
        return dumps({'success':True, 'packets':strip_id(packets)})

    @app.route('/api/networks/<net_uuid>/devices/<dev_idx>/comment')
    def commentDevice(net_uuid, dev_idx):
        req = json.loads(request.body)
        mqttClient.publish(
            'deviceAddData',
            {
                'networkId': net_uuid,
                'deviceIdx': int(dev_idx),
                'comment': req['comment']
            }
        )
        return json.dumps({'success':True}), 200
    @app.route('/api/networks/<uuid>')
    def getNetwork(uuid):
        network = db['networks'].find_one({'uuid': uuid})
        if not network:
            return json.dumps({
                'success': False,
                'error': 'Unknown network with this uuid'
            }), 404
        else:
            return dumps({
                'success': True,
                'network': network
            }), 200

    @app.route('/api/networks/<uuid>/clear', methods=['POST'])
    def clearNetwork(uuid):
        mqttClient.publish('clearNetwork', {
            'uuid': uuid
        })
        return json.dumps({'success': True}), 200
        
    @app.route('/api/networks/<uuid>/remove', methods=['POST'])
    def removeNetwork(uuid):
        mqttClient.publish('removeNetwork', {
            'uuid': uuid
        })
        return json.dumps({'success': True}), 200
        
    @app.route('/api/networks/<uuid>/rename/<name>', methods=['POST'])
    def renameNetwork(uuid, name):
        mqttClient.publish('renameNetwork', {
            'uuid': uuid,
            'name': name
        })
        return json.dumps({
            'success': True
        }), 200
    @app.route('/api/playback/<network>', methods=['POST'])
    def playback(network):
        if 'file' not in request.files:
            logger.error('No file in request')
            return json.dumps({'success': False, 'error': 'No file selected'}), 400
        file = request.files['file']
        if file.filename == '':
            logger.error('No file in request')
            return json.dumps({'success': False, 'error': 'No file selected'}), 400
        fileparts = file.filename.split('.')
        filename = '%s-%s.%s' % (fileparts[0], uuid.uuid4().hex, fileparts[1])
        logger.info('Playing file: %s', filename)

        file.save(os.path.join(env.pbak_folder, filename))
        payload = {
            'file': filename,
            'destNetwork': network 
        }
        mqttClient.publish('playbackRequest', payload)
        return json.dumps({'success': True}), 200

    return app