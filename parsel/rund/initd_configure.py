#!/usr/bin/env python

import time
import re
import os

from parsel.rund.conf import Config
from parsel import logger
from parsel.rund.raid import RaidInstaller
from parsel.rund.cassandra import CassandraInstaller
from parsel.rund.priam import PriamInstaller


def restart_tasks(config):
    logger.exe('sudo mount -a')
    logger.exe('sudo swapoff --all')
    # Ensure the correct blockdev readahead since this sometimes resets after restarts
    if config.get_config('instance', 'raid_readahead'):
        logger.exe('sudo blockdev --setra %s /dev/md0'
                   % (config.get_config('instance', 'raid_readahead')), expectError=True)


def configure_jmxtrans(ipaddr):
    with open('/home/ubuntu/parsel/parsel/ami/cassandra_jmxtrans.json', 'r') as f:
        json = f.read()
    # todo: fragile
    p = re.compile('"127.0.0.1"')
    json = p.sub('"{0}"'.format(ipaddr), json)
    with open(os.path.join('/var/lib/jmxtrans/', 'cassandra_jmxtrans.json'), 'w') as f:
        f.write(json)
    logger.info('cassandra_jmxtrans.json configured with %s as source host.' % (ipaddr,))
    logger.exe("sudo /etc/init.d/jmxtrans stop")
    time.sleep(8)  # jmxtrans can take a few seconds to stop
    logger.exe("sudo /etc/init.d/jmxtrans start")
    logger.info('jmxtrans restarted.')


def fixup_diamond():
    # fixup for diamond's broken deb file
    logger.exe("sudo mkdir -p /var/run/diamond")
    logger.exe("sudo /etc/init.d/diamond stop")
    time.sleep(4)
    logger.exe("sudo /etc/init.d/diamond start")


def run():
    config = Config()
    if config.get_config("instance", "initial_configuration") != "completed":

        instance_data = config.get_instance_data()
        options = config.parse_supplied_userdata(instance_data)
        config.set_supplied_userdata(options)
        RaidInstaller().install(config)
        CassandraInstaller().install(config, options)
        PriamInstaller().install(config)

        if config.get_config("instance", "perms") != "completed":
            # let priam find yaml
            logger.exe("sudo mkdir -p /etc/cassandra/conf/")
            logger.exe("sudo ln -s /etc/cassandra/cassandra.yaml  /etc/cassandra/conf/cassandra.yaml")

            # cassandra base dirs
            logger.exe("sudo mkdir -p /raid0/cassandra/saved_caches")
            logger.exe("sudo mkdir -p /raid0/cassandra/data")
            logger.exe("sudo mkdir -p /raid0/cassandra/commitlog")
            logger.exe('sudo chown -R cassandra:cassandra /raid0/cassandra/saved_caches')
            logger.exe('sudo chown -R cassandra:cassandra /raid0/cassandra/data')
            logger.exe('sudo chown -R cassandra:cassandra /raid0/cassandra/commitlog')

            # blow away any existing data
            logger.exe("sudo rm -rf /var/lib/cassandra")
            logger.exe("sudo ln  -s /raid0/cassandra  /var/lib/cassandra")
            logger.exe('sudo chown -Rh cassandra:cassandra /var/lib/cassandra')
            logger.info("Linked /var/lib/cassandra to /raid0/cassandra ")

            # give perms back to cassandra and ubuntu
            logger.exe('sudo chown -hR ubuntu:ubuntu /home/ubuntu')
            logger.exe('sudo chown -hR cassandra:cassandra /raid0/cassandra', False)
            logger.exe('sudo chown -hR cassandra:cassandra /mnt/cassandra', False)

            # shared access
            logger.exe("sudo groupadd databas")
            logger.exe("sudo usermod -aG databas cassandra")
            logger.exe("sudo usermod -aG databas tomcat7")
            logger.exe("sudo usermod -aG databas ubuntu")
            logger.exe("sudo chgrp -R databas /raid0/cassandra/")
            logger.exe("sudo chgrp -R databas /var/lib/cassandra/")
            logger.exe("sudo chgrp -R databas /etc/cassandra/")
            logger.exe("sudo chgrp -R databas /var/lib/tomcat7/")
            logger.exe("sudo chgrp -R databas /var/log/tomcat7/")
            logger.exe("sudo chgrp -R databas /var/log/cassandra/")

            # trailing path needed to follow symlinks
            logger.exe("sudo chmod -R g+rwxs,o+rx /raid0/cassandra/")
            logger.exe("sudo chmod -R g+rwxs,o+rx /var/lib/cassandra/")
            logger.exe("sudo chmod -R g+rwxs,o+rx /etc/cassandra/")
            logger.exe("sudo chmod -R g+rwxs,o+rx /var/log/cassandra/")
            logger.exe("sudo chmod -R g+rwxs,o+rx /var/lib/tomcat7/")
            logger.exe("sudo chmod -R g+rwxs,o+rx /var/log/tomcat7/")
            logger.exe("sudo setfacl -R -m d:u::rwx,d:g::rwx,d:m:rwx,d:o:r-x /raid0/cassandra/")
            logger.exe("sudo setfacl -R -m d:u::rwx,d:g::rwx,d:m:rwx,d:o:r-x /var/lib/cassandra/")
            logger.exe("sudo setfacl -R -m d:u::rwx,d:g::rwx,d:m:rwx,d:o:r-x /etc/cassandra/")
            logger.exe("sudo setfacl -R -m d:u::rwx,d:g::rwx,d:m:rwx,d:o:r-x /var/log/cassandra/")
            logger.exe("sudo setfacl -R -m d:u::rwx,d:g::rwx,d:m:rwx,d:o:r-x /var/lib/tomcat7/")
            logger.exe("sudo setfacl -R -m d:u::rwx,d:g::rwx,d:m:rwx,d:o:r-x /var/log/tomcat7/")

            logger.exe("sudo adduser tomcat7 sudo")
            logger.exe("sudo adduser cassandra sudo")

            logger.info("Permissions completed!\n")

            configure_jmxtrans(instance_data['local-ipv4'])
            fixup_diamond()

            config.set_config("instance", "perms", "completed")
        else:
            logger.info('Permissions configuration logged as completed, skipping.')

        restart_tasks(config)
        # priam will start cassandra for us
        logger.exe('sudo service tomcat7 start')
        logger.info("initd_configure.py completed!\n")
        config.set_config("instance", "initial_configuration", "completed")
    else:
        logger.info('Initial configuration logged as completed, skipping.')
        # in case we are rebooting
        restart_tasks(config)


run()
