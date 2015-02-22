# coding: utf8
"""
kuha.py - Willie Lannistaja Kuha Module
Copyright © 2015, Marcus Leivo

Licensed under the GNU Lesser General Public
License Version 3 (or greater at your wish).
"""
from urllib import urlopen
from bs4 import BeautifulSoup
from willie.module import commands, example


@commands('kuha')
@example('.kuha 69')
def lannistaja_kuha(bot, trigger):
    number = ""
    if trigger.group(2):
        try:
            number = str(int(trigger.group(2).split(" ")[0]))
        except:
            pass
    if len(number) > 0:
        url = urlopen("http://lannistajakuha.com/" + number).read()
    else:
        url = urlopen("http://lannistajakuha.com/random").read()
    soup = BeautifulSoup(url)
    result = (soup.find("p", attrs={"class": "teksti"}))
    result = result.text.strip()
    bot.say(result)
