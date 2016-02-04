"""
unicafe.py - Willie Unicafe Module
Copyright 2015, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
from sopel.module import commands, example, rate
from sopel import web
import feedparser
import datetime
from dateutil.tz import tzlocal


unicafet = {
    u"metsätalo": "1",
    u"olivia": "2",
    u"porthania": "3",
    u"päärakennus": "4",
    u"portaali": "5",
    u"topelias": "7",
    u"valtiotiede": "8",
    u"ylioppilasaukio": "9",
    u"chemicum": "10",
    u"exactum": "11",
    u"physicum": "12",
    u"meilahti": "13",
    u"ruskeasuo": "14",
    u"soc&kom": "15",
    u"biokeskus": "16",
    u"korona": "17",
    u"viikuna": "18",
    u"ricola": "19",
    u"bulevardi": "20",
    u"albertinkatu": "21",
    u"onnentie": "22",
    u"tukholmankatu": "23",
    u"viertotie": "24",
    u"hämeentie": "25",
    u"sofianlehto": "26",
    u"maantie": "27",
    u"leiritie": "28",
    #u"viola": "29",
    u"domus": "30",
    u"gaudeaumus": "31",
    u"serpens": "33"
}
paivat = {"ma": "1", "ti": "2", "ke": "3", "to": "4", "pe": "5"}

tuetut = []
for i in unicafet:
    tuetut.append(i[:1].upper() + i[1:] + ", ")
tuetut.sort()
tuetut = "".join(tuetut)[:-2]


@rate(10)
@commands('food', 'f', 'uni', 'unicafe')
def ruoka(bot, trigger):
    now = datetime.datetime.now(tzlocal())
    # Kuluva päivä
    day = str(now.weekday() % 7)
    hour = datetime.datetime.today().hour
    if hour >= 16:
        day = str((int(day)+1) % 7)

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
                day = args[1]
            # Jos päivä on postattu kirjaimin niin tsekkaa onko se sallitus
            # muodos (tsekkaa rivi 25)
            else:
                if args[1] in paivat:
                    day = str(int(paivat[args[1]])-1)
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
                day = str(int(args[0])-1)
                ruokala = ""
            elif args[0] in paivat:
                day = str(int(paivat[args[0]]) - 1)
                ruokala = ""
            else:
                bot.say("Yritä edes")
                return
    # Tää paska suorittuu silloin ku ruokalaa ei oo annettu ja kattoo onko sql
    # databaseen tallennettu ruokalaa
    if not (ruokala and ruokala != ''):
        ruokala = bot.db.get_nick_value(trigger.nick, 'hese_unicafe')
        if not ruokala:
            bot.reply("Unicafea: ei ole. Aseta sellane komennol " +
                      ".setunicafe <ravintola> " +
                      "tai postaa .f <ravintola>")
            return
    url = "http://messi.hyyravintolat.fi/rss/fin/" + ruokala
    feed = feedparser.parse(url)
    try:
        paiva = ".".join(str(feed["entries"][int(day)]['title']).split(".")[:-1]) + " - "
    except IndexError:
        bot.say("Ne ankat on menny taas failaa jotai enkä saa fetchattuu menuu")
        return
    safkat = str(feed["entries"][int(day)]['summary_detail']['value'])
    if len(safkat) == 0:
        bot.say("Viikonloppusafkaa: ei ole")
        return
    # Poistoon turha paska (VE, [S], M, L, K, G) yms.
    output = ""
    for i in safkat.split("("):
        output += i.split(").")[-1][:-1] + ";"
    bot.say(paiva + output[:-2])


@rate(10)
@commands('setunicafe')
@example('.setunicafe exactum')
def update_hese_unicafe(bot, trigger):
    if not trigger.group(2):
        bot.say("Postaas ny joku Unicafe. Nää Unicafet on tuettui: " + tuetut)
    ruokala = trigger.group(2).lower()
    if not ruokala in unicafet:
        bot.say("Paskat Unicafet sul. Nää Unicafet on tuettui: " + tuetut)
        return
    # rid on ruokalan urlin numero
    rid = str(unicafet[ruokala])
    # tallentaa rid:n SQL databaseen
    bot.db.set_nick_value(trigger.nick, 'hese_unicafe', rid)
    bot.reply('Sun Unicafe on nyt ' + ruokala[0].upper() + ruokala[1:].lower())
