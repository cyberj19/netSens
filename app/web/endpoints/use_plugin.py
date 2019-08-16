from bson.json_util import dumps
name = 'usePlugin'
url = '/api/networks/<net_uuid>/devices/<dev_uuid>/plugins/<plg_uuid>'
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
    plg_uuid = path_data['plg_uuid']
    topic = 'plugin-device-%s' % plg_uuid
    device = db_client.getDevice(net_uuid, dev_uuid)
    if device:
        mq_client.publish(topic, device)
    return dumps({'success':True}), 200
    