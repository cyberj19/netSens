from collections import OrderedDict

class LogItem:
    network_id  = -1
    time        = 0
    source      = ''
    typ         = ''
    msg         = ''
    priority    = 0
    def __init__(self, network_id, time, source, typ, msg, priority):
        self.network_id = network_id
        self.time = time
        self.source = source
        self.typ = typ
        self.msg = msg
        self.priority = priority
    
    def serialize(self):
        dct = OrderedDict()
        dct['networkId'] = self.network_id,
        dct['time'] = self.time,
        dct['source'] = self.source,
        dct['type'] = self.typ,
        dct['msg'] = self.msg,
        dct['priority'] = self.priority
        return dct

def loadLogItem(item):
    return LogItem(item['networkId'], item['time'],
                    item['source'],
                    item['type'], item['msg'],
                    item['priority'])
