from collections import OrderedDict
import uuid
import time

def create(idx, network_id, msg):
    return Alert({
        'idx': idx,
        'uuid': 'alert-%s' % uuid.uuid4().hex,
        'networkId': network_id,
        'time': time.time(),
        'message': msg
    })
class Alert:
    def __init__(self, dct):
        self.idx = dct['idx']
        self.uuid = dct['uuid']
        self.network_id = dct['networkId']
        self.time = dct['time']
        self.message = dct['message']
        
    def serialize(self):
        dct = OrderedDict()
        dct['idx'] = self.idx
        dct['uuid'] = self.uuid
        dct['networkId'] = self.network_id
        dct['time'] = self.time
        dct['message'] = self.message
        return dct