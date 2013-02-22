cd ~
mkdir ec2
cd ec2

curl http://s3.amazonaws.com/ec2-downloads/ec2-api-tools.zip > ec2-api-tools.zip
curl http://s3.amazonaws.com/ec2-downloads/ec2-ami-tools.zip > ec2-ami-tools.zip

unzip ec2-api-tools.zip
unzip ec2-ami-tools.zip

ln -s ec2-ami-tools-* current-ec2-ami-tools
ln -s ec2-api-tools-* current-ec2-api-tools

echo "export EC2_AMITOOL_HOME=~/ec2/current-ec2-ami-tools" >> ~/.bashrc
echo "export EC2_APITOOL_HOME=~/ec2/current-ec2-api-tools" >> ~/.bashrc
echo "export PATH=${PATH}:~/ec2/current-ec2-ami-tools/bin:~/ec2/current-ec2-api-tools/bin" >> ~/.bashrc

cd ~

source ~/.bashrc
