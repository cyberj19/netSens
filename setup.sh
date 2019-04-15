#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ -n "$(which apt-get 2>/dev/null)" ]
  then apt-get install python-pip libpcap-dev -y
else if [ -n "$(which yum 2>/dev/null)" ]
  then yum install python-pip libpcap-devel.$(arch) -y
fi
fi

pip install flask
cd $(pwd)/sensor/sources
make
cd -
mkdir -p /var/log/netsens
