#!/usr/bin/env python

import ConfigParser
import os
import urllib2
from  urllib2 import HTTPError
from optparse import OptionParser
import shlex
from nedry import logger
import sys, traceback

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
        self.config_data['conf_path'] = os.path.expanduser("/etc/nedry/")
        # noinspection PyBroadException
        try:
            self.config_parser.add_section('instance')
            self.config_parser.add_section('nedry')
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
            print "Whoa! What if there was an Exception?"
            instance_data['user-data'] = ''
        instancetype = http_get('http://instance-data/latest/meta-data/instance-type')
        logger.info("instance-type: %s" % instancetype)
        if instancetype == 'm1.small' or instancetype == 'm1.medium' or instancetype == 'm1.micro':
            logger.exit_path(self, "Instance too small, must be at least m1.large.", instance_data)
        instance_data['local-ipv4'] = http_get('http://instance-data/latest/meta-data/local-ipv4')
        return instance_data

    def parse_supplied_userdata(self, instance_data):
        parser = OptionParser()
        parser.add_option("--cluster_name", action="store", type="string", dest="cluster_name",
                          help="ZooKeeper cluster_name")
        parser.add_option("--s3_config_bucket", action="store", type="string", dest="s3_config_bucket",
                          help="Exhibitor S3 config")
        parser.add_option("--s3_backup_bucket", action="store", type="string", dest="s3_backup_bucket",
                          help="Exhibitor S3 backup")
        parser.add_option("--aws_region", action="store", type="string", dest="aws_region", default="eu-west-1",
                          help="AWS region")
        parser.add_option("--exhibitor_heap", action="store", type="string", dest="exhibitor_heap", default="512M",
                          help="Exhibitor min/max heap")

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
    instance_data = {}
    # instance_data = config.get_instance_data()
    instance_data['user-data'] = " --cluster_name zoo_cayovaprod_0001 --s3_config_bucket cayova-backup-zookeeper --s3_backup_bucket cayova-backup-zookeeper --puppet_master_addr 10.36.129.93 --graphite_addr 10.246.103.196 --exhibitor_heap 512M --aws_region eu-west-1"
    options = config.parse_supplied_userdata(instance_data)
    print options