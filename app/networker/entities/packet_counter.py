from collections import OrderedDict
import models

class PacketCounter(models.Model):
    @classmethod
    def create(cls):
        return PacketCounter({
            'total': 0,
            'distribution': {}
        })

    def __init__(self, packetCounter):
        super(PacketCounter, self).__init__(
            schema_file='packet_counter.json', 
            data=packetCounter
            )

    def clear(self):
        self.total = 0
        self.distribution = {}

    def add(self, pkttype, count=1):
        if not pkttype in self.distribution:
            self.distribution[pkttype] = 0
        self.total += count
        self.distribution[pkttype] += count
    
    def merge(self, pktCounter):
        for t, c in pktCounter.distribution.items():
            self.add(t, count=c)