#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt-get install python-pip
pip install flask
apt-get install libpcap0.8-dev
cd sensor/sources
make
cd -
