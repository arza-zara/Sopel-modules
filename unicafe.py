#-*- encoding:utf8 -*-
"""
Unicafe.py - Willie Unicafe Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
from willie.module import commands, example, rate
from willie import web
from bs4 import BeautifulSoup
import datetime
from dateutil.tz import tzlocal


def setup(bot):
    if bot.db and not bot.db.preferences.has_columns('hese_unicafe'):
        bot.db.preferences.add_columns(['hese_unicafe'])

unicafet = {
    u"metsätalo": "1",
    u"olivia": "2",
    u"porthania": "3",
    u"päärakennus": "4",
    u"ylioppilasaukio": "8",
    u"chemicum": "10",
    u"exactum": "11",
    u"meilahti": "13",
    u"ruskeasuo": "14",
    u"biokeskus": "18",
    u"viikuna": "21"}
paivat = {"ma": "1", "ti": "2", "ke": "3", "to": "4", "pe": "5"}


@rate(10)
@commands('food', 'f')
def ruoka(bot, trigger):
    now = datetime.datetime.now(tzlocal())
    # Kuluva päivä
    day = str(now.weekday() + 1)
    # Kuluva viikko
    week = str(now.isocalendar()[1])
    # Kuluva vuosi
    year = str(now.year)

    ruokala = ''
    # Jos annettu argumenttei (.f <jotain>) nii tää tulkitsee annettui termei
    if trigger.group(2):
        args = trigger.group(2).split(" ")
        ruokala = args[0].lower()
        # Jos postattun esim ".f exactum pe" nii args[1] on päivä (day) ja
        # args[0] ruokala
        if len(args) > 1:
            # Jos päivä on annettu numerona niin tää
            if args[1] in ["1", "2", "3", "4", "5"]:
                if int(day) > int(args[1]):
                    week = str(int(week) + 1)
                day = args[1]
            # Jos päivä on postattu kirjaimin niin tsekkaa onko se sallitus
            # muodos (tsekkaa rivi 30)
            else:
                if args[1] in paivat:
                    if int(day) > int(paivat[args[1]]):
                        week = str(int(week) + 1)
                    day = paivat[args[1]]
                else:
                    bot.say(u"Paska päivä sul. Pitää olla ma ti ke to tai pe")
                    return
        # Tsekkaa onko ruokala tuettu
        if ruokala in unicafet:
            ruokala = unicafet[ruokala]
        # Jos ei oo tuettu niin kattoo onko argumenttina päivä, ja jos on niin
        # hakee ruokalan sit erikseen SQL databasest (toi "if not (ruokala...)"
        # juttu tos alempan)
        else:
            if args[0] in ["1", "2", "3", "4", "5"]:
                if int(day) > int(args[0]):
                    week = str(int(week) + 1)
                day = args[0]
                ruokala = ""
            elif args[0] in paivat:
                if int(day) > int(paivat[args[0]]):
                    week = str(int(week) + 1)
                day = paivat[args[0]]
                ruokala = ""
            else:
                bot.say("Yritä edes")
                return
    # Tää paska suorittuu silloin ku ruokalaa ei oo annettu ja kattoo onko sql
    # databaseen tallennettu ruokalaa
    if not (ruokala and ruokala != ''):
        if trigger.nick in bot.db.preferences:
            ruokala = bot.db.preferences.get(trigger.nick, 'hese_unicafe')
        if not ruokala:
            bot.reply("Unicafea: ei ole. Aseta sellane komennol .setunicafe <exactum|chemicum|physicum> tai postaa .f <exactum|chemicum|physicum>")
            return

    # Viikonloppusin postaa ens maanantain setit
    if int(day) > 5:
        day = "1"
        week = str(int(week) + 1)
    weekday = ""
    if day == "1":
        weekday = "maanantai: "
    if day == "2":
        weekday = "tiistai: "
    if day == "3":
        weekday = "keskiviikko: "
    if day == "4":
        weekday = "torstai: "
    if day == "5":
        weekday = "perjantai: "
    url = "http://www.hyyravintolat.fi/lounastyokalu/index.php?option=com_ruokalista&Itemid=29&task=lounaslista_haku&week=" + week + "&day=" + day + "&year=" + year + "&rid=" + ruokala + "&lang=1"
    soup = BeautifulSoup(web.get(url))
    output = ""
    tyyppi = ""
    # Hakee safkat soossista
    for food in soup.find_all('li'):
        # Tyyppi meinaa edullisesti, maukkaasti yms.
        try:
            tyyppi = " (" + food.find_all('span', attrs={'class': 'price'})[0].text + ")"
        except IndexError:
            tyyppi = ""
        try:
            tyyppi = " (" + food.find_all('span', attrs={'class': 'price_disclosed'})[0].text + ")"
        except IndexError:
            pass
        # Hommaa safkan nimen ja yhdistää safkan ja tyypin
        output += str(food.contents[0].encode('utf8')) + str(tyyppi.encode('utf8')) + " / "
    # Tää paska hakee nätimman muodon ruokalalle. Esim. jos vedetään .f exactum
    # nii lopulliseen outputtiin tää vetää exactum -> Exactum
    if output == "":
        bot.say(u"Menua: ei ole. Syyttäkää Unicafejäbii siit.")
        return
    for i in unicafet:
        if unicafet[i] == ruokala:
            ruokala = i[0].upper() + i[1:].lower() + ", "
    # Postaa setit, lopust turhaa paskaa vittuu ja replacelt tupla spacet
    # vittuu (paskan soossin takii niit tulee)
    bot.say(ruokala + weekday + output.decode('utf8')[:-3].replace("  ", " "))


@rate(10)
@commands('setunicafe')
@example('.setunicafe exactum')
def update_hese_unicafe(bot, trigger):
    if not trigger.group(2):
        bot.say("Postaas ny joku Unicafe. Nää Unicafet on tuettui: Metsätalo, Olivia, Porthania, Päärakennus, Ylioppilasaukio, Chemicum, Exactum, Meilahti, Ruskeasuo, Biokeskus, Viikuna")
    ruokala = trigger.group(2).lower()
    if not ruokala in unicafet:
        bot.say("Paskat Unicafet sul. Nää Unicafet on tuettui: Metsätalo, Olivia, Porthania, Päärakennus, Ylioppilasaukio, Chemicum, Exactum, Meilahti, Ruskeasuo, Biokeskus, Viikuna")
        return
    # rid on ruokalan urlin numero
    rid = str(unicafet[ruokala]).encode("utf8")
    # tallentaa rid:n SQL databaseen
    bot.db.preferences.update(trigger.nick, {'hese_unicafe': rid})
    bot.reply('Sun Unicafe on nyt ' + ruokala[0].upper() + ruokala[1:].lower())
