from bson.json_util import dumps
name = 'analyzeDevice'
url = '/api/networks/<net_uuid>/devices/<dev_uuid>/analyze'
methods = ['GET']
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
    packets = db_client.getDevicePackets(net_uuid, dev_uuid)
    return dumps({'success':True, 'packets': packets})
    