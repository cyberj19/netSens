import env
import json
from mqtt_client import MQTTClient
from processQueue import ProcessQueue
from db import DB

mqtt = MQTTClient(env)
mongo = DB(env)


def writePackets(packets):
    mongo.db['packets'].insert_many(packets)

def writeNetwork(network):
    mongo.db['networks'].update_one(
        {'id': network['id']},
        {'$set': network},
        upsert=True
    )

ProcessQueue(
    'PacketWriter',
    writePackets,
    bulkMode=True,
    preFunc=lambda p: json.loads(p),
    broker=mqtt,
    topic='packetUpdate'
)
ProcessQueue(
    'NetworkWriter',
    writeNetwork,
    preFunc=lambda n: json.loads(n),
    broker=mqtt,
    topic='networkUpdate'
)