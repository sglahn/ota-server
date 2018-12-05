#!/bin/bash

sudo useradd -r -s /bin/false otaserver

sudo mkdir -p /etc/ota-server
sudo mkdir -p /etc/ota-server/firmware

sudo cp server.py /etc/ota-server

sudo chown -R otaserver:otaserver /etc/ota-server

sudo cp ota-server.service /etc/systemd/system/

sudo systemctl enable ota-server
sudo systemctl start ota-server
