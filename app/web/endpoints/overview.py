from bson.json_util import dumps
name = 'overview'
url = '/api/overview'
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
    networks = db_client.getNetworksOverview()
    monitor = db_client.db.monitor.find()
    jobs = db_client.db.jobs.find({'finished':False})
    return dumps({
        'success': True,
        'networks': networks,
        'monitor': monitor,
        'jobs': jobs
    }), 200
    