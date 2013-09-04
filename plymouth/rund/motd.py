#!/usr/bin/env python

from random import choice
quotes = ["Sudo make me a sandwich.",
          "SCIENCE. It works.",
          "Someone is _wrong_ on the Internet.",
          "It was a soundstage on Mars.",
          "Your party enters the tavern.",
          "Citation needed.",
          "Take the bitstring down, flip it, and reverse it.",
          "0x3A228213A, 0x6339392C, 0x7363682E.",
          "Did you know you can just _buy_ lab coats?",
          "Who are you? How did you get in my house?",
          "When someone calls my phone, it makes a goddamn RINGING sound.",
          "Oh, yes. Little Bobby Tables, we call him.",
          "Turing Test Extra Credit: Convince the examiner that he's a computer.",
          "What are you doing!?. - Gluing captions to your cats.",
          "Did I do a good job? Do I get to come home?",
          "Actually, it's looking more like six days.",
          "Everybody stand back. I know regular expressions.",
          "If we make it back alive, you're never upgrading anything again.",
          "To complete your web registration, please prove that you're human.",
          "My hobby: extrapolation.",
          "7:15am - 8:00am: Post on productivity blogs about my schedule.",
          "Why? - To mess around with advertisers. Check it out.",
          "And over there, we have the labyrinth guards.",
          "Stand back! I'm going to try science!",
          "I just typed, 'import antigravity'."]

def node_type():
    print """

    ,--.|           |   o                         |
    |-- |   ,--.,--.|-- .,--.,--.,---.,--.,--.,--.|--.
    |   |   ,--|`--.|   ||   `--.|---',--||   |   |  |
    `--'`--'`--^`--'`--'``--'`--'`---'`--^`   `--'`  '

    "%s"

Logs:
   tail -f /var/log/supervisor/elasticsearch/elasticsearch.err
   tail -f /var/log/supervisor/elasticsearch/elasticsearch.out

""" % (choice(quotes))


def run():
    node_type()

run()
