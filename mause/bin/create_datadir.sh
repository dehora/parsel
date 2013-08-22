#!/bin/sh

if [ "$(id -u)" != "0" ]; then
   echo "This script can only be run as root" 1>&2
   exit 1
fi

sudo apt-get -y --no-install-recommends install mdadm lvm2

sudo echo 'DEVICE /dev/xvdh1 /dev/xvdh2 /dev/xvdh3 /dev/xvdh4' | sudo tee -a /etc/mdadm.conf
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm.conf


# set the readahead
sudo blockdev --setra 512 /dev/md0
sudo blockdev --setra 512 /dev/xvdh1
sudo blockdev --setra 512 /dev/xvdh2
sudo blockdev --setra 512 /dev/xvdh3
sudo blockdev --setra 512 /dev/xvdh4

sudo pvcreate /dev/md0

#  zero out the device
sudo dd if=/dev/zero of=/dev/md0 bs=512 count=1

sudo vgcreate vg0 /dev/md0
sudo vgdisplay vg0

# logical volume takes the entire array
sudo lvcreate -l 100%FREE -n data vg0

# use xfs
sudo mkfs.xfs /dev/vg0/data -f

# create a dir and plant the raid on it
sudo mkdir /data
echo '/dev/vg0/data /data xfs defaults,auto,noatime,noexec 0 0' | sudo tee -a /etc/fstab

# enable on reboot
sudo perl -ne 'print if $_ !~ /mnt/' /etc/fstab > /etc/fstab.2
sudo echo '#/dev/md0  /mnt  xfs    defaults 0 0' >> /etc/fstab.2
sudo mv /etc/fstab.2 /etc/fstab

#  stop /dev/md0 disappearing on a reboot
sudo update-initramfs -u

sudo mount /data
