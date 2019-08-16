name = 'device_extra_data'
topic = 'deviceExtraData'

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
    global mongo, NetworkLock
    net_uuid = data['networkUUID']
    dev_uuid = data['deviceUUID']
    ext_data = data['extraData']
    with NetworkLock(net_uuid) as net:
        if net:
            net.addDeviceData(dev_uuid, ext_data)