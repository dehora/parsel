from parsel.logger import exe


class TimeInstaller:
    def setup_ntp(self, server_list="ie.pool.ntp.org\nuk.pool.ntp.org"):
        exe('sudo apt-get -y install ntp')
        with open('/etc/ntp.conf', 'r') as f:
            ntp_conf = f.read()
        for i in range(0, 4):
            server_list += "server {0}.europe.pool.ntp.org\n".format(i)
        ntp_conf = ntp_conf.replace('server ntp.ubuntu.com', server_list)
        exe('sudo echo "%s" > /etc/ntp.conf' % (ntp_conf, ))
        exe('sudo service ntp restart')


if __name__ == "__main__":
    TimeInstaller().setup_ntp()