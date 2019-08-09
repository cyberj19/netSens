services:
--mongo db server
--mosquitto server

python dependencies:
--dpkt
--flask
--pymongo
--paho

how to run in localhost:
--run mongo server on localhost with port 27017
--run mosquitto server on localhost with port 1883
--run "python networker.py" from app/networker
--run "python playback.py" from app/playback
--run "python web.py" from app/web
--app will be available on port 8000

basic usage:
--goto localhost:8000
--upload a pcap file on the main page
--explore the create network by clicking "view" in the main page