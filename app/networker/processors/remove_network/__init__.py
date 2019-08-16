name = 'remove_network'
topic = 'removeNetwork'

NetworkLock = None
logger = None
db_client = None
mq_client = None

def init(mq, db, nlock, lgr):
    global NetworkLock, logger, db_client, mq_client
    mq_client = mq
    db_client = db
    NetworkLock = nlock
    logger = lgr

def process(data):
    global NetworkLock, db_client
    uuid = data['uuid']
    with NetworkLock(uuid):
        db_client.deleteNetwork(uuid)