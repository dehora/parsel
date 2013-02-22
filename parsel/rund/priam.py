from parsel import logger
from parsel.rund.conf import Config

default_version = "1.1.19-euwest-0.0.5"
default_bucket = "https://viscis-archive.s3.amazonaws.com"
default_tomcat = "/var/lib/tomcat7/webapps"


class PriamInstaller:
    def __init__(self):
        pass

    def install(self, config, bucket=default_bucket, version=default_version, tomcat=default_tomcat):
        if config.get_config("instance", "priam_configuration") != "completed":
            self.install_s3cmd()
            logger.exe("sudo service tomcat7 stop")
            self.install_priam(bucket, version, tomcat)
            config.set_config("instance", "priam_configuration", "completed")
        else:
            logger.info('PriamInstaller logged as completed, skipping.')

    def install_priam(self, bucket, version, tomcat):
        logger.exe('sudo wget --no-check-certificate %s/priam-cass-extensions-%s.jar' % (bucket, version,))
        logger.exe('sudo mv priam-cass-extensions-%s.jar /usr/share/cassandra/lib/' % (version,))
        with open('/etc/cassandra/cassandra-env.sh', 'a') as f:
            f.write('JVM_OPTS="$JVM_OPTS -javaagent:/usr/share/cassandra/lib/priam-cass-extensions-%s.jar"\n'
                    % (version,))
        logger.exe('sudo wget --no-check-certificate %s/priam-web-%s.war' % (bucket, version,))
        # the agent is looking for "/Priam/" in the uri
        logger.exe('sudo mv priam-web-%s.war %s/Priam.war' % (version, tomcat,))

    def install_s3cmd(self):
        while True:
            output = logger.exe('sudo apt-get -y install s3cmd')
            if not output[1] and not 'err' in output[0].lower() and not 'failed' in output[0].lower():
                break


if __name__ == "__main__":
    config = Config()
    instance_data = config.get_instance_data()
    options = config.parse_supplied_userdata(instance_data)
    config.set_supplied_userdata(options)
    priam = PriamInstaller()
    priam.install(config)
