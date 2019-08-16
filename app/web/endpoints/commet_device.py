from flask import request
from bson.json_util import dumps
name = 'commentDevice'
url = '/api/networks/<net_uuid>/devices/<dev_uuid>/comment'
methods = ['POST']
db_client = None
mq_client = None
logger = None

def init(dbClient, mqClient, lgr):
    global db_client, mq_client, logger
    db_client = dbClient
    mq_client = mqClient
    logger = lgr

def handle(path_data, request_data):
    net_uuid = path_data['net_uuid']
    dev_uuid = path_data['dev_uuid']
    req = request_data.json
    mq_client.publish(
        'deviceExtraData',
        {
            'networkUUID': net_uuid,
            'deviceUUID': dev_uuid,
            'extraData': {'comment': req['comment']}
        }
    )
    return dumps({'success':True}), 200