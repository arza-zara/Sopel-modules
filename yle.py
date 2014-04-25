#-*- coding: utf-8 -*-
"""
yle.py - Willie YLE Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
from willie.module import commands, rate, example
from willie import web
import sys
import json



@commands('yletlue', 'yleplue', 'ytlue', 'yplue')
@example('.ytlue 6')
@rate(120)
def yle_tulostus(bot, trigger):
    """Postaa artikkelin nro. 1-12"""
    #Tarkistaa etta kelpoisa numero annettu, ja hakee oikean urlin
    if not trigger.group(2) or trigger.group(2).split(" ")[0] not in ['1', '2', '3', '4']:
        bot.reply("Postaa kunnollinen artikkelin numero (1-12)")
        sys.exit(0)
    if trigger.bytes.find('yletlue') != -1 or trigger.bytes.find('ytlue') != -1:
        url = "https://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=12&q=http://yle.fi/uutiset/rss/uutiset.rss"
        kategoria = "YLE Tuoreimmat"
    if trigger.bytes.find('yleplue') != -1 or trigger.bytes.find('yplue') != -1:
        url = "https://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=12&q=http://yle.fi/uutiset/rss/paauutiset.rss"
        kategoria = u"YLE Pääuutiset"

    #tallentaa inffot muuttujaan resp
    resp = json.loads(web.get(url))

    #tallentaa artikkeleiden lukumaaran
    total = len(resp['responseData']['feed']['entries'])

    #Yrittaa hakea artikkelin sisallon, sen otsikon ja linkin. Jos ei pysty, postaa etta paska input.
    try:
        artikkeli = resp['responseData']['feed']['entries'][int(trigger.group(2).split(" ")[0]) - 1]['content'].split("</p>")
        title = resp['responseData']['feed']['entries'][int(trigger.group(2).split(" ")[0]) - 1]['title']
        #Lyhentaa urlin poistamalla artikkelin nimen urlista
        link = resp['responseData']['feed']['entries'][int(trigger.group(2).split(" ")[0]) - 1]['link'].split("uutiset")[0] + "uutiset/" + resp['responseData']['feed']['entries'][int(trigger.group(2).split(" ")[0]) - 1]['link'].split("/")[-1].split("?")[0]
        if len(artikkeli) < 7:
            bot.say("00" + title + "" + " (" + link + ")")
            for paragraph in artikkeli:
                bot.say(paragraph.replace("<p>", ""))
            return
        else:
            bot.say("00" + title + "" + "(" + link + ")")
            for paragraph in artikkeli:
                bot.msg(trigger.nick, paragraph.replace("<p>", "").replace("<h3>", "00").replace("</h3>", ": "))
            return
    except (ValueError, UnicodeEncodeError, IndexError):
        bot.reply("Paska input. Komento on: <.ylep|.ylet> [1..4|1..12] [lue|cont|content]")
        return

@commands('ylet', 'ylep')
@example('.ylet 3')
@rate(5)
def yle_uusimmat(bot, trigger):
    """Postaa otsikoita. Annettavat numerot ovat 1-4."""

    #Hakee oikean urlin
    if trigger.bytes.find('ylet') != -1:
        url = "https://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=12&q=http://yle.fi/uutiset/rss/uutiset.rss"
        kategoria = "YLE Tuoreimmat"
    if trigger.bytes.find('ylep') != -1:
        url = "https://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=12&q=http://yle.fi/uutiset/rss/paauutiset.rss"
        kategoria = u"YLE Pääuutiset"

    #tallentaa inffot muuttujaan resp
    resp = json.loads(web.get(url))

    #tallentaa artikkeleiden lukumaaran
    total = len(resp['responseData']['feed']['entries'])

    #jos numero on annettu, tarkistaa onko se kelpoisa. muuten else
    if trigger.group(2):
        if trigger.group(2).split(" ")[0] not in ['1', '2', '3' , '4']:
            bot.reply("Numeron on oltava 1, 2, 3 tai 4")
        shown_titles = [trigger.group(2)[0]]
    else:
        shown_titles = ['1']

    output = []
    #ensimmainen artikkeli (1, 4, 7 tai 10)
    first_range = (int(shown_titles[0]) - 1) * 3
    #  viimeinen artikkeli (3, 6, 9 tai 12)
    second_range = int(shown_titles[0]) * 3

    #kay lapi artikkelit, tallentaa titlen ja linkin artikkeliin minka jalkeen lisaa ne outputtiin
    for otsikko in range(first_range, second_range):
        title = resp['responseData']['feed']['entries'][otsikko]['title']
        link = resp['responseData']['feed']['entries'][otsikko]['link'].split("uutiset")[0] + "uutiset/" + resp['responseData']['feed']['entries'][otsikko]['link'].split("/")[-1].split("?")[0]
        output.append("00" + str(otsikko + 1) + ". " + title + " (" + link + ")")

    #artikkelin numero (1-12)
    position = str(first_range + 1) + "-" + str(second_range) + "/" + str(total)

    #lopullinen output
    bot.say(kategoria + " (" + position + "): " + " ".join(output))
