#!/usr/bin/env python

import subprocess
from random import choice

quotes = ["How's that for a slice of fried gold?",
          "Wait for all of this to blow over.",
          "Okay. But dogs _can_ look up.",
          "Vacant, with a hint of sadness.",
          "You've got red on you.",
          "I will repeat that: by removing the head or destroying the brain.",
          "It's not hip hop, it's electro.",
          "Player 2 has entered the game.",
          "The zed-word. Don't say it!",
          "Cornetto.",
          "That is really going to exacerbate things for all of us.",
          "L1 cache reference: 0.5ns"
          "Branch mispredict: 5ns",
          "L2 cache reference: 7ns",
          "Mutex lock/unlock: 100ns",
          "Main memory reference: 100ns",
          "Compress 1K bytes with Zippy: 10,000ns",
          "Send 2K bytes over 1 Gbps network: 20,000ns",
          "Read 1 MB sequentially from memory: 250,000ns (0.25ms)",
          "Round trip within same datacenter: 500,000 ns (0.5ms)",
          "Disk seek: 10,000,000ns (10ms)",
          "Read 1 MB sequentially from network: 10,000,000ns (10ms)",
          "Read 1 MB sequentially from disk: 30,000,000ns (30ms)",
          "Send packet CA->Netherlands->CA: 150,000,000ns (150ms)",
          "Rotational random seek delay at 10K RPM: 3ms"]


def nodetool_ring():
    print "Asking nodetool for cluster status..."
    print
    p1 = subprocess.Popen(["nodetool", "ring"], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=False)
    p1.wait()
    for line in iter(p1.stdout.readline, ''):
        print " ", line.rstrip()
    print


def nodetool_info():
    print "Asking nodetool for node info..."
    print
    p1 = subprocess.Popen(["nodetool", "info"], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=False)
    p1.wait()
    for line in iter(p1.stdout.readline, ''):
        print " ", line.rstrip()
    print


def node_type():
    print """
  ____                              _
 / ___|__ _ ___ ___  __ _ _ __   __| |_ __ __ _
| |   / _` / __/ __|/ _` | '_ \ / _` | '__/ _` |
| |__| (_| \__ \__ \ (_| | | | | (_| | | | (_| |
 \____\__,_|___/___/\__,_|_| |_|\__,_|_|  \__,_|

   "%s"

Logs:
   tail -f /var/log/tomcat7/priam.log
   tail -f /var/log/cassandra/system.log

C* Commands:
  cassandra-cli
  nodetool info|tpstats|cfstats|compactionstats|netstats
  More: nodetool --help

Priam Commands:
  curl http://127.0.0.1:8080/Priam/REST/v1/cassadmin/start
  curl http://127.0.0.1:8080/Priam/REST/v1/cassadmin/stop
  More: https://github.com/dehora/Priam/wiki/REST-API
""" % (choice(quotes))


def run():
    node_type()
    nodetool_ring()
    nodetool_info()


run()
