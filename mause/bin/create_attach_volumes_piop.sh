#!/bin/sh
instance_id=$1
volume_size=$2
volume_iops=$3
qua=`date +"%Y%m%d_%H%M%S"`

for x in {1..4}; do  ec2-create-volume --size $volume_size --type io1 --iops $volume_iops  --availability-zone  eu-west-1a; done >> /tmp/vols_$qua.txt

(i=0; \
for vol in $(awk '{print $2}' /tmp/vols_$qua.txt); do \
  i=$(( i + 1 )); \
  ec2-attach-volume $vol -i $instance_id -d /dev/sdh${i}; \
done)

echo "Volume details saved to /tmp/vols_$qua.txt:"
cat /tmp/vols_$qua.txt
echo "In Ubuntu these volumes will appear as /dev/xvdh*"
echo