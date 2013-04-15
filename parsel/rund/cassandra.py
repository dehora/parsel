from parsel import logger

from parsel.rund.conf import Config
from parsel import repo

# Based on ComboAMI, see https://github.com/riptano/ComboAMI


class CassandraInstaller:

    def __init__(self):
        pass

    def install(self, config, options):
        if config.get_config("instance", "cassandra_configuration") != "completed":
            if options.release and options.release.startswith('dsc'):
                repo.install_datastax_debian_repos(config)
                self.install_cassandra_datastax(config, options)
            elif options.release and options.release.startswith('asf'):
                cass_release = options.release[3:]
                repo.install_apache_debian_repos(config, cass_release)
                self.install_cassandra_apache(config, options.release)
            else:
                pass  # fail
            config.set_config("instance", "cassandra_configuration", "completed")
        else:
            logger.info('CassandraInstaller logged as completed, skipping.')

    def install_cassandra_apache(self, config, cass_release="asf11x"):
        logger.info('Installing apache cassandra cassandra=%s' % (cass_release,))
        config.set_config('cassandra', 'partitioner', 'random_partitioner')
        logger.exe('sudo apt-get install cassandra')
        config.set_config('instance', 'package', cass_release)

    def install_cassandra_datastax(self, config, options):
        if options.release and options.release.startswith('dsc1.0'):
            cass_release = options.release
            if cass_release == '1.0.11-1':
                cass_release = '1.0.11'
            logger.info('Installing datastax cassandra cassandra=%s dsc=%s' % (cass_release, options.release))
            logger.exe('sudo apt-get install -y python-cql cassandra={0} dsc={1}'.format(cass_release, options.release))
            config.set_config('instance', 'package', 'dsc')
            config.set_config('cassandra', 'partitioner', 'random_partitioner')
        elif options.release and options.release.startswith('dsc1.1'):
            dse_release = cass_release = options.release
            if dse_release == '1.1.6':
                dse_release = '1.1.6-1'
            if cass_release == "1.1":
                # use highest available
                cass_release = "1.1.9"
                dse_release = "1.1.9-1"
                logger.info('Cassandra 1.1 requested, installing 1.1.9 as highest available')
            logger.info('Installing datastax cassandra cassandra=%s dsc=%s' % (cass_release, dse_release))
            logger.exe('sudo apt-get install -y python-cql cassandra={0} dsc1.1={1}'.format(cass_release, dse_release))
            config.set_config('instance', 'package', 'dsc1.1')
            config.set_config('cassandra', 'partitioner', 'random_partitioner')
        else:
            logger.info('Installing cassandra dsc12 with murmur hash (vnodes)')
            logger.exe('sudo apt-get install -y python-cql dsc12')
            config.set_config('instance', 'package', 'dsc12')
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
