from bson.json_util import dumps
name = 'clearNetwork'
url = '/api/networks/<uuid>/clear'
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
    uuid = path_data['uuid']
    mq_client.publish('clearNetwork', {
        'uuid': uuid,
    })
    return dumps({
        'success': True
    }), 200