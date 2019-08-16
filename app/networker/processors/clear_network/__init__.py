name = 'clear_network'
topic = 'clearNetwork'

NetworkLock = None
logger = None
mongo = None
mqtt = None

def init(mq, mng, nlock, lgr):
    global NetworkLock, logger, mongo, mqtt
    mqtt = mq
    mongo = mng
    NetworkLock = nlock
    logger = lgr

def process(data):
    global NetworkLock, mongo
    uuid = data['uuid']
    with NetworkLock(uuid) as net:
        if net:
            net.clear()