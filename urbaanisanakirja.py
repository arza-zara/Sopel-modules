#-*- coding: utf-8 -*-
"""
urbaanisanakirja.py - Willie Urbaani Sanakirja Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
from willie.module import commands
from willie import web
from bs4 import BeautifulSoup
from urllib import quote


@commands('us')
def urbaani(bot, trigger):
    haku = trigger.group(2).lower().split(", ")

    # Generoi haettavan sanan sopivaksi urbaanille sanakirjalle (URL)
    hakusana = haku[0].replace(u"ä", "a").replace(u"ö", "o").replace(" ", "-")
    url = "urbaanisanakirja.com/word/" + hakusana + "/"
    qnumero = 1

    # Jos annettu, asettaa quoten numeron ja generoi sitten urlin
    if len(haku) > 1:
        hakusana = haku[1].replace(u"ä", "a").replace(u"ö", "o").replace(" ", "-")
        url = "urbaanisanakirja.com/word/" + hakusana + "/"
        try:
            qnumero = int(haku[0])
        except ValueError, UnicodeEncodeError:
            qnumero = 1
    soup = BeautifulSoup(web.get("http://"+quote(url.encode('utf-8'))))


    # Tarkistaa onko maaritelmia
    if str(soup.find_all("title", attrs={'class': None})[0]) == "<title>404 | Urbaani Sanakirja</title>":
        bot.say("Hakusanalla ei löytynyt tuloksia")
        return

    # Tarkistaa, etta annettu numero on sallituissa rajoissa
    total = len(soup.find_all("p", attrs={'class': None}))
    if qnumero > total or qnumero < 0:
        bot.say("Numero ei vastaa mitään määritelmää.")
        return

    # Hakee up ja down votet
    ups = str(soup.find_all("button", attrs={'class': 'btn btn-vote-up rate-up'})[qnumero-1].contents[1][1:])
    dns = str(soup.find_all("button", attrs={'class': 'btn btn-vote-down rate-down'})[qnumero-1].contents[1][1:])

    # Hakee maaritelman, poistaa <p> ja </p> tagit ja korvaa <br/> tagit kauttamerkilla
    definition = str(soup.find_all("p", attrs={'class': None})[qnumero-1])[3:-4].replace("<br/>", " / ")
    # Jos maaritelma on yli 350 merkkia, pilkkoo maaritelmaa
    if len(definition) > 350:
        definition = definition[0:351] + "..."
    bot.say("Määritelmä " + str(qnumero) + "/" + str(total) + ": " +  definition + " (03" + ups + "|05" + dns + ")")
