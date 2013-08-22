### Install Packer ###

See http://www.packer.io/downloads.html

### Clone Parsel ###

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

Create a variables.json file as needed and validate the configuration, replacing `...` below with your local details -

```
packer validate \
-var-file=variables.json \
-var 'aws_access_key=...' \
-var 'aws_secret_key=...' \
-var 'init_parsel_src=<path-to-parsel-parent>/parsel/packer/cassandra/init-parsel-cassandra.sh' \
-var 'awscredential_properties_src=<path-to-awscredential_properties_src>' \
<path-to-parsel-parent>/parsel/packer/cassandra/cassandra.json
```
The params are

 - aws_access_key: AWS access key; you must set this
 - aws_secret_key: AWS secret key; you must set this
 - init_parsel_src:  the path to the `init-parsel-cassandra.sh` file; you must set this
 - parsel_tar_src: (not shown) the path to parsel tarball file; you must set this
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
packer validate \
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

Parsel defaults to C* 1.1. To build a 1.2 ami set the `cassandra_version` variable to `12x`.


