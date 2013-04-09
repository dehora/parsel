from parsel import logger
from parsel.rund.conf import Config


default_tomcat = "/var/lib/tomcat7/webapps"


class PriamInstaller:
    def __init__(self):
        pass

    def install(self,
                config,
                priam_agent_jar_url,
                priam_agent_jar_filename,
                priam_war_url,
                priam_war_filename,
                tomcat=default_tomcat):

        if config.get_config("priam", "priam_configuration") != "completed":
            logger.exe("sudo service tomcat7 stop")
            self.install_priam(priam_agent_jar_url, priam_agent_jar_filename, priam_war_url, priam_war_filename, tomcat)
            config.set_config("priam", "priam_configuration", "completed")
        else:
            logger.info('PriamInstaller logged as completed, skipping.')

    def install_priam(self,
                      priam_agent_jar_url,
                      priam_agent_jar_filename,
                      priam_war_url,
                      priam_war_filename,
                      tomcat):

        logger.exe('sudo wget --no-check-certificate --output-document %s %s'
                   % (priam_agent_jar_filename, priam_agent_jar_url,))

        logger.exe('sudo mv %s /usr/share/cassandra/lib/' % (priam_agent_jar_filename,))

        with open('/etc/cassandra/cassandra-env.sh', 'a') as f:
            f.write('JVM_OPTS="$JVM_OPTS -javaagent:/usr/share/cassandra/lib/%s"\n'
                    % (priam_agent_jar_filename,))

        logger.exe('sudo wget --no-check-certificate --output-document %s %s'
                   % (priam_war_filename, priam_war_url,))

        # the agent is looking for "/Priam/" in the uri
        logger.exe('sudo mv %s %s/Priam.war' % (priam_war_filename, tomcat,))


if __name__ == "__main__":
    config = Config()
    instance_data = config.get_instance_data()
    options = config.parse_supplied_userdata(instance_data)
    config.set_supplied_userdata(options)
    priam = PriamInstaller()
