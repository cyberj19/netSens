from flask import request
from bson.json_util import dumps
import uuid
import os
name = 'playback'
pbak_folder = '../data/playback'
url = '/api/playback'
methods = ['POST']
db_client = None
mq_client = None
logger = None
env = None

def init(dbClient, mqClient, lgr):
    global db_client, mq_client, logger, env
    db_client = dbClient
    mq_client = mqClient
    logger = lgr

def handle(path_data, request_data):
    if 'file' not in request_data.files:
        logger.error('No file in request')
        return dumps({'success': False, 'error': 'No file selected'}), 400
    file = request_data.files['file']
    if file.filename == '':
        logger.error('No file in request')
        return dumps({'success': False, 'error': 'No file selected'}), 400
    fileparts = file.filename.split('.')
    filename = '%s-%s.%s' % (fileparts[0], uuid.uuid4().hex, fileparts[1])
    logger.info('uploading file: %s', filename)
    file.save(os.path.join(pbak_folder, filename))
    mq_client.publish('playbackRequest', {'file':filename})
    return dumps({'success': True}), 200
