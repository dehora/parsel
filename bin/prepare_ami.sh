#!/bin/sh

export PYTHONPATH=${PYTHONPATH}:/home/ubuntu/parsel
PYTHONPATH=${PYTHONPATH}:/home/ubuntu/parsel
sudo mkdir -p /var/log/parsel
chown -R ubuntu:ubuntu /var/log/parsel
cd /home/ubuntu/parsel
git checkout $(head -n 1 parsel/ami/branch)
cd /home/ubuntu/parsel/parsel/ami
python prepare_ami
cd /home/ubuntu/parsel/
