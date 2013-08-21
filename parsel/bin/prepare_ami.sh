#!/bin/sh

sudo apt-get -y install python-setuptools
sudo easy_install pip
sudo pip install fabric

export PYTHONPATH=${PYTHONPATH}:/home/ubuntu/parsel
PYTHONPATH=${PYTHONPATH}:/home/ubuntu/parsel
sudo mkdir -p /var/log/parsel
chown -R ubuntu:ubuntu /var/log/parsel
cd /home/ubuntu/parsel
git checkout $(head -n 1 parsel/ami/branch)
cd /home/ubuntu/parsel/parsel/ami
echo  "jmxtrans: $1"
echo  "jmxtrans uri: $2"
echo  "jmxtrans file: $3"
echo  "java uri: $4"
echo  "java file: $5"
echo  "java rev: $6"
python prepare_ami -j $1 -k $2 -l $3 -m $4 -n $5 -o $6
cd /home/ubuntu/parsel/
