import threading
from entities import network
import contextlib

mongo = None
network_locks = {}
llock = threading.Lock()

def init(mng):
    global mongo
    mongo = mng

@contextlib.contextmanager
def lock(uuid):
    global network_locks, llock
    global mongo
    with llock:
        if not uuid in network_locks:
            network_locks[uuid] = threading.Lock()
    with network_locks[uuid]:
        network_data = mongo.db['networks'].find_one({'uuid': uuid})
        if not network_data:
            net = None
        else:
            net = network.Network(network_data)
        yield net
        if net:
            mongo.saveNetwork(net.serialize())

@contextlib.contextmanager
def device_lock(netUUID, devUUID):
    with lock(netUUID) as net:
        if net:
            dev = net.findDevice(devUUID)
            if dev:
                yield dev
                