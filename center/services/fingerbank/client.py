import json
import httplib

key = '1a59215c58c85c7555523e153e4b991134934587'
host = 'api.fingerbank.org'
api = '/api/v2/combinations/interrogate?key=<key>'
api = api.replace('<key>', key)

def interrogate(device_mac):
    encoded_data = json.dumps({'mac': device_mac}).encode('utf-8')
    headers = {
        "Content-type": "application/json"
    }
    conn = httplib.HTTPSConnection(host)
    conn.request("GET", api, encoded_data, headers)
    response = conn.getresponse()
    data = response.read()
    print data
    return json.loads(data)
    
