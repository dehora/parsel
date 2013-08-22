#!/usr/bin/env python

from random import choice

quotes = ["Make fists with your toes.",
          "I think I can handle this Eurotrash.",
          "Does it sound like I'm ordering a pizza?",
          "Ho ho ho.",
          "Was always kinda partial to Roy Rogers actually.",
          "I'm Agent Johnson, this is Special Agent Johnson.",
          "Welcome to the party, pal.",
          "This is agent Johnson. No, the other one.",
          "I could talk about industrialization and men's fashion all day.",
          "Yippee-ki-yay.",
          "Now I know what a TV dinner feels like."]


def node_type():
    print """
 _  __      __ _           ____            _
| |/ /__ _ / _| | ____ _  | __ ) _ __ ___ | | _____ _ __
| ' // _` | |_| |/ / _` | |  _ \| '__/ _ \| |/ / _ \ '__|
| . \ (_| |  _|   < (_| | | |_) | | | (_) |   <  __/ |
|_|\_\__,_|_| |_|\_\__,_| |____/|_|  \___/|_|\_\___|_|

    "%s"

Logs:
   tail -f /var/log/kafka/kafka.log
   tail -f /var/log/supervisor/kafka/kafka.err
   tail -f /var/log/supervisor/kafka/kafka.out

""" % (choice(quotes))


def run():
    node_type()

run()
