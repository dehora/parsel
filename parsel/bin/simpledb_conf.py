#!/usr/bin/env python

import boto.sdb
import sys
import time
from optparse import OptionParser


default_bucket = "cayova-backup-cassandra"
default_zones_available = "eu-west-1a,eu-west-1b,eu-west-1c"
default_sdb_region = "us-east-1"


def main(argv=None):
    parser = OptionParser(usage="""

    simpledb_conf.py [options]

Create Priam cluster metadata in Simple DB. Example

 python simpledb_conf.py -k AA00AA00AA00AA00AA00 -s AAAAA/00AAAAAAAAAAAAAAAAAAAAAAAAAAAA000 -c test_cluster_5 -z "eu-west-1a,eu-west-1b"

    """)

    parser.add_option(
        '-k', '--key', nargs=1, action='store', dest='awskey',
        help="The AWS key (required).")

    parser.add_option(
        '-s', '--secret', nargs=1, action='store', dest='awssecret',
        help="The AWS Secret (required).")

    parser.add_option(
        '-c', '--cluster_name', metavar='priam.clustername', nargs=1, action='store', dest='cluster_name',
        help="""The 'priam.clustername' property (required). Also the 'appId' value in simple db
 and the 1st part of autoscaling group name. This value _SHOULD NOT_ contain hyphens.""")

    parser.add_option(
        '-b', '--bucket', metavar="priam.s3.bucket", nargs=1, action='store', dest='s3_bucket',
        default=default_bucket,
        help="The 'priam.s3.bucket' property (optional). default [%s]" % default_bucket)

    parser.add_option(
        '-z', '--zones_available', metavar="priam.zones.available", nargs=1, action='store', dest='zones_available',
        default=default_zones_available,
        help="The 'priam.zones.available' property (optional). default [%s]" % default_zones_available)

    parser.add_option(
        '-r', '--aws_region', nargs=1, action='store', dest='aws_region',
        default=default_sdb_region,
        help="The AWS Simple DB Region (optional).  default [%s] This is _not_ the Cassandra cluster region." % default_sdb_region)

    (options, args) = parser.parse_args()

    if not options.awssecret:
        parser.error('Please provide an AWS Secret with -s, --secret')

    if not options.awskey:
        parser.error('Please provide an AWS Key with -k, --key')

    if not options.cluster_name:
        parser.error('Please provide a cassandra cluster name with -c, --cluster_name')

    conn = boto.sdb.connect_to_region(
        options.aws_region,
        aws_access_key_id=options.awskey,
        aws_secret_access_key=options.awssecret)

    dom = conn.get_domain('PriamProperties')

    cluster_name = options.cluster_name
    zones_available = options.zones_available
    s3_bucket = options.s3_bucket

    cluster_name_key = cluster_name + '.clustername'
    s3_bucket_key = cluster_name + '.s3.bucket'
    zones_available_key = cluster_name + '.zones.available'

    items = {
        cluster_name_key: {
            'property': "priam.clustername",
            'value': cluster_name,
            'appId': cluster_name,
        },
        s3_bucket_key: {
            'property': 'priam.s3.bucket',
            'value': s3_bucket,
            'appId': cluster_name,
        },
        zones_available_key: {
            'property': 'priam.zones.available',
            'value': zones_available,
            'appId': cluster_name,
        },
        cluster_name+".cass.home": {
            'property': 'priam.cass.home',
            'value': "/etc/cassandra",
            'appId': cluster_name,
        },
        cluster_name+".cass.startscript": {
            'property': 'priam.cass.startscript',
            'value': "/etc/init.d/cassandra start",
            'appId': cluster_name,
        },
        cluster_name+".cass.stopscript": {
            'property': 'priam.cass.stopscript',
            'value': "/etc/init.d/cassandra stop",
            'appId': cluster_name,
        },
        #priam.cass.home
    }

    dom.batch_put_attributes(items)

    time.sleep(8) # simple db sometimes needs time to update
    rs = dom.select('select * from `PriamProperties` where appId="%s"' % cluster_name)
    print "\nCluster metadata stored in Simple DB under appID [%s] is - \n" % cluster_name
    for item in rs:
        print "property key:", item.name
        print " property:", item.get("property")
        print " value:", item.get("value")
        print " appId:", item.get("appId")
        print "---------"


if __name__ == "__main__":
    sys.exit(main())