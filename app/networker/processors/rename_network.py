name = 'rename_network'
topic = 'renameNetwork'

NetworkLock = None
logger = None

def init(mq, db, nlock, lgr):
    global NetworkLock, logger
    NetworkLock = nlock
    logger = lgr

def process(data):
    global NetworkLock
    uuid = data['uuid']
    name = data['name']
    with NetworkLock(uuid) as net:
        if net:
            net.name = name