#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [[ ! -z `pgrep python` ]]; then
sudo kill -9 $(pgrep python)
echo "killing python"
fi
if [[ ! -z `pgrep linux2_live` ]]; then
sudo kill -9 $(pgrep linux2_live)
echo "killing listener"
fi
cd  $(pwd)/center
python center.py playback >> /var/log/netsens/center.log 2>&1 &
echo "run center"
cd ../sensor
python sensor.py playback >> /var/log/netsens/sensor.log 2>&1 &
echo "run sensor"
cd ../netSens
python -m SimpleHTTPServer 2000 >> /var/log/netsens/bootstrap.log 2>&1 &
echo "run graph"
