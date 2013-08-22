#!/bin/sh

### BEGIN INIT INFO
# Provides:
# Required-Start:    $remote_fs $syslog
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: Start AMI Configurations on boot.
# Description:       Enables AMI Configurations on startup.
### END INIT INFO

export PYTHONPATH=${PYTHONPATH}:/home/ubuntu/parsel
sudo su -c 'ulimit -n 32768'
sudo mkdir -p /etc/parsel
sudo mkdir -p /var/log/parsel
sudo touch /etc/parsel/parsel.conf
sudo chown -R ubuntu:ubuntu /etc/parsel
sudo chown -R ubuntu:ubuntu /var/log/parsel

echo 1 | sudo tee /proc/sys/vm/overcommit_memory

if [ -d "/data" ]; then
    sudo blockdev --setra 512 /dev/md0
    sudo blockdev --setra 512 /dev/xvdh1
    sudo blockdev --setra 512 /dev/xvdh2
    sudo blockdev --setra 512 /dev/xvdh3
    sudo blockdev --setra 512 /dev/xvdh4
fi

sudo mount -a
sudo swapoff --all

echo "\n -------------------------------------\n" >> /var/log/parsel/parsel.log
cd /home/ubuntu/parsel/mause/rund
python initd_configure.py