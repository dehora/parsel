from parsel import logger

from parsel.rund.conf import Config
from parsel import repo

# Based on ComboAMI, see https://github.com/riptano/ComboAMI


class CassandraInstaller:

    def __init__(self):
        pass

    def install(self, config, release):
        if config.get_config("cassandra", "cassandra_configuration") != "completed":
            if release.startswith('dsc'):
                repo.install_datastax_debian_repos(config)
                self.install_cassandra_datastax(config, release)
            elif release.startswith('asf'):
                cass_release = release[3:]
                repo.install_apache_debian_repos(config, cass_release)
                self.install_cassandra_apache(config, release)
            else:
                logger.error('Cassandra cassandra=%s unrecognized' % (release,))
                config.set_config("cassandra", "cass_release", "notrecognized")
            config.set_config("cassandra", "cassandra_configuration", "completed")
        else:
            logger.info('CassandraInstaller logged as completed, skipping.')

    def install_cassandra_apache(self, config, cass_release="asf11x"):
        logger.info('Installing apache cassandra cassandra=%s' % (cass_release,))
        config.set_config('cassandra', 'partitioner', 'random_partitioner')
        logger.exe('sudo apt-get -y --force-yes install cassandra')
        config.set_config('cassandra', 'package', cass_release)

    def install_cassandra_datastax(self, config, release):
        if release.startswith('dsc1.0'):
            cass_release = release
            if cass_release == '1.0.11-1':
                cass_release = '1.0.11'
            logger.info('Installing datastax cassandra cassandra=%s dsc=%s' % (cass_release, release))
            logger.exe('sudo apt-get install -y python-cql cassandra={0} dsc={1}'.format(cass_release, release))
            config.set_config('cassandra', 'package', 'dsc')
            config.set_config('cassandra', 'partitioner', 'random_partitioner')
        elif release.startswith('dsc1.1'):
            dse_release = cass_release = release
            if dse_release == '1.1.6':
                dse_release = '1.1.6-1'
            if cass_release == "1.1":
                # use highest available
                cass_release = "1.1.9"
                dse_release = "1.1.9-1"
                logger.info('Cassandra 1.1 requested, installing 1.1.9 as highest available')
            logger.info('Installing datastax cassandra cassandra=%s dsc=%s' % (cass_release, dse_release))
            logger.exe('sudo apt-get install -y python-cql cassandra={0} dsc1.1={1}'.format(cass_release, dse_release))
            config.set_config('cassandra', 'package', 'dsc1.1')
            config.set_config('cassandra', 'partitioner', 'random_partitioner')
        else:
            logger.info('Installing cassandra dsc12 with murmur hash (vnodes)')
            logger.exe('sudo apt-get install -y python-cql dsc12')
            config.set_config('cassandra', 'package', 'dsc12')
            config.set_config('cassandra', 'partitioner', 'murmur')

        logger.exe('sudo service cassandra stop')


if __name__ == "__main__":
    config = Config()
    instance_data = config.get_instance_data()
    options = config.parse_supplied_userdata(instance_data)
    config.set_supplied_userdata(options)
    cassandra = CassandraInstaller()
    cassandra.install_cassandra(config, options)
    config.set_config("instance", "initial_configuration", "completed")
