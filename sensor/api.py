import json
import logging
import flask
import os
logger = logging.getLogger('api')

class API:
    def __init__(self, env, manager):
        self.http = flask.Flask('API')
        self.env = env
        self.manager = manager
        _setupAPI(self.http, self.manager)
        # if self.env.mode == 'live':
            # _setupLiveAPI(self.http, self.manager)
        # elif self.env.mode == 'playback':
            # _setupPlaybackAPI(self.env, self.http, self.manager)
        self.http.run(host='0.0.0.0', port=self.env.local_port)

def _setupPlaybackAPI(env, http, manager):
    @http.route('/files', methods=['GET'])
    def getFiles():
        pbak_files = manager.getPlaybackCatalogue()
        resp = {'success':True, 'files': pbak_files}
        return json.dumps(resp), 200

    @http.route('/playback/start/<filename>', methods=['POST'])
    def startPlayback(filename):
        try:
            pbak_id = manager.startPlayback(filename)
            return json.dumps({'success': True, 'playbackId': pbak_id})
        except Exception,e:
            return json.dumps({'success':False, 'error': str(e)}), 404

def _setupAPI(http, manager):
    @http.route('/playback/<filename>', methods=['POST'])
    def playback(filename):
        manager.startPlayback(filename)
        return json.dumps({'success': True}), 200
        
    @http.route('/<guid>/connect', methods=['POST'])
    def connect(guid):
        logger.info('connection request for guid %s', guid)
        try:
            manager.connectSource(guid)
            return json.dumps({'success': True}), 200
        except Exception,e:
            return json.dumps({'success': False, 'error': str(e)}), 404
    
    @http.route('/<guid>/disconnect', methods=['POST'])
    def disconnect(guid):
        logger.info('connection request for interface %s', guid)
        try:
            manager.disconnectSource(guid)
            return json.dumps({'success': True}), 200
        except Exception,e:
            return json.dumps({'success': False, 'error': str(e)}), 404
