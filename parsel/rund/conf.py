#!/usr/bin/env python

import ConfigParser
import os
import urllib2
from urllib2 import HTTPError
from optparse import OptionParser
import shlex
import traceback

# Based on ComboAMI, see https://github.com/riptano/ComboAMI
from parsel.rund import logger

configfile = '/etc/parsel/parsel.conf'


def http_get(url):
    try:
        return urllib2.urlopen(urllib2.Request(url)).read()
    except HTTPError:
        logger.info("Failed to fetch %s, retrying..." % url)


class Config:
    def __init__(self):
        self.config_parser = ConfigParser.RawConfigParser()
        self.config_parser.read(configfile)
        self.config_data = {}
        self.config_data['conf_path'] = os.path.expanduser("/etc/cassandra/")
        # noinspection PyBroadException
        try:
            self.config_parser.add_section('instance')
            self.config_parser.add_section('cassandra')
        except:
            pass

    def set_config(self, section, variable, value):
        self.config_parser.set(section, variable, value)
        with open(configfile, 'wb') as configtext:
            self.config_parser.write(configtext)

    def get_config(self, section, variable):
        # noinspection PyBroadException
        try:
            self.config_parser.read(configfile)
            return self.config_parser.get(section, variable.lower())
        except:
            traceback.print_exc()
            return False

    def get_instance_data(self):
        instance_data = {}
        self.set_config("instance", "initial_configuration", "started")
        # noinspection PyBroadException
        try:
            instance_data['user-data'] = http_get('http://instance-data/latest/user-data/')
            if instance_data['user-data'] is None:
                instance_data['user-data'] = ""
            logger.info("user-data follows:")
            logger.info(instance_data['user-data'])
        except Exception:
            traceback.print_exc()
            instance_data['user-data'] = ''
        instancetype = http_get('http://instance-data/latest/meta-data/instance-type')
        logger.info("instance-type: %s" % instancetype)
        if instancetype == 'm1.small' or instancetype == 'm1.micro':
            logger.exit_path(self, "instance too small, must be at least m1.medium.", instance_data)

        instance_data['local-ipv4'] = http_get('http://instance-data/latest/meta-data/local-ipv4')
        return instance_data

    def set_supplied_userdata(self, options):
        logger.info("set_supplied_userdata")
        self.set_config("instance", "cluster_name", options.cluster_name)
        self.set_config("instance", "aws_region", options.aws_region)

    def parse_supplied_userdata(self, instance_data):
        parser = OptionParser()
        parser.add_option("--cluster_name", action="store", type="string", dest="cluster_name",
                          help="Cluster_name")
        parser.add_option("--aws_region", action="store", type="string", dest="aws_region", default="eu-west-1",
                          help="AWS region")

        # noinspection PyBroadException
        try:
            (options, args) = parser.parse_args(shlex.split(instance_data['user-data']))
            return options
        except:
            traceback.print_exc()
            logger.exit_path(self, instance_data,
                             "Options not set correctly, options follow: \n %s" % (str(instance_data['user-data']),))


if __name__ == "__main__":
    config = Config()
    instance_data = config.get_instance_data()
    options = config.parse_supplied_userdata(instance_data)
    config.set_supplied_userdata(options)