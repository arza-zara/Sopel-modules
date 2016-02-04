"""
s-ryhma.py - Sopel S-Ryhmä Module
Copyright 2015, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
from __future__ import unicode_literals
import json

from sopel import web
from urllib.parse import quote
from sopel.module import commands, example

import datetime


# 11120: Prisma
# 12200: ABC liikennemyymälä
#   101: S-market
#   103: Sale
#   104: Alepa
chainIDs = ['11120', '12200', '101', '103', '104']

def sKauppaLaskeAika(kauppa):
    aukeamisaika = kauppa['opening_times_today']['start_time'].split(":")
    sulkeutumisaika = kauppa['opening_times_today']['end_time'].split(":")

    now = datetime.datetime.now()
    tunnit = now.hour + now.minute/60.0

    kauppaAukeaa = int(aukeamisaika[0]) + int(aukeamisaika[1])/60.0
    kauppaSulkeutuu = int(sulkeutumisaika[0]) + int(sulkeutumisaika[1])/60.0

    output = ""
    if kauppaSulkeutuu < kauppaAukeaa:
        kauppaSulkeutuu += 24
    if tunnit < kauppaAukeaa:
        tunteja = int(kauppaAukeaa - tunnit)
        minuutteja = int(((kauppaAukeaa - tunnit) % 1) * 60)
        output += "Aukeamiseen %sh %smin" % (tunteja, minuutteja)
    if kauppaAukeaa <= tunnit <= kauppaSulkeutuu:
        if kauppaSulkeutuu - kauppaAukeaa == 24:
            return ""
        else:
            tunteja = int(kauppaSulkeutuu - tunnit)
            minuutteja = int(((kauppaSulkeutuu - tunnit) % 1) * 60)
            output += "Sulkeutumiseen %sh %smin" % (tunteja, minuutteja)
    if tunnit > kauppaSulkeutuu:
        kauppaAukeaa = 0
        count = 1

        while kauppaAukeaa <= 0 and count < 7:
            aukeamisaika = kauppa['opening_times'][count]['start_time'].split(":")
            sulkemisaika = kauppa['opening_times'][count]['end_time'].split(":")
            kauppaAukeaa += int(aukeamisaika[0]) + int(aukeamisaika[1])/60.0
            if aukeamisaika == sulkemisaika and ":".join(aukeamisaika) == "00:00":
                return "Totuus: ei aukea"
            count += 1
        if kauppaAukeaa == 0:
            return "Totuus: ei aukea"

        tunteja = int(kauppaAukeaa + (24 - tunnit))
        minuutteja = int((kauppaAukeaa % 1) * 60 + ((1 - (tunnit % 1)) * 60))
        output += "Aukeamiseen %sh %smin" % (tunteja, minuutteja)
    return output


def sKauppaAuki(kauppa):
    aukiolot = []
    for auki in kauppa['opening_times'][:3]:
        aukeaa = auki['start_time']
        kiinni = auki['end_time']
        output = ""

        # Appendaa paivan aukioloajan eteen
        if len(aukiolot) == 0:
            output += "Auki tänään "
        elif len(aukiolot) == 1:
            output += "huomenna "
        else:
            output += "ylihuomenna "

        if aukeaa.find(":00") != -1 and kiinni.find(":00") != -1:
            aukeaa = aukeaa[:-3]
            kiinni = kiinni[:-3]
        # Jos aukeaa 00 ja sulkeutuu 00 niin kauppa on suljettu
        if kiinni == aukeaa and (kiinni in "00:00"):
            output += "suljettu"
        # Jos aukeamis- ja sulkeutumisaika muotoa XX:00
        # niin poistetaan loppunollat
        else:
            if aukeaa == "00" and kiinni == "24":
                output += "24h"
            else:
                output += aukeaa + "-" + kiinni
        aukiolot.append(output)

    return ", ".join(aukiolot)


@commands('s-ryhma', 'jutkus', u's-ryhmä', u'sryhmä', u'sryhma', u'smafia', u's-mafia')
@example('.s-ryhma 00100')
def sryhma(bot, trigger):
    sryhmaHaku(bot, trigger, trigger.group(2))


@commands('alepa')
def alepa(bot, trigger):
    sryhmaHaku(bot, trigger, "alepa " + trigger.group(2))


@commands('sale')
def sale(bot, trigger):
    sryhmaHaku(bot, trigger, "sale " + trigger.group(2))


@commands('smarket', 's-market')
def smarket(bot, trigger):
    sryhmaHaku(bot, trigger, "s-market " + trigger.group(2))


@commands('prisma')
def prisma(bot, trigger):
    sryhmaHaku(bot, trigger, "prisma " + trigger.group(2))


def sryhmaHaku(bot, trigger, hakuTermit):
    url = ""
    nro = 0
    if not (hakuTermit and hakuTermit != ""):
        urlid = bot.db.get_nick_value(trigger.nick, 'sryhmaid')
        if not urlid:
            bot.say("homo")
            return
        else:
            url = "https://karttapalvelu.s-kanava.net/map/serviceapi/search.html?output=json&maxresults=10&value=" + urlid
    else:
        args = hakuTermit.replace(", ", ",").split(",", 1)
        try:
            nro = int(args[1]) - 1
        except:
            pass
        url = "https://karttapalvelu.s-kanava.net/map/serviceapi/search.html?output=json&maxresults=10&value=%s" % (quote(args[0]))
    url += "&chain=" + ",".join(chainIDs)
    try:
        tulokset = json.loads(web.get(url))['pobs']
        kauppa = tulokset[nro]
    except:
        bot.say("Kauppaa ei löytynyt.")
        return

    output = "%s/%s %s" % (str(nro + 1), str(len(tulokset)), kauppa['marketingName'])
    output += " (%s)" % (kauppa['streetAddress'])
    if output == "":
        output = kauppa['name']
    try:
        output += "; " + sKauppaAuki(kauppa)
        output += "; " + sKauppaLaskeAika(kauppa)
        if output[-2:] == "; ":
            output = output[:-2]
    except:
        output += "; Aukioloaikoja: ei ole"
    bot.say(output)


@commands('sets-ryhma', 'setjutkus', u'sets-ryhmä', u'setsryhmä', 'setsryhma', 'setsmafia', 'sets-mafia')
def setsryhma(bot, trigger):
    if not trigger.group(2):
        bot.say("yritä edes")
        return
    hakuUrl = "https://karttapalvelu.s-kanava.net/map/serviceapi/search.html?output=json&maxresults=1&value=" + str(quote(trigger.group(2)))
    hakuUrl += "&chain=" + ",".join(chainIDs)
    tulokset = ""
    try:
        tulokset = json.loads(web.get(hakuUrl))['pobs'][0]
    except:
        bot.say("Virhe haussa.")
        return
    tunnisteID = str(tulokset['id'])
    kaupanNimi = tulokset['marketingName']
    if kaupanNimi == "":
        kaupanNimi = tulokset['name']
    bot.db.set_nick_value(trigger.nick, 'sryhmaid', tunnisteID)
    bot.say("S-kauppasi on nyt " + kaupanNimi)
