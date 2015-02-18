# -*- coding: utf-8 -*-
"""
ilmatieteenlaitos.py - Willie Ilmatieteenlaitos Weather Module
Copyright © 2015, Marcus Leivo

Licensed under the GNU Lesser General Public
License Version 3 (or greater at your wish).
"""
from willie.module import commands
from urllib import quote, urlopen, unquote
from bs4 import BeautifulSoup

def setup(bot):
    if bot.db and not bot.db.preferences.has_columns('location'):
        bot.db.preferences.add_columns(['location'])

@commands('saa', u'sää')
def ilmatieteenlaitos(bot, trigger):
    paikkakunta = trigger.group(2)
    # Tarkastaa onko nimimerkki asettanut itselleen paikkakuntaa .setlocationilla
    if not (paikkakunta and paikkakunta != ''):

        if trigger.nick in bot.db.preferences:
            try:
                paikkakunta = unquote(bot.db.preferences.get(trigger.nick, 'location').encode("utf8"))
            except AttributeError:
                bot.reply("Hnnngh annas ny paikkakunta tai sit aseta default location komennolla .setlocation <paikkakunta>")
                return


        if not paikkakunta:
            bot.reply("Hnnngh annas ny paikkakunta tai sit aseta default location komennolla .setlocation <paikkakunta>")
            return
    else:
        paikkakunta = paikkakunta.encode("utf8")

    # Aliakset
    if paikkakunta.lower() == "hese":
        paikkakunta = "helsinki"
    if paikkakunta.lower() == "perse":
        paikkakunta = "turku"

    # Kaupungin haku
    #haku = "http://ilmatieteenlaitos.fi/paikallissaa?p_p_id=locationmenuportlet_WAR_fmiwwwweatherportlets&p_p_lifecycle=2&p_p_mode=view&doAsUserLanguageId=fi_FI&place=" + quote(paikkakunta)
    haku = "http://ilmatieteenlaitos.fi/saa-ja-meri?p_p_id=locationmenuportlet_WAR_fmiwwwweatherportlets&p_p_lifecycle=2&p_p_mode=view&doAsUserLanguageId=fi_FI&term=" + quote(paikkakunta)
    tulokset = (urlopen(haku).read())[8:].split('",')[0]
    if len(tulokset) < 3:
        bot.say("Paskat paikkakunnat sul :D")
        return
    else:
        paikkakunta = str(tulokset)
        if paikkakunta.find(",") != -1:
            maaJaCity = paikkakunta.split(", ")
            maa = maaJaCity[1]
            city = maaJaCity[0]
            paikkakunta = maa + "/" + city

    # Säätietojen haku
    url = "http://ilmatieteenlaitos.fi/saa/" + quote(paikkakunta.decode("utf8").encode("utf8"))
    soup = BeautifulSoup(urlopen(url).read())

    # Lämpötila, kosteus, tuulen nopeus yms.
    infot = soup.find_all("span", attrs={"class": "parameter-name-value"})

    havaintoasema = soup.find_all("option", value=True)
    # Yrittää hakea kellonajan
    try:
        kellonaika = "(%s) " % (str(soup.find_all("span", attrs={"class": "time-stamp"})[0]).split(" ")[0].split(" ")[2])
        m
    except IndexError:
        kellonaika = ""

    # Auringonnousu, -lasku ja päivän pituus
    try:
        paivan_pituus = str(soup.find_all("div", attrs={"class": "celestial-text"})[0]).replace('<div class="celestial-text"> ', '')
    except IndexError:
        paivan_pituus = ""

    # Yrittää hakea havaintoaseman, ja sen löytäessä, lisää havaintoaseman nimen ja kellon ajan outputin alkuun
    try:
        output = str(havaintoasema[0]).replace('</option>', '').split(">")[1]
        output += " %s- " % (kellonaika)

        # Ilmatieteenlaiton heittää autom. Kaisaniemeen jos ei löydä urlilla paikkakuntaa.
        if output == "Helsinki Kaisaniemi" and paikkakunta != "Helsinki":
            bot.say("Osta uus paikkakunta")
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
    if not paikkakunta:
        bot.say("vitun peelo postaa paikkakunta :D")
        return
    # Aliakset
    if paikkakunta.lower() == "hese":
        paikkakunta = "helsinki"
    if paikkakunta.lower() == "perse":
        paikkakunta = "turku"
    haku = "http://ilmatieteenlaitos.fi/saa-ja-meri?p_p_id=locationmenuportlet_WAR_fmiwwwweatherportlets&p_p_lifecycle=2&p_p_mode=view&doAsUserLanguageId=fi_FI&term=" + quote(paikkakunta.encode("utf8"))
    tulokset = (urlopen(haku).read())[8:].split('",')[0]
    if len(tulokset)<3:
        bot.say("Paskat paikkakunnat sul :D")
        return
    else:
        paikkakunta = str(tulokset)
        if paikkakunta.find(",") != -1:
            maaJaCity = paikkakunta.split(", ")
            maa = maaJaCity[1]
            city = maaJaCity[0]
            paikkakunta = city

    bot.db.preferences.update(trigger.nick, {'location': str(quote(paikkakunta.decode("utf8").encode("utf8")))})
    bot.reply('Paikkakuntas on nyt ' + paikkakunta)
