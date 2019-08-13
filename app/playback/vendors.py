import logging

logger = logging.getLogger('playback')

vendor_file = 'mac_vendor'
with open(vendor_file,'r') as fp:
    vendor_data = fp.readlines()
vendors = {}
for vnd in vendor_data:
    vnd_parts = vnd.split('\t')
    vendors[vnd_parts[0].strip()] = vnd_parts[1].strip()
logger.info('Loaded vendors file: %d records', len(vendor_data))

def getVendor(macAddress):
    if not macAddress:
        return None
    macAddr_nc = macAddress.replace(':','')
    macAddr_nc = macAddr_nc[:6]
    if not macAddr_nc in vendors:
        return None
    return None #vendors[macAddr_nc]
