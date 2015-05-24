# coding: utf8
"""
paivyri.py - Willie Päivyri Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).

http://willie.dftba.net
"""
from willie.module import commands
from urllib import urlopen
from bs4 import BeautifulSoup as BS4


@commands(u'almanakka', u'tänään', u'nimipäivät')
def almanakka(bot, trigger):
    url = "http://almanakka.helsinki.fi/fi/"
    soossi = BS4(urlopen(url).read())
    nimet = soossi.find("div", attrs={"id": "rt-sidebar-a"})
    nimet = nimet.find("div", attrs={"class": "module-content"})

    erikoispaiva = unicode(nimet.find_all("p")[0].text)
    nimet = str(nimet.find_all("p")[1])

    nimet = BS4(str(nimet).replace("<br></br>", "").replace(")", ");"))
    nimet = unicode(nimet.text.split(": ")[1][:-1])
    output = ""
    if erikoispaiva != "":
        output += "%s: %s" % (erikoispaiva, nimet)
    else:
        output += nimet
    bot.say(output)
