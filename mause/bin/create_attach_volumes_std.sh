#!/bin/sh
instance_id=$1
volume_size=$2
volume_zone=$3
qua=`date +"%Y%m%d_%H%M%S"`
vol_file="/tmp/vols_$1_$2_$volume_zone_$qua.txt"

for x in {1..4}; do  ec2-create-volume --size $volume_size --type standard --availability-zone $volume_zone; done >> $vol_file

(i=0; \
for vol in $(awk '{print $2}' $vol_file); do \
  i=$(( i + 1 )); \
  ec2-attach-volume $vol -i $instance_id -d /dev/sdh${i}; \
done)

echo "Volume details saved to $vol_file:"
cat $vol_file
echo