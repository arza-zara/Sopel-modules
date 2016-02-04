#coding: utf8
"""
suomisanakirja.py - Willie Suomisanakirja Module
Copyright 2015, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
from sopel.module import commands, example
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import json


def maaritelmaSivulta(maarNro, url):
    source = BeautifulSoup(urlopen(url).read().decode())

    # haetaan urlin takaa määritelmät listaan.
    maaritelmat = source.find("ol").find_all("p")
    # poistetaan maaritelmat listasta tyhjät (eli "") määritelmät, joita löytyy
    # jostain syystä esim. sanan "liesu" määritelmästä.
    for i in maaritelmat:
        if len(i.text) == 0:
            maaritelmat.remove(i)
    # jos käyttäjän postaama määritelmänumero on määritelmien määrää suurempi,
    # niin maarNro = len(maaritelmat)
    maarNro = min(len(maaritelmat), maarNro)
    maaritelma = str(maaritelmat[maarNro - 1].text).strip()
    return [maaritelma, maarNro, len(maaritelmat)]


def maaritelmaHaku(hakusanat):
    # hakutermi ascii(?) muotoon
    hakutermi = quote(hakusanat)

    # katotaan onko käyttäjä antanu hakuun mukaan määritelmän numeroa ja jos ei
    # ole, niin tulostetaan ensimmäinen määritelmä.
    args = hakusanat.replace(", ", ",").split(",")
    maarNro = 1
    try:
        # jos vika termi ei oo integeri nii try-lohko failaa ja maarNro pysyy
        # ykkösenä.
        maarNro = int(args[-1])
        # poistetaan käyttäjän syöttämä numero hakutermeistä ja muutetaan
        # hakutermi ascii(?) muotoon
        hakutermi = quote(" ".join(args[:-1]))
    except:
        pass

    hakuURL = "http://www.suomisanakirja.fi/ajax-search.php?query=" + hakutermi

    # haetaan suomisanakirjan autocompleten jsonin tiedot
    resp = json.loads(urlopen(hakuURL).read().decode())
    # jos suggestionseja ei ole, niin palautetaan "None".
    if len(resp['suggestions']) == 0:
        return None
    # hakutermejä lähiten vastaava sana
    sana = resp['suggestions'][0]
    # url josta määritelmä haetaan
    url = "http://www.suomisanakirja.fi/" + quote(sana)
    return (sana, maaritelmaSivulta(maarNro, url))


@commands('suomisanakirja', 'ss', 'sana')
@example(u'sana mänty, 2')
def suomisanakirja(bot, trigger):
    if not trigger.group(2):
        return bot.say("Haista vittu, vitun homo! Vihaan sua!")

    # sanaJaMaaritelma on tuple, jossa ekana on userin hakusanalla löydetty
    # hakusana, ja tokana määritelmän tiedot listana. jos hakusanoilla ei löydy
    # määritelmää niin maaritelmaHaku palauttaa "None".
    sanaJaMaaritelma = maaritelmaHaku(trigger.group(2))
    if sanaJaMaaritelma is None:
        return bot.say(u"Ei löytyny ketään.")
    sana = sanaJaMaaritelma[0]
    maaritelma = sanaJaMaaritelma[1][0]
    maarNro = sanaJaMaaritelma[1][1]
    maaritelmiaYht = sanaJaMaaritelma[1][2]

    # outputin alkuun sana jonka määritelmä outputataan, isolla alkukirjaimella
    output = sana[0].upper() + sana[1:]
    output += " >> Määritelmä %s/%s: " % (str(maarNro), str(maaritelmiaYht))
    # outputista pois kaikki tupla-spacet
    output += maaritelma.replace("  ", " ")

    # lyhentää outputtia tarvittaessa inhimillisemmäks.
    if len(output) > 350:
        # pistetään outputin sanat listaan
        sanat = output.split(" ")
        # outputti menee kokonaan uusiks
        output = ""
        # looppaa sanat ja lisäilee niitä outputtiin sen verran että outputin
        # pituus pysyy alle 351
        for i in sanat:
            if len(output + i) > 350:
                output += "..."
                break
            output += i + " "
        # poistaa vikan whitespacen
        output[:-1]

    bot.say(output)
