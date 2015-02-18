# coding: utf8
"""
sanakirja-org.py - Willie Sanakirja.org Module
Copyright © 2014, Marcus Leivo

Licensed under the GNU Lesser General Public
License Version 3 (or greater at your wish).
"""
from willie.module import commands, rate
from bs4 import BeautifulSoup
from urllib import quote, urlopen
import re

maatunnus = {"bg": "1", "ee": "2", "en": "3", "es": "4",
             "ep": "5", "it": "6", "el": "7", "lat": "8",
             "lv": "9", "lt": "10", "no": "11", "pt": "12",
             "pl": "13", "fr": "14", "se": "15", "de": "16",
             "fi": "17", "dk": "18", "cz": "19", "tr": "20",
             "hu": "21", "ru": "22", "nl": "23", "jp": "24"}


@rate(10)
@commands("sk", "sanakirja", "sana")
def sanakirja(bot, trigger):
    command = trigger.group(2)

    def langcode(p):
        return p.startswith(':') and (2 < len(p) < 10) and p[1:].isalpha()

    args = ['en', 'fi']

    for i in range(2):
        if ' ' not in command:
            break
        prefix, cmd = command.split(' ', 1)
        if langcode(prefix):
            args[i] = prefix[1:]
            command = cmd
    hakusana = command
    lahdekieli = args[0].lower()
    kohdekieli = args[1].lower()

    if lahdekieli == "fi" and kohdekieli == "fi":
        kohdekieli = "en"

    if lahdekieli not in maatunnus or kohdekieli not in maatunnus:
        bot.say(u"Yritä edes")
        return
    url = "http://www.sanakirja.org/search.php?q=%s&l=%s&l2=%s&dont_switch_languages" % (quote(hakusana.encode("utf8")), maatunnus[lahdekieli], maatunnus[kohdekieli])
    soup = BeautifulSoup(urlopen(url).read())
    output = ""
    # Valitsee vaan kaannokset eika mitaan genetiivei yms.
    pysaytys = 0
    for kaannokset in soup.find_all("table", attrs={"class": "translations"}):
        if pysaytys == 1:
            break
        # <tr class="sk-row(1|2)"> paskeist loytyy kaannokset + ylimaarasta paskaa
        for sk_row in kaannokset.find_all("tr", attrs={"class": re.compile("sk-row")}):
            if pysaytys == 1:
                break
            # ylimaaranen paska vittuun
            for kaannos in sk_row.find_all("a", attrs={"href": re.compile("search")}):
                if len(output + '"%s", ' % kaannos.text.encode("utf8")) < 335:
                    output += '"%s", ' % kaannos.text.encode("utf8")
                else:
                    output += "....."
                    pysaytys = 1
    if output == "":
        for i in soup.find_all("p"):
            if i.text.encode("utf8").find("Automatisoitujen") != -1:
                bot.say(u"Kusipäähomo sanakirja blockaa :D pitää oottaa varmaa jotai 5min tyylii et toimii taas :D")
                return
        bot.say(u"Tuloksia: ei ole. (%s to %s)" % (lahdekieli, kohdekieli))
        return
    bot.say("%s (%s to %s)" % (output[:-2].decode("utf8"), lahdekieli, kohdekieli))
