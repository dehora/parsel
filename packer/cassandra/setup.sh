#!/bin/sh


echo && echo "Packer ENV"
echo "---------------------------------------------------------------"
echo "CASSANDRA_DEB_VERSION $CASSANDRA_DEB_VERSION"
echo "JMXTRANS_URL $JMXTRANS_URL"
echo "JMXTRANS_FILE $JMXTRANS_FILE"
echo "GRAPHITE_HOST $GRAPHITE_HOST"
echo "PUPPET_HOST $PUPPET_HOST"
echo "PRIAM_WAR_URL $PRIAM_WAR_URL"
echo "PRIAM_WAR_FILE $PRIAM_WAR_FILE"
echo "PRIAM_JAR_URL $PRIAM_JAR_URL"
echo "PRIAM_JAR_FILE $PRIAM_JAR_FILE"

export CASSANDRA_VERSION="$CASSANDRA_DEB_VERSION"

echo && echo "apt-get all the things"
echo "---------------------------------------------------------------"
echo "deb http://archive.canonical.com/ precise partner" | sudo tee -a /etc/apt/sources.list.d/java.sources.list
sudo apt-get -y update
sudo apt-get -y install --fix-missing facter
sudo apt-get -y install --fix-missing libjna-java
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
sudo apt-get -y install --fix-missing maven2
sudo apt-get -y install --fix-missing ant
sudo apt-get -y install --fix-missing liblzo2-dev
sudo apt-get -y install --fix-missing ntp
sudo apt-get -y install --fix-missing subversion
sudo apt-get -y install --fix-missing python-pip
sudo apt-get -y install --fix-missing tree
sudo apt-get -y install acl
sudo apt-get -y install policykit-1
sudo apt-get -y install ca-certificates-java
#sudo apt-get -y install icedtea-6-jre-cacao
#sudo apt-get -y install java-common
sudo apt-get -y install jsvc
#sudo apt-get -y install libavahi-client3
#sudo apt-get -y install libavahi-common-data
#sudo apt-get -y install libavahi-common3
#sudo apt-get -y install libcommons-daemon-java
#sudo apt-get -y install libcups2
sudo apt-get -y install libjna-java
#sudo apt-get -y install libjpeg62
#sudo apt-get -y install liblcms1
#sudo apt-get -y install libnspr4-0d
#sudo apt-get -y install libnss3-1d
sudo apt-get -y install tzdata-java
sudo apt-get -y install ntp
sudo apt-get -y install tomcat7
sudo apt-get -y --no-install-recommends install mdadm


echo && echo "Stopping Tomcat, using Java7 "
echo "---------------------------------------------------------------"
sudo service tomcat7 stop
echo "JAVA_HOME=\"/usr/local/java/jdk1.7.0_07\"" | sudo tee -a /etc/default/tomcat7


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


echo && echo "Installing Cassandra"
echo "---------------------------------------------------------------"
sudo gpg --keyserver pgp.mit.edu --recv-keys 2B5C1B00
sudo gpg --export --armor 2B5C1B00 | sudo apt-key add -
sudo gpg --keyserver pgp.mit.edu --recv-keys F758CE318D77295D
sudo gpg --export --armor F758CE318D77295D | sudo apt-key add -
sudo rm /etc/apt/sources.list.d/apache_cassandra.sources.list
echo "deb http://www.apache.org/dist/cassandra/debian $CASSANDRA_VERSION main" | sudo tee -a /etc/apt/sources.list.d/apache_cassandra.sources.list
echo "deb-src http://www.apache.org/dist/cassandra/debian $CASSANDRA_VERSION main" | sudo tee -a /etc/apt/sources.list.d/apache_cassandra.sources.list
sudo apt-get update
sudo apt-get -y --force-yes install cassandra


# the deb starts c* which assigns itself a random token, disable/clean
echo && echo "Stopping Cassandra, to let Priam manage tokens"
echo "---------------------------------------------------------------"
sudo service cassandra stop


echo && echo "Removing Cassandra data"
echo "---------------------------------------------------------------"
sudo rm -rf /var/lib/cassandra/data/system/*
sudo rm -rf /var/lib/cassandra/commitlog/*
sudo rm -rf /var/log/cassandra/*


echo && echo "Installing Priam"
echo "---------------------------------------------------------------"
sudo wget --no-check-certificate --output-document $PRIAM_JAR_FILE $PRIAM_JAR_URL
sudo mv $PRIAM_JAR_FILE/usr/share/cassandra/lib/$PRIAM_JAR_FILE
echo "JVM_OPTS=\"\$JVM_OPTS -javaagent:/usr/share/cassandra/lib/$PRIAM_JAR_FILE\"" | sudo tee -a /etc/cassandra/cassandra-env.sh
sudo cat /etc/cassandra/cassandra-env.sh
sudo wget --no-check-certificate --output-document $PRIAM_WAR_FILE $PRIAM_WAR_URL
sudo mv $PRIAM_WAR_FILE /var/lib/tomcat7/webapps/Priam.war
sudo mv /tmp/awscredential.properties /etc/

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


echo && echo "Configuring /etc/init.d/init-parsel-cassandra.sh"
echo "---------------------------------------------------------------"
sudo mv /tmp/init-parsel-cassandra.sh /etc/init.d/
sudo chmod 777 /etc/init.d/init-parsel-cassandra.sh
sudo chmod 755 /etc/init.d/init-parsel-cassandra.sh
sudo update-rc.d -f init-parsel-cassandra.sh start 99 2 3 4 5 .
