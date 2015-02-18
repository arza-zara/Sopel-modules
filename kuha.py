# coding: utf8
"""
kuha.py - Willie Lannistaja Kuha Module
Copyright © 2015, Marcus Leivo

Licensed under the GNU Lesser General Public
License Version 3 (or greater at your wish).
"""
from urllib import urlopen
from bs4 import BeautifulSoup
from willie.module import commands


@commands('kuha')
def lannistaja_kuha(bot, trigger):
    url = urlopen("http://lannistajakuha.com/random").read()
    soup = BeautifulSoup(url)
    result = (soup.find("p", attrs={"class": "teksti"}))
    result = result.text.strip()
    if trigger.group(3) is None:
        bot.say(result)
    else:
        bot.say("%s: %s" % (trigger.group(2), result))
