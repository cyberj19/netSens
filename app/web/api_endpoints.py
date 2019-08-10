from flask import Blueprint, request, send_from_directory
import logging
from bson.json_util import dumps
import json
import os
import uuid
logger = logging.getLogger('api')

def create(env, mqttClient, dbClient):
    db = dbClient.db
    app = Blueprint('netSensAPI', __name__)
    logger.debug('static folder: %s', env.static_files_folder)
    @app.route('/<path:path>')
    def send(path):
        return send_from_directory(env.static_files_folder, path)
    
    @app.route('/')
    def sendIndex():
        return send_from_directory(env.static_files_folder, 'index.html')

    
    @app.route('/api/overview', methods=['GET'])
    def getOverview():
        networks = dbClient.getNetworksOverview()
        monitor = db.monitor.find()
        jobs = db.jobs.find({'finished':False})
        return dumps({
            'success': True,
            'networks': networks,
            'monitor': monitor,
            'jobs': jobs
        }), 200
    
    @app.route('/api/networks/<net_uuid>/devices/<dev_uuid>/analyze', methods=['GET'])
    def analyzeDevice(net_uuid, dev_uuid):
        packets = db.getDevicePackets(net_uuid, dev_uuid)
        return dumps({'success':True, 'packets': packets})

    @app.route('/api/networks/<net_uuid>/devices/<dev_uuid>/comment', methods=['POST'])
    def commentDevice(net_uuid, dev_uuid):
        req = request.json
        mqttClient.publish(
            'deviceExtraData',
            {
                'networkUUID': net_uuid,
                'deviceUUID': dev_uuid,
                'extraData': {'comment': req['comment']}
            }
        )
        return json.dumps({'success':True}), 200
    @app.route('/api/networks/<uuid>')
    def getNetwork(uuid):
        network = db.networks.find_one({'uuid': uuid})
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
    @app.route('/api/playback', methods=['POST'])
    def playback():
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
        mqttClient.publish('playbackRequest', {'file':filename})
        return json.dumps({'success': True}), 200

    return app