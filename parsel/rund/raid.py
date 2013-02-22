import glob
import time
import os
from parsel import logger

# Based on ComboAMI, see https://github.com/riptano/ComboAMI


class RaidInstaller:

    def mount_raid(self, devices, config):
        # Make sure the devices are umounted, then run fdisk on each device
        logger.info(
            'Clear "invalid flag 0x0000 of partition table 4" by issuing a write, then running fdisk on each device...')
        formatCommands = "echo 'n\np\n1\n\n\nt\nfd\nw'"
        for device in devices:
            logger.info('Confirming devices are not mounted:')
            logger.exe('sudo umount {0}'.format(device), False)
            logger.pipe("echo 'w'", 'sudo fdisk -c -u {0}'.format(device))
            logger.pipe(formatCommands, 'sudo fdisk -c -u {0}'.format(device))

        # Create a list of partitions to RAID
        logger.exe('sudo fdisk -l')
        partitions = glob.glob('/dev/xvd*[0-9]')
        partitions.remove('/dev/xvda1')
        partitions.sort()
        logger.info('Partitions about to be added to RAID0 set: {0}'.format(partitions))

        # Make sure the partitions are umounted and create a list string
        for partition in partitions:
            logger.info('Confirming partitions are not mounted:')
            logger.exe('sudo umount ' + partition, False)
        partion_list = ' '.join(partitions).strip()

        logger.info('Creating the RAID0 set:')
        time.sleep(3)  # was at 10

        config.set_config("instance", "initial_configuration", "raiding")

        # Continuously create the Raid device, in case there are errors
        raid_created = False
        while not raid_created:
            logger.exe(
                'sudo mdadm --create /dev/md0 --chunk=256 --level=0 --raid-devices={0} {1}'.format(len(partitions),
                                                                                                   partion_list),
                expectError=True)
            raid_created = True

            logger.pipe('echo DEVICE {0}'.format(partion_list), 'sudo tee /etc/mdadm/mdadm.conf')
            time.sleep(5)

            # New parsing and elimination of the name= field due to 12.04's new RAID'ing methods
            response = logger.exe('sudo mdadm --examine --scan')[0]
            response = ' '.join(response.split(' ')[0:-1])
            logger.exe('sudo echo "%s" >> /etc/mdadm/mdadm.conf' % (response,))
            logger.exe('sudo update-initramfs -u')

            time.sleep(10)
            config.set_config('instance', 'raid_readahead', 512)
            logger.exe('sudo blockdev --setra 512 /dev/md0')

            logger.info('Formatting the RAID0 set:')
            time.sleep(10)
            raidError = logger.exe('sudo mkfs.xfs -f /dev/md0', expectError=True)[1]

            if raidError:
                logger.exe('sudo mdadm --stop /dev/md_d0', expectError=True)
                logger.exe('sudo mdadm --zero-superblock /dev/sdb1', expectError=True)
                raid_created = False

        # Configure fstab and mount the new RAID0 device
        mnt_point = '/raid0'
        logger.pipe("echo '/dev/md0\t{0}\txfs\tdefaults,nobootwait,noatime\t0\t0'".format(mnt_point),
                    'sudo tee -a /etc/fstab')
        logger.exe('sudo mkdir {0}'.format(mnt_point))
        logger.exe('sudo mount -a')
        logger.exe('sudo mkdir -p {0}'.format(os.path.join(mnt_point, 'cassandra')))
        logger.exe('sudo chown -R cassandra:cassandra {0}'.format(os.path.join(mnt_point, 'cassandra')))

        logger.info('Showing RAID0 details:')
        logger.exe('cat /proc/mdstat')
        logger.exe('echo "15000" > /proc/sys/dev/raid/speed_limit_min')
        logger.exe('sudo mdadm --detail /dev/md0')
        return mnt_point

    def format_xfs(self, devices):
        # Make sure the device is umounted, then run fdisk on the device
        logger.info(
            'Clear "invalid flag 0x0000 of partition table 4" by issuing a write, then running fdisk on the device...')
        formatCommands = "echo 'd\nn\np\n1\n\n\nt\n83\nw'"
        logger.exe('sudo umount {0}'.format(devices[0]))
        logger.pipe("echo 'w'", 'sudo fdisk -c -u {0}'.format(devices[0]))
        logger.pipe(formatCommands, 'sudo fdisk -c -u {0}'.format(devices[0]))

        # Create a list of partitions to RAID
        logger.exe('sudo fdisk -l')
        partitions = glob.glob('/dev/xvd*[0-9]')
        partitions.remove('/dev/xvda1')
        partitions.sort()

        logger.info('Formatting the new partition:')
        logger.exe('sudo mkfs.xfs -f {0}'.format(partitions[0]))

        # Configure fstab and mount the new formatted device
        mnt_point = '/mnt'
        logger.pipe("echo '{0}\t{1}\txfs\tdefaults,nobootwait,noatime\t0\t0'".format(partitions[0], mnt_point),
                    'sudo tee -a /etc/fstab')
        logger.exe('sudo mkdir {0}'.format(mnt_point), False)
        logger.exe('sudo mount -a')
        logger.exe('sudo mkdir -p {0}'.format(os.path.join(mnt_point, 'cassandra')))
        logger.exe('sudo chown -R cassandra:cassandra {0}'.format(os.path.join(mnt_point, 'cassandra')))
        return mnt_point

    def install(self, config):
        # Only create raid0 once. Mount all times in init.d script. A failsafe against deleting this file.
        if config.get_config("instance", "raid_installed"):
            return

        config.set_config("instance", "initial_configuration", "pre-raid")

        # Remove EC2 default /mnt from fstab
        fstab = ''
        file_to_open = '/etc/fstab'
        logger.exe('sudo chmod 777 {0}'.format(file_to_open))
        with open(file_to_open, 'r') as f:
            for line in f:
                if not "/mnt" in line:
                    fstab += line
        with open(file_to_open, 'w') as f:
            f.write(fstab)
        logger.exe('sudo chmod 644 {0}'.format(file_to_open))

        # Create a list of devices
        devices = glob.glob('/dev/xvd*')
        devices.remove('/dev/xvda1')
        devices.sort()
        logger.info('Unformatted devices: {0}'.format(devices))

        # Check if there are enough drives to start a RAID set
        if len(devices) > 1:
            logger.info("Enough drives found to RAID together.\n")
            time.sleep(3)
            mnt_point = self.mount_raid(devices, config)
        else:
            logger.info("Not enough drives to RAID together, formatting XFS.\n")
            mnt_point = self.format_xfs(devices)

        # Never create raid array again
        logger.info("Mounted Raid.\n")
        config.set_config("instance", "raid_installed", True)
        config.set_config("instance", "mount", mnt_point)
        config.set_config("instance", "initial_configuration", "raided")
        return mnt_point