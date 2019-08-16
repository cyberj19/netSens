from bson.json_util import dumps
name = 'getNetwork'
url = '/api/networks/<uuid>'
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
    uuid = path_data['uuid']
    network = db_client.db.networks.find_one({'uuid': uuid})
    plugins = db_client.db.plugins.find({})
    if not network:
        logger.warning('request for unknown network %s', uuid)
        return dumps({
            'success': False,
            'error': 'Unknown network with this uuid'
        }), 404
    else:
        return dumps({
            'success': True,
            'plugins': plugins,
            'network': network
        }), 200
    