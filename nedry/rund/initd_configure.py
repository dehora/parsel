#!/usr/bin/env python

import time
import re
import os

from nedry.rund.conf import Config
from nedry import logger
from nedry.rund.raid import RaidInstaller


def restart_tasks_on_reboot(config):
    disk_tasks(config)


def disk_tasks(config):
    logger.exe('sudo mount -a')
    logger.exe('sudo swapoff --all')
    # Ensure the correct blockdev readahead since this sometimes resets after restarts
    if config.get_config('instance', 'raid_readahead'):
        logger.exe('sudo blockdev --setra %s /dev/md0'
                   % (config.get_config('instance', 'raid_readahead')), expectError=True)


def configure_jmxtrans(config, ipaddr):
    if config.get_config("nedry", "jmxtrans") != "completed":
        with open('/home/ubuntu/parsel/nedry/bin/zookeeper_jmxtrans.json', 'r') as f:
            json = f.read()
        p = re.compile('"127.0.0.1"')
        json = p.sub('"{0}"'.format(ipaddr), json)
        logger.exe("sudo mkdir -p /var/lib/jmxtrans")
        with open(os.path.join('/var/lib/jmxtrans/', 'zookeeper_jmxtrans.json'), 'w') as f:
            f.write(json)
        logger.info('zookeeper_jmxtrans.json configured with %s as source host.' % (ipaddr,))
        config.set_config("nedry", "jmxtrans", "completed")
    else:
        logger.info('jmxtrans configuration logged as completed, skipping.')


def run_puppet_agent():
    logger.exe("sudo puppet agent -t -d")


def configure_zookeeper_exhibitor_dir_linked_to_raid(config):
    if config.get_config("nedry", "zookeeper_raid_dir") != "completed":
        logger.exe("sudo mkdir -p /raid0/zookeeper")
        logger.exe("sudo ln  -s /raid0/zookeeper  /var/lib/zookeeper")
        logger.info("Linked /var/lib/zookeeper to /raid0/zookeeper ")
        config.set_config("nedry", "zookeeper_raid_dir", "completed")
    else:
        logger.info('ZooKeeper/Exhibitor dirs logged as mapped to /raid0, skipping.')


def run():
    config = Config()
    if config.get_config("instance", "initial_configuration") != "completed":
        # The call order here isn't arbitrary:
        # [config]-> [raid]->  [exhb]-> [restarts]
        instance_data = config.get_instance_data()
        options = config.parse_supplied_userdata(instance_data)
        RaidInstaller().install(config)
        configure_jmxtrans(config, instance_data['local-ipv4'])
        configure_zookeeper_exhibitor_dir_linked_to_raid(config)
        run_puppet_agent()
        disk_tasks(config)
        config.set_config("instance", "initial_configuration", "completed")
        logger.info('Configuration completed.')
    else:
        logger.info('Initial configuration logged as completed, skipping.')
        restart_tasks_on_reboot(config)


run()
