import json
import httplib

key = '1a59215c58c85c7555523e153e4b991134934587'
host = 'api.fingerbank.org'
api = '/api/v2/combinations/interrogate?key=<key>'
api = api.replace('<key>', key)

def __mac__interrogate(device_mac):
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
    

def interrogate(dhcp_fp):
    encoded_data = json.dumps({'dhcp_fingerprint': str(dhcp_fp[0])[1:-1].replace(" ","")}).encode('utf-8')
    headers = {
        "Content-type": "application/json"
    }
    conn = httplib.HTTPSConnection(host)
    conn.request("GET", api, encoded_data, headers)
    response = conn.getresponse()
    data = response.read()
    print data
    return json.loads(data)

if __name__=="__main__":
	#interrogate("1,3,6,15,26,28,51,58,59,43")
	interrogate("252,3,42,15,6,1")
    
