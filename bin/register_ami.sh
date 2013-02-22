AWSID=$1
AWS_ACCESS_KEY=$2
AWS_SECRET_KEY=$3

sudo rm /var/log/parsel/parsel.log
sudo mv /home/ubuntu/*.pem /mnt

CERT_PEM=/mnt/cert-*.pem
PK_PEM=/mnt/pk-*.pem
VERSION=$(head -1 /home/ubuntu/parsel/version)
AMINAME=cassandra_ami_$VERSION
MANIFEST=/mnt/$AMINAME.manifest.xml
S3BUCKET=viscis-machine

rm -rf ~/.bash_history
history -c

ec2-bundle-vol -p $AMINAME -d /mnt -k $PK_PEM -c $CERT_PEM -u $AWSID -r x86_64

REGION=EU;              yes | ec2-upload-bundle -m $MANIFEST -a $AWS_ACCESS_KEY -s $AWS_SECRET_KEY -b $S3BUCKET --location $REGION
#REGION=US;              yes | ec2-upload-bundle -m $MANIFEST -a $AWS_ACCESS_KEY -s $AWS_SECRET_KEY -b $S3BUCKET-$REGION --location $REGION
#REGION=us-west-1;       yes | ec2-upload-bundle -m $MANIFEST -a $AWS_ACCESS_KEY -s $AWS_SECRET_KEY -b $S3BUCKET-$REGION --location $REGION
#REGION=us-west-2;       yes | ec2-upload-bundle -m $MANIFEST -a $AWS_ACCESS_KEY -s $AWS_SECRET_KEY -b $S3BUCKET-$REGION --location $REGION

export EC2_HOME=/root/ec2/current-ec2-api-tools
export JAVA_HOME=/opt/java/64/jdk1.6.0_38

ec2-register $S3BUCKET/$AMINAME.manifest.xml -region eu-west-1 -n "Cassandra AMI $VERSION" -d "Starts a Priam managed Cassandra Server" -O $AWS_ACCESS_KEY -W $AWS_SECRET_KEY
#ec2-register $S3BUCKET/$AMINAME.manifest.xml -region us-west-1 -n "Cassandra AMI $VERSION" -d "Starts a Priam managed Cassandra Server" -O $AWS_ACCESS_KEY -W $AWS_SECRET_KEY
#ec2-register $S3BUCKET/$AMINAME.manifest.xml -region us-west-2 -n "Cassandra AMI $VERSION" -d "Starts a Priam managed Cassandra Server" -O $AWS_ACCESS_KEY -W $AWS_SECRET_KEY
