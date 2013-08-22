# Parsel

Parsel is a set of scripts to create an AMI for Cassandra/Kafka and deploy clusters into EC2.

It borrows instance creation techniques from  [ComboAMI](https://github.com/riptano/ComboAMI),
and uses [Priam](https://github.com/netflix/Priam) with auto-scaling groups for instance management.

AMI creation is done with [Packer](https://packer.io/).

# Documentation

 - See [the wiki](https://github.com/dehora/parsel/wiki).

# License

Copyright 2012-2013 Bill de hÓra.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance 
with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is 
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See 
the License for the specific language governing permissions and limitations under the License.
