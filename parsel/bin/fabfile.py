from fabric.api import *
import time

env.hosts = []
env.user = 'ubuntu'
env.key_filename = ""


def __reset():
    """
    This is workaround for 0.2.0, which has a bug that lets C* start before Priam can configure it
    """
    print("Executing on %s as %s" % (env.host, env.user))
    sudo("service cassandra stop")
    sudo('service tomcat7 stop')
    time.sleep(10)
    sudo('rm -rf /raid0/cassandra/data/system/*')
    sudo('rm -rf /raid0/cassandra/commitlog/*')
    sudo('rm -rf /var/log/tomcat7/*')
    sudo('rm -rf /var/log/cassandra/*')
    sudo('service tomcat7 start')


def tpstats():
    print("Executing on %s as %s" % (env.host, env.user))
    sudo('nodetool tpstats')