from collections import OrderedDict

def create():
    return PacketCounter({
        'total': 0,
        'distribution': {}
    })
class PacketCounter:
    def __init__(self, dct):
        self.total = dct['total']
        self.distribution = dct['distribution']

    def clear(self):
        self.total = 0
        self.distribution = {}

    def serialize(self):
        dct = OrderedDict()
        dct['total'] = self.total
        dct['distribution'] = self.distribution
        return dct

    def add(self, pkttype, count=1):
        if not pkttype in self.distribution:
            self.distribution[pkttype] = 0
        self.total += count
        self.distribution[pkttype] += count
    
    def merge(self, pktCounter):
        for t, c in pktCounter.distribution.items():
            self.add(t, count=c)