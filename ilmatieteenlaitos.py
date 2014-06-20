# -*- coding: utf-8 -*-
"""
ilmatieteenlaitos.py - Willie Ilmatieteenlaitos Weather Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).

http://willie.dftba.net
"""
from willie.module import commands
from urllib import quote, urlopen, unquote
from bs4 import BeautifulSoup


@commands('saa', u'sää')
def ilmatieteenlaitos(bot, trigger):
    paikkakunta = trigger.group(2)
    # Tarkastaa onko nimimerkki asettanut itselleen paikkakuntaa .setlocationilla
    if not (paikkakunta and paikkakunta != ''):

        if trigger.nick in bot.db.preferences:
            paikkakunta = unquote(bot.db.preferences.get(trigger.nick, 'location')).decode("utf8")

        if not paikkakunta:
            bot.reply("Anna paikkakunta tai aseta sellainen komennolla .setlocation <paikkakunta>")
            return

    # Aliakset
    if paikkakunta.lower() == "hese":
        paikkakunta = "helsinki"
    if paikkakunta.lower() == "perse":
        paikkakunta = "turku"

    # Kaupungin haku
    haku = "http://ilmatieteenlaitos.fi/paikallissaa?p_p_id=locationmenuportlet_WAR_fmiwwwweatherportlets&p_p_lifecycle=2&p_p_mode=view&doAsUserLanguageId=fi_FI&place=" + quote(paikkakunta.encode("utf8"))
    tulokset = urlopen(haku).read().split("\n")
    if str(tulokset).replace(r"\x00", "") == "['']":
        bot.say("Paikkakuntaa ei löytynyt")
        return
    else:
        paikkakunta = str(tulokset[0])

    # Säätietojen haku
    url = "http://ilmatieteenlaitos.fi/saa/" + quote(paikkakunta.decode("utf8").encode("utf8"))
    soup = BeautifulSoup(urlopen(url).read())

    # Lämpötila, kosteus, tuulen nopeus yms.
    infot = soup.find_all("span", attrs={"class": "parameter-name-value"})

    havaintoasema = soup.find_all("option", value=True)
    # Yrittää hakea kellonajan
    try:
        kellonaika = "(%s) " % (str(soup.find_all("span", attrs={"class": "time-stamp"})[0]).split(" ")[0].split(" ")[2])
    except IndexError:
        kellonaika = ""

    # Auringonnousu, -lasku ja päivän pituus
    paivan_pituus = str(soup.find_all("div", attrs={"class": "celestial-text"})[0]).replace('<div class="celestial-text"> ', '')

    # Yrittää hakea havaintoaseman, ja sen löytäessä, lisää havaintoaseman nimen ja kellon ajan outputin alkuun
    try:
        output = str(havaintoasema[0]).replace('</option>', '').split(">")[1]
        output += " %s- " % (kellonaika)

        # Ilmatieteenlaiton heittää autom. Kaisaniemeen jos ei löydä urlilla paikkakuntaa.
        if output == "Helsinki Kaisaniemi" and paikkakunta != "Helsinki":
            bot.say("Paikkakunnalle ei löydy säätietoja")
            return
    except IndexError:
        output = ""

    # Jos paikkakunta löytyy, hakee tiedot ja lisää ne outputtiin
    for i in infot:
        # Poistaa turhaa paskaa + splittaa nimen (esim. "Lämpötila") omaan muuttujaan, ja arvon (esim. 20°C) toiseen
        lista = str(i).replace('<span class="parameter-name-value"><span class="parameter-name">', '').split('</span> <span class="parameter-value">')
        nimi = lista[0]
        arvo = lista[1].replace("</span></span>", "").replace('<span class="parameter-date-time">', '').replace("</span>", "")
        if len(arvo) != 0:
            if arvo[-1] == " ":
                arvo = arvo[:-1]
        output += "%s %s; " % (nimi, arvo)

    # Lisää päivän pituuden yms. outputin perälle ja poistaa turhan paskan lopusta
    output += paivan_pituus.replace("<strong>", "").replace("</strong>", "").replace('<div class="celestial-status"> ', '').replace(".", ";", 1)[:-8]

    bot.say(output)


@commands('setlocation', u'setsää')
def update_location(bot, trigger):
    paikkakunta = trigger.group(2)
    haku = "http://ilmatieteenlaitos.fi/paikallissaa?p_p_id=locationmenuportlet_WAR_fmiwwwweatherportlets&p_p_lifecycle=2&p_p_mode=view&doAsUserLanguageId=fi_FI&place=" + quote(paikkakunta.encode("utf8"))
    tulokset = urlopen(haku).read().split("\n")
    if str(tulokset).replace(r"\x00", "") == "['']":
        bot.say("Paikkakuntaa ei löytynyt")
        return
    else:
        paikkakunta = str(tulokset[0])

    bot.db.preferences.update(trigger.nick, {'location': str(quote(paikkakunta.decode("utf8").encode("utf8")))})
    bot.reply('Paikkakuntasi on nyt ' + paikkakunta)
