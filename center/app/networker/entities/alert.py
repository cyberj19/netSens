import uuid
import time
import models

class Alert(models.Model):
    @classmethod
    def create(cls, idx, network_id, msg):
        return Alert({
            'idx': idx,
            'uuid': 'alert-%s' % uuid.uuid4().hex,
            'networkId': network_id,
            'time': time.time(),
            'message': msg
        })

    def __init__(self, alrt=None):
        super(Alert, self).__init__(schema_file='alert.json', data=alrt)