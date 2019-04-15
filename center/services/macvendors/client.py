
import httplib

host = 'api.macvendors.com'

def interrogate(device_mac):
    api = "/%s"%device_mac
    conn = httplib.HTTPSConnection(host)
    conn.request("GET", api)
    response = conn.getresponse()
    data = response.read()
    print data
    return data

#interrogate("00:21:6A:C0:38:F2")

