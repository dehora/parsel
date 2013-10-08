### parsel

Parsel is a set of scripts to create an AMI for Cassandra and deploy clusters into EC2.

It borrows instance creation techniques from  [ComboAMI](https://github.com/riptano/ComboAMI),
and uses [Priam](https://github.com/netflix/Priam) with auto-scaling groups for instance management.

AMI creation is done with [Packer](https://packer.io/).


### Install Packer ###

See http://www.packer.io/downloads.html

### Install Parsel ###

```
cd <path-to-parsel-parent>
git clone git@github.com:dehora/parsel.git
cd parsel
```


### Setup files for upload ###

You will need to tarball the parsel project -

```
cd <path-to-parsel-parent>
tar -zcvf /tmp/parsel.tar.gz parsel
```

Make sure where you put it matches the `parsel_tar_src` variable.

### Create an AMI ###

Edit the variables.json file as needed and validate the configuration, replacing `...` below with your local details -

```
cd <path-to-parsel-parent>/parsel/packer/cassandra
packer validate \
-var-file=variables.json \
-var 'aws_access_key=...' \
-var 'aws_secret_key=...' \
-var 'init_parsel_src=<path-to-parsel-parent>/parsel/packer/cassandra/init-parsel-cassandra.sh' \
-var 'awscredential_properties_src=<path-to-awscredential_properties_src>' \
<path-to-parsel-parent>/parsel/packer/cassandra/cassandra.json
```

The params are -

 - aws_access_key: AWS access key; you must set this
 - aws_secret_key: AWS secret key; you must set this
 - init_parsel_src: the path to the parsel init-parsel.sh; default is `/tmp/init-parsel.sh`
 - parsel_tar_src: (not shown) the path to the parsel init-parsel.sh; default is `/tmp/parsel.tar.gz`
 - awscredential_properties_src: the path to the properties file that will be used by Priam; default is `/tmp/awscredential.properties`

The `awscredential.properties` file should contain the following properties, replacing `...` with your property values -

```
# aws access key
AWSACCESSID=...
# aws secret key
AWSKEY=..
```

Build the AMI -

```
packer build \
-var-file=variables.json \
-var 'aws_access_key=...' \
-var 'aws_secret_key=...' \
-var 'init_parsel_src=<path-to-parsel-parent>/parsel/packer/cassandra/init-parsel-cassandra.sh' \
-var 'awscredential_properties_src=<path-to-awscredential_properties_src>' \
<path-to-parsel-parent>/parsel/packer/cassandra/cassandra.json
```

There will be lots of output. At the end, the AMI name will be displayed -

```
==> amazon-ebs: Stopping the source instance...
==> amazon-ebs: Waiting for the instance to stop...
==> amazon-ebs: Creating the AMI: packer-cassandra-1377166443
==> amazon-ebs: AMI: ami-33081347
==> amazon-ebs: Waiting for AMI to become ready...
==> amazon-ebs: Adding tags to AMI (ami-33081347)...
    amazon-ebs: Adding tag: "cassandra_version": "11x"
==> amazon-ebs: Modifying AMI attributes...
    amazon-ebs: Modifying: description
==> amazon-ebs: Terminating the source AWS instance...
==> amazon-ebs: Deleting temporary keypair...
Build 'amazon-ebs' finished.

==> Builds finished. The artifacts of successful builds are:
--> amazon-ebs: AMIs were created:

eu-west-1: ami-33081347
dehora:packer[master]$
```

### Cassandra version ###

The `0.5.0` parsel version defaults to 1.2. To build a 1.1 ami set the `cassandra_version` variable to `11x`.


### Tribbles ###

#### ssh timeout ####

```
 ==> amazon-ebs: Creating temporary keypair for this instance...
==> amazon-ebs: Launching a source AWS instance...
==> amazon-ebs: Waiting for instance (i-5c27a610) to become ready...
==> amazon-ebs: Waiting for SSH to become available...
==> amazon-ebs: Timeout waiting for SSH.
==> amazon-ebs: Terminating the source AWS instance...
==> amazon-ebs: Deleting temporary keypair...
```

 - Check you have permissions to access the created instance via the `security_group_id` settings.
 - Increase the value of "ssh_timeout" in `cassandra.json`'s ebs builder

### can't validate ###

Earlier versions of packer didn't like running outside the directory `cassandra.json` was located in. Try
absolute paths or running from within the directory `cassandra.json` is in.


