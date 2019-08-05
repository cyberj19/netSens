from infra import ProcessQueue
import client

_broker = None

def setup(broker):
    global _broker
    _broker = broker
    ProcessQueue(
        'FingerBankQueue',
        processDevice,
        errorFunc=lambda e: printError(e),
        broker=broker,
        topic='fingerBankAnalysis'
    )
def printError(err):
    print str(err)
def processDevice(device):
    global _broker
    if not device:
        return
    if not device.dhcp_fp:
        return
    device_data = client.interrogate(device.dhcp_fp)
    if 'errors' in device_data:
        return
    _broker.emit('manualOper', {
        'type': 'addDeviceData',
        'networkId': device.network_id,
        'deviceId': device.id,
        'data': {
            'OS': device_data['device']['name']
        }
    })