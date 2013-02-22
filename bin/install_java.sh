#!/bin/sh

JDKBIN="jdk-6u38-linux-x64.bin"
JDKV="jdk1.6.0_38"
BASEPATH="/opt/java/64"
JDKPATH="$BASEPATH/$JDKV"

sudo wget https://s3.amazonaws.com/viscis-archive/$JDKBIN
sudo mkdir -p $BASEPATH
sudo mv $JDKBIN $BASEPATH
sudo cd $BASEPATH
sudo chmod +x $JDKBIN
sudo ./$JDKBIN
sudo update-alternatives --install "/usr/bin/java" "java" "$JDKPATH/java" 1
sudo update-alternatives --set java $JDKPATH/bin/java
sudo export JAVA_HOME=$JDKPATH
sudo rm -rf ~/.bash_history && history -c