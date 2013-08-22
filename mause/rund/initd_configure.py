#!/usr/bin/env python

import re
import os

from mause.rund.conf import Config
from mause import logger


def configure_jmxtrans(config, ipaddr):
    if config.get_config("mause", "jmxtrans") != "completed":
        with open('/home/ubuntu/parsel/mause/bin/kafka_jmxtrans.json', 'r') as f:
            json = f.read()
        p = re.compile('"127.0.0.1"')
        json = p.sub('"{0}"'.format(ipaddr), json)
        logger.exe("sudo mkdir -p /var/lib/jmxtrans")
        with open(os.path.join('/var/lib/jmxtrans/', 'kafka_jmxtrans.json'), 'w') as f:
            f.write(json)
        logger.info('Kafka_jmxtrans.json configured with %s as source host.' % (ipaddr,))
        config.set_config("mause", "jmxtrans", "completed")
    else:
        logger.info('jmxtrans configuration logged as completed, skipping.')


def run():
    config = Config()
    if config.get_config("instance", "initial_configuration") != "completed":
        instance_data = config.get_instance_data()
        options = config.parse_supplied_userdata(instance_data)
        configure_jmxtrans(config, instance_data['local-ipv4'])
        config.set_config("instance", "initial_configuration", "completed")
    else:
        logger.info('Initial configuration logged as completed, skipping.')

    if config.get_config("mause", "post_configuration") != "completed":
        logger.exe("sudo service puppet stop")
        logger.exe("sudo service kafka stop")


run()
