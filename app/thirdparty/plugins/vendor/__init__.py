import json

logger = None
name = 'Vendor'
uuid = 'vendor-123'
level = 'device'

vendor_file = 'thirdparty/plugins/vendor/mac_vendor'
with open(vendor_file,'r') as fp:
    vendor_data = fp.readlines()
vendors = {}
for vnd in vendor_data:
    vnd_parts = vnd.split('\t')
    vendors[vnd_parts[0].strip()] = vnd_parts[1].strip()

def setLogger(lgr):
    global logger
    logger = lgr

def processDevice(device, manual=False):
    logger.info('processing device: %s', device['mac'])
    vendor = getVendorFromFile(device['mac'])
    if not vendor:
        if not manual:
            return None
        else:
            vendor = getVendorFromAPI(device['mac'])
            if not vendor:
                return None
    
    return {
        'vendor': vendor
    }
    
import httplib

host = 'api.macvendors.com'

def isAPIError(data):
    try:
        json.loads(data)
        return True
    except Exception:
        return False

def getVendorFromAPI(macAddress):
    api = "/%s" % macAddress
    conn = httplib.HTTPSConnection(host)
    conn.request("GET", api)
    response = conn.getresponse()
    data = response.read()
    if isAPIError(data):
        logger.error('API ERROR')
        return None
    return data

def getVendorFromFile(macAddress):
    if not macAddress:
        return None
    macAddr_nc = macAddress.replace(':','')
    macAddr_nc = macAddr_nc[:6]
    if not macAddr_nc in vendors:
        return None
    return vendors[macAddr_nc]
