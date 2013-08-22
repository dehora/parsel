#!/bin/sh


echo && echo "Packer ENV"
echo "---------------------------------------------------------------"
echo "JMXTRANS_URL $JMXTRANS_URL"
echo "JMXTRANS_FILE $JMXTRANS_FILE"
echo "GRAPHITE_HOST $GRAPHITE_HOST"
echo "PUPPET_HOST $PUPPET_HOST"
echo "KAFKA_VERSION $KAFKA_VERSION"
echo "KAFKA_URL KAFKA_URL"
echo "KAFKA_FILE $KAFKA_FILE"


echo && echo "apt-get all the things"
echo "---------------------------------------------------------------"
echo "deb http://archive.canonical.com/ precise partner" | sudo tee -a /etc/apt/sources.list.d/java.sources.list
sudo apt-get -y update
sudo apt-get -y install --fix-missing facter
sudo apt-get -y install --fix-missing libjna-java
sudo apt-get -y install --fix-missing crashmail
sudo apt-get -y install --fix-missing htop
sudo apt-get -y install --fix-missing sysstat
sudo apt-get -y install --fix-missing iftop
sudo apt-get -y install --fix-missing binutils
sudo apt-get -y install --fix-missing pssh
sudo apt-get -y install --fix-missing pbzip2
sudo apt-get -y install --fix-missing xfsprogs
sudo apt-get -y install --fix-missing zip
sudo apt-get -y install --fix-missing unzip
sudo apt-get -y install --fix-missing ruby
sudo apt-get -y install --fix-missing openssl
sudo apt-get -y install --fix-missing libopenssl-ruby
sudo apt-get -y install --fix-missing curl
sudo apt-get -y install --fix-missing ntp
sudo apt-get -y install --fix-missing python-pip
sudo apt-get -y install --fix-missing python-setuptools
sudo apt-get -y install --fix-missing tree
sudo apt-get -y install acl
sudo apt-get -y install policykit-1
sudo apt-get -y install ca-certificates-java
sudo apt-get -y install jsvc
sudo apt-get -y install libjna-java
sudo apt-get -y install tzdata-java
sudo apt-get -y install ntp
sudo apt-get -y --no-install-recommends install lvm2
sudo apt-get -y --no-install-recommends install mdadm

echo && echo "Using European TZ servers"
echo "---------------------------------------------------------------"
echo "server 0.ie.pool.ntp.org" | sudo tee -a /etc/ntp.conf
echo "server 1.ie.pool.ntp.org" | sudo tee -a /etc/ntp.conf
echo "server 2.ie.pool.ntp.org" | sudo tee -a /etc/ntp.conf
echo "server 3.ie.pool.ntp.org" | sudo tee -a /etc/ntp.conf
echo "server 3.ie.pool.ntp.org" | sudo tee -a /etc/ntp.conf
sudo service ntp restart


echo && echo "Installing pip modules"
echo "---------------------------------------------------------------"
sudo pip install superlance
sudo pip install fabric


echo && echo "Installing JMXTrans"
echo "---------------------------------------------------------------"
sudo wget  --no-check-certificate --output-document $JMXTRANS_FILE $JMXTRANS_URL
export DEBIAN_FRONTEND=noninteractive
sudo -E dpkg -i $JMXTRANS_FILE


echo && echo "Installing Parsel"
echo "---------------------------------------------------------------"
mv /tmp/parsel.tar.gz /home/ubuntu
cd /home/ubuntu
tar xvf parsel.tar.gz
sudo chown -R ubuntu:ubuntu /home/ubuntu/parsel
tree /home/ubuntu/parsel


echo && echo "Configuring Limits"
echo "---------------------------------------------------------------"
echo "* soft nofile 32768" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 32768" | sudo tee -a /etc/security/limits.conf
echo "root soft nofile 32768" | sudo tee -a /etc/security/limits.conf
echo "root hard nofile 32768" | sudo tee -a /etc/security/limits.conf


echo && echo "Configuring Graphite Host"
echo "---------------------------------------------------------------"
sudo echo "$GRAPHITE_HOST    graphite.server.pri" | sudo tee -a /etc/hosts
sudo echo "$GRAPHITE_HOST    graphite" | sudo tee -a /etc/hosts


echo && echo "Configuring Puppet Host"
echo "---------------------------------------------------------------"
sudo echo "$PUPPET_HOST    puppet.server.pri" | sudo tee -a /etc/hosts
sudo echo "$PUPPET_HOST    puppet" | sudo tee -a /etc/hosts


echo && echo "Configuring .profile"
echo "---------------------------------------------------------------"
sudo chmod 777 /home/ubuntu/.profile
sudo echo "python parsel/parsel/rund/motd.py" | sudo tee -a  /home/ubuntu/.profile
sudo echo "export PYTHONPATH=\${PYTHONPATH}:/home/ubuntu/parsel" | sudo tee -a  /home/ubuntu/.profile
sudo chmod 644 /home/ubuntu/.profile


echo && echo "Configuring .bashrc"
echo "---------------------------------------------------------------"
sudo chmod 777 /home/ubuntu/.bashrc
sudo echo "export PYTHONPATH=\${PYTHONPATH}:/home/ubuntu/parsel" | sudo tee -a  /home/ubuntu/.bashrc
sudo chmod 644 /home/ubuntu/.bashrc


echo && echo "Configuring parsel log dir"
echo "---------------------------------------------------------------"
sudo mkdir -p /var/log/parsel
sudo chown -hR ubuntu:ubuntu /var/log/parsel


echo && echo "Installing Kafka $KAFKA_VERSION"
echo "---------------------------------------------------------------"
sudo wget  --no-check-certificate --output-document $KAFKA_FILE $KAFKA_URL
sudo -E dpkg -i $KAFKA_FILE
# disable this as we'll manage kafka with supervisord
sudo update-rc.d -f kafka-server remove


echo && echo "Configuring /etc/init.d/init-parsel-kafka.sh"
echo "---------------------------------------------------------------"
sudo mv /tmp/init-parsel-kafka.sh /etc/init.d/
sudo chmod 777 /etc/init.d/init-parsel-kafka.sh
sudo chmod 755 /etc/init.d/init-parsel-kafka.sh
sudo update-rc.d -f init-parsel-kafka.sh start 99 2 3 4 5 .
