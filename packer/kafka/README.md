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
-var 'init_parsel_src=<path-to-parsel-parent>/parsel/packer/kafka/init-parsel-kafka.sh' \
<path-to-parsel-parent>/parsel/packer/kafka/kafka.json
```
The params are

 - aws_access_key: AWS access key; you must set this
 - aws_secret_key: AWS secret key; you must set this
 - init_parsel_src:  the path to the `init-parsel-kafka.sh` file; you must set this
 - parsel_tar_src: (not shown) the path to the parsel tarball file; you must set this

Build the AMI -

```
packer validate \
-var-file=variables.json \
-var 'aws_access_key=...' \
-var 'aws_secret_key=...' \
-var 'init_parsel_src=<path-to-parsel-parent>/parsel/packer/kafka/init-parsel-kafka.sh' \
<path-to-parsel-parent>/parsel/packer/kafka/kafka.json
```

There will be lots of output. At the end, the AMI name will be displayed -

```
==> amazon-ebs: Stopping the source instance...
==> amazon-ebs: Waiting for the instance to stop...
==> amazon-ebs: Creating the AMI: packer-kafka-1377166443
==> amazon-ebs: AMI: ami-33081347
==> amazon-ebs: Waiting for AMI to become ready...
==> amazon-ebs: Adding tags to AMI (ami-33081347)...
    amazon-ebs: Adding tag: "kafka_version": "0.7.2-2.9.2-rc3-1"
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



