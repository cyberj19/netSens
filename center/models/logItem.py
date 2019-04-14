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
        return {
            'networkId': self.network_id,
            'time': self.time,
            'source': self.source,
            'type': self.typ,
            'msg': self.msg,
            'priority': self.priority
        }

def loadLogItem(item):
    return LogItem(item['networkId'], item['time'],
                    item['source'],
                    item['type'], item['msg'],
                    item['priority'])