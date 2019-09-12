# netSens


netSens is a system for collecting, processing and presenting network information for the benefit of online and offline communication network analysis, all in a passive and secretive manner.


* Written in Python and JavaScript.
* Based on open shelf products.
* Generic and modular-oriented development - an infrastructure that allows easy integration of new capabilities within the product and interfaces with external services.

## Features

- Cross-Platform (Linux, Windows)
- Event-oriented Pub / Sub architecture
- Web-based UI
- Agent for online data collection
- Pcap upload system for offline data analysis


<img src="https://github.com/cyberj19/netsens/blob/master/netsens.jpg" alt="Screenshot of netsens" width="560"/>




## services:
- mongo db server
- mosquitto server

## python dependencies:
- dpkt
- flask
- pymongo
- paho

## how to run in localhost (Windows):
- use run_public.bat file to start up the system
- app will be available on port 8000

## basic usage:
- goto localhost:8000
- upload a pcap file on the main page
- explore the created network by going to networks tab. use filter if needed.
