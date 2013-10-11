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
          "Now I know what a TV dinner feels like."
          "Dude, at least it's an ethos.",
          "Yeah, well, you know, that's just, like, your opinion, man.",
          "That rug really tied the room together.",
          "You want a toe? I can get you a toe, believe me.",
          "Dude, let's go bowling.",
          "Donny, these men are nihilists, there's nothing to be afraid of.",
          "You are entering a world of pain",
          "I can see you don't want to be cheered up here.",
          "I'm the Dude, man.",
          "For your information, the Supreme Court has roundly rejected prior restraint.",
          "Hey, nice marmot!",
          "Ve vant ze money, Lebowski.",
          "You know, Dude, I myself dabbled in pacifism once.",
          "Obviously, you're not a golfer."]


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
