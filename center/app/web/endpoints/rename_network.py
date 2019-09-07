from bson.json_util import dumps
name = 'renameNetwork'
url = '/api/networks/<uuid>/rename/<name>'
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
    name = path_data['name']
    mq_client.publish('renameNetwork', {
        'uuid': uuid,
        'name': name
    })
    return dumps({
        'success': True
    }), 200