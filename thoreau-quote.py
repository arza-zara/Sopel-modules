# coding: utf8
"""
thoreau-quote.py - Willie Thoreau Quotes Module
Copyright © 2014, Marcus Leivo

Licensed under the GNU Lesser General Public
License Version 3 (or greater at your wish).
"""
from __future__ import unicode_literals
from urllib import urlopen
from bs4 import BeautifulSoup
from random import randint, choice
from willie.module import commands


def th_quote_get():
    url = "https://www.goodreads.com/author/quotes/10264.Henry_David_Thoreau?page=" + str(randint(1,11))
    soup = BeautifulSoup(urlopen(url).read())
    quotes = soup.find_all("div", attrs={"class": "quoteText"})
    quote = (choice(quotes).contents[0].replace('      ', '').replace("  ", " ").encode('utf8') + "-H. D. Thoreau".encode('utf8'))
    return quote

@commands('inffo', 'thoreau')
def homopaska(bot, trigger):
    q = th_quote_get()
    while len(q) > 400 or q.decode("utf8").find(u'”') == -1:
        q = th_quote_get()
    bot.say(q)
