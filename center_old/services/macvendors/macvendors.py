from infra import ProcessQueue
import client
import logging

_broker = None
logger=logging.getLogger('main')

def setup(broker):
    global _broker
    _broker = broker
    ProcessQueue(
        'MacVandorsQueue',
        processDevice,
        errorFunc=lambda e: printError(e),
        broker=broker,
        topic='macVendorsLookup'
    )
def printError(err):
    print str(err)
def processDevice(device):
    global _broker
    if not device:
        return
    if not device.mac:
        return
    device_vendor = client.interrogate(device.mac)
    if 'errors' in device_vendor:
        return
    logger.debug("macvendors: %s is %s",device.mac, device_vendor)
    _broker.emit('manualOper', {
        'type': 'addDeviceData',
        'networkId': device.network_id,
        'deviceId': device.id,
        'data': {
            'Vendor': device_vendor
        }
    })
