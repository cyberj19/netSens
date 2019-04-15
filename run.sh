#!/bin/bash

if [[ ! -z `pgrep python` ]]; then
sudo kill -9 $(pgrep python)
echo "killing python"
fi
if [[ ! -z `pgrep linux2_listener` ]]; then
sudo kill -9 $(pgrep linux2_listener)
echo "killing listener"
fi
cd  $(pwd)/center
python center.py >> /var/log/netsens/center.log 2>&1 &
echo "run center"
cd $(pwd)/sensor
python sensor.py >> /var/log/netsens/sensor.log 2>&1 &
echo "run sensor"
