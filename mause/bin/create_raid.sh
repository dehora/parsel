#!/bin/sh

if [[ $EUID -ne 0 ]]; then
   echo "This script can only be run as root" 1>&2
   exit 1
fi

yes | mdadm --verbose --create /dev/md0 --level=10 --chunk=256 --raid-devices=4 /dev/xvdh1 /dev/xvdh2 /dev/xvdh3 /dev/xvdh4
