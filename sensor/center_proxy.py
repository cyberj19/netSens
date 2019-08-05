import time
import threading
import httplib
import logging
import json
import interface
from infra.processQueue import ProcessQueue

logger = logging.getLogger('centerProxy')

class CenterProxy:
    def __init__(self, env, broker):
        self.broker = broker
        self.env = env
        self.ip = env.center_ip
        self.port = env.center_port
        self.firstConnection = True
        self.status_cache = {}
        ifaces = interface.getInterfaces()
        if env.comm_iface in ifaces:
            self.mac = ifaces[env.comm_iface]
        else:
            self.mac = env.comm_mac
        self.packetQueue = ProcessQueue(
            'SendPackets',
            procFunc=self._sendPackets,
            broker=broker,
            topic='packet',
            maxCapacity=env.queue_max_packets,
            bulkMode=True,
            requeueOnFail=True,
            errorFunc=lambda e: logger.error(str(e)),
            interval=1
        )

        self.statusQueue = ProcessQueue(
            'statusQueue',
            procFunc=self._updateStatusCache,
            broker=broker,
            topic='status',
            maxCapacity=1,
            bulkMode=False,
            requeueOnFail=False,
            errorFunc=lambda e: logger.error(str(e)),
        )

        self.connected = True
        self.statusThread = threading.Thread(target=self._sendStatus)
        self.statusThread.start()
        logger.info('Center proxy is ready')

    def _updateStatusCache(self, status):
        self.status_cache[status['guid']] = status

    def _sendPackets(self, packets):
        payload = {
            'time': time.time(),
            'mode': self.env.mode,
            'mac': self.mac,
            'packets': packets
        }
        self._send('/packets', payload)

    def stop(self):
        self.connected = False

    def _getStatus(self):
        status_array = []
        for guid in self.status_cache:
            status_array.append(self.status_cache[guid])
        payload = {
            'time': time.time(),
            'mode': self.env.mode,
            'mac': self.mac,
            'port': self.env.local_port,
            'active': True,
            'sources': status_array
        }
        return payload

    def _sendStatus(self):
        logger.info('Starting send status thread')
        while self.connected:
            try:
                payload = self._getStatus()
                logger.debug('Sending status to center')
                self._send('/status', payload)
            except Exception,e :
                logger.error(e)
            finally:
                if not self.connected:
                    break
                time.sleep(5)

    def _send(self, url, data):
        logger.debug('Sending data to %s:%d%s', self.ip, self.port, url)
        encoded_data = json.dumps(data).encode('utf-8')
        headers = {
            "Content-type": "application/json", 
            "Accept": "text/plain"
            }
        conn = httplib.HTTPConnection(self.ip, port=self.port)
        conn.request("POST",url,encoded_data,headers)
        conn.getresponse()
