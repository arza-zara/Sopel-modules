"""
siwa.py - Sopel Siwa Module
Copyright 2015, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
from sopel.module import commands
from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import json


# Converttaa sulkemisajan sekunneista tunneiksi ja minuuteiksi
def sulk_auk(aika):
    h = int(aika/60/60)
    m = int((aika-h*60*60)/60)
    s = aika - h*60*60 - m*60
    if s >= 30:
        m += 1
    aika = ""
    if m == 60:
        h += 1
    if h > 0:
        aika += str(h) + "h "
    aika += str(m) + "min"
    if m == 0 and h == 0:
        aika = "IT'S TOO LATE!"
    return aika


# Laskee kauanko aikaa aukeamiseen tai sulkeutumiseen
def siwacount(aukiolot):
    now = datetime.datetime.now()
    tunnit = []
    paiva = int(now.day)

    # Jos joka pv sama aukioloaika (esim. "Joka päivä 7-24", niin lisää
    # aukiolot listaan lauantaille ja sunnuntaille saman ajan.
    # siis ["7-24"] -> ["7-24", "7-24", "7-24"]
    if len(aukiolot) == 1:
        aukiolot.append(aukiolot[0])
        aukiolot.append(aukiolot[0])

    # poistaa turhan paskan aukioloista (<span> yms paskaa). listassa eka (0)
    # on arki, toka (1) lauantai, viimenen (2) sunnuntai
    for i in range(len(aukiolot)):
        aukiolot[i] = aukiolot[i].string

    # 0 on maanantai, splittaa aukeamisajan ja sulkemisajan tunnit-listaan
    # siis "7-24" -> ["7", "24"]
    if 0 <= now.weekday() <= 4:
        tunnit = aukiolot[0].split("-")
    if now.weekday() == 5:
        tunnit = aukiolot[1].split("-")
    if now.weekday() == 6:
        tunnit = aukiolot[2].split("-")

    # converttaa tunnit-listasta str -> int
    # siis "7" -> 7
    for i in range(len(tunnit)):
        try:
            x = int(tunnit[i])
        except:
            return "; Kiinni."
        if int(tunnit[i]) == 24:
            tunnit[i] = 0
        else:
            tunnit[i] = int(tunnit[i])

    # Vertaa tuntia siwan aukeamistuntiin ja sulkeutumistuntiin ts. katsoo
    # onko siwa tällä hetkellä auki ja jos siwa on kiinni, laskee aukeamiseen
    # kuluvan ajan
    if now.hour < tunnit[0]:
        # Eka paska ennen miinusmerkkiä on se hetki kun siwa aukaa. kellonajat
        # convertattu UNIX ajaksi, sillä kahden UNIX ajan erotus on yksiköinä
        # sekunteja mikä taas on helppo converttaa tunneiksi ja minuuteiksi
        # Toka paska siis se hetki kun käyttäjä käyttää komentoa .siwa
        aika = int(datetime.datetime(now.year, now.month, paiva, tunnit[0], 00).strftime("%s")) - int(datetime.datetime.today().strftime("%s"))
        return "; Aukeamiseen aikaa " + sulk_auk(aika)

    # Skenaario: Siwa on auki (laskee sulkeutumiseen menevän ajan)
    if tunnit[0] <= now.hour < tunnit[1]:
        aika = int(datetime.datetime(now.year, now.month, paiva, tunnit[1], 00).strftime("%s")) - int(datetime.datetime.today().strftime("%s"))
        return "; Sulkeutumiseen aikaa " + sulk_auk(aika)

    # Skenaario: siwa kiinni ja kello on välillä [22,24[
    if now.hour >= tunnit[1] and tunnit[1] > tunnit[0]:
        tunnit = ""
        # Tässä pitää tarkastella mikä päivä seuraava päivä on.
        # (ark, la vai su)
        if 0 <= now.weekday()+1 <= 4 or now.weekday()+1 == 7:
            tunnit = aukiolot[0].split("-")
        if now.weekday()+1 == 5:
            tunnit = aukiolot[1].split("-")
        if now.weekday()+1 == 6:
            tunnit = aukiolot[2].split("-")
        # int(paiva)+1 koska siwa aukeaa seuraavana päivänä
        aika = int(datetime.datetime(now.year, now.month, int(paiva)+1, int(tunnit[0]), 00).strftime("%s")) - int(datetime.datetime.today().strftime("%s"))
        return "; Aukeamiseen aikaa " + sulk_auk(aika)

    # Skenaario: Siwa menee kiinni aamuyöllä
    if now.hour >= tunnit[0] and tunnit[0] > tunnit[1]:
        tunnit = ""
        # Tässä pitää tarkastella mikä päivä seuraava päivä on.
        # (ark, la vai su)
        if 0 <= now.weekday()+1 <= 4 or now.weekday()+1 == 7:
            tunnit = aukiolot[0].split("-")
        if now.weekday()+1 == 5:
            tunnit = aukiolot[1].split("-")
        if now.weekday()+1 == 6:
            tunnit = aukiolot[2].split("-")
        # jos siwa menee kiinni puoleltaöin (24) ja siwa on auki
        # niin tää adddaa päivän
        if int(tunnit[1]) == 24 and now.hour >= int(tunnit[0]):
            paiva += 1
        # converttaa tunnit-listasta str -> int ja muuttaa 24->0
        # (python ei ymmärrä 24)
        for i in range(len(tunnit)):
            if int(tunnit[i]) == 24:
                tunnit[i] = 0
            else:
                tunnit[i] = int(tunnit[i])
        aika = int(datetime.datetime(now.year, now.month, int(paiva), int(tunnit[1]), 00).strftime("%s")) - int(datetime.datetime.today().strftime("%s"))
        return "; Sulkeutumiseen aikaa " + sulk_auk(aika)


@commands('siwa')
def siwa(bot, trigger):
    siwa_ja_valintatalo(bot, trigger, "Siwa")

@commands('valintatalo', 'valinta', 'vt')
def valintatalo(bot, trigger):
    siwa_ja_valintatalo(bot, trigger, "Valintatalo")

def siwa_ja_valintatalo(bot, trigger, ketju):
    # Jos trigger.group(2) niin ei hae databasesta
    #return
    kauppasivu = "http://www.siwa.fi/fi/kaupat-ja-aukioloajat/?id="
    kauppaid = ""
    if not (trigger.group(2) and trigger.group(2) != ""):
        if ketju == "Siwa":
            kauppaid = bot.db.get_nick_value(trigger.nick, 'siwaid')
        if ketju == "Valintatalo":
            kauppaid = bot.db.get_nick_value(trigger.nick, 'valintataloid')
        if not kauppaid:
            bot.say(u"Joo elix vedäs ny .setsiwa ekax tai sit postaa joku hakutermi.")
            return
        else:
            kauppasivu += kauppaid

    # Jos käyttäjä ei oo tallentanu siwaa itelleen .setsiwa komennol nii
    # tää hakee kaupan sivun kauppaurlin kautta (ensimmäinen hakutulos)
    if kauppaid == "":
        args = trigger.group(2).replace(", ", ",").split(",")
        nro = 1
        hakuUrl = "http://www.siwa.fi/__snippet/keyword/?chain=%s&text=%s" % (ketju, str(quote(args[0])))
        try:
            nro = int(args[-1])
        except:
            pass
        try:
            tulokset = json.loads(urlopen(hakuUrl).read().decode())
            if nro > len(tulokset) or nro < 1:
                nro = 1
            tunnisteID = str(tulokset[nro - 1]['id'])
        except:
            return bot.say("Juu elix haku failas.")
        kauppasivu = "http://www.siwa.fi/fi/kaupat-ja-aukioloajat/?id=" + tunnisteID

    # Jos "kaupat-ja-aukioloajat" paskaa ei löydy kauppasivult nii
    # haku failas (paska hakija)
    if kauppasivu.find("kaupat-ja-aukioloajat") == -1:
        bot.say("Virhe haussa")
        return

    # Hakee kaupan soossit
    try:
        soup = BeautifulSoup(urlopen(kauppasivu).read().decode())
    except:
        return bot.say("Juuh eli kesko ddossaa, kokeile pääsex ite selaimel: " + kauppasivu)

    # ark, la, su
    paivat = soup.find_all("td", attrs={"class": "weekdays"})

    # aukioloajat
    ajat = soup.find_all("td", attrs={"class": "time-inteval"})

    # jos ajat kusee nii kysees 24/7 siwa (esim. etelä-esplanadi)
    try:
        if not ajat[0].string.lower() == "Avoinna 24h".lower():
            count = siwacount(ajat)
        else:
            count = ""
    # jos ajat kusee eik oo 24/7 siwa niin kysees on avaamaton siwa
    except:
        try:
            count = "; " + soup.find("p", attrs={"class": "launch_info"}).string
        except:
            return bot.say("Juuh eli joku kyl kusee nyt siwan sivuil.")

    # kaupan tiedot (osoite, postinumero)
    store_details = soup.find("address").find_all("p")#.string.split(" | ")

    output = ""
    try:
        output = "%s/%s " % (nro, len(tulokset))
    except:
        pass
    for i in store_details:
        output += i.get_text() + ", "
    output = output[:-2] + "; "
    for i in range(len(paivat)):
        output += "%s %s, " % (paivat[i].string, ajat[i].string)
    bot.say(output[:-2].replace("  ", " ") + count)


@commands('setsiwa')
def setsiwa(bot, trigger):
    # Jos pelkkä ".setsiwa" ilman kaupunkia nii käyttäjä on homoseksuaali
    if not trigger.group(2):
        bot.say("yritä edes")
        return
    # Sama hakujuttu ku tossa .siwa komennos
    hakuUrl = "http://www.siwa.fi/__snippet/keyword/?chain=Siwa&text=" + str(quote(trigger.group(2)))
    tulokset = json.loads(urlopen(hakuUrl).read().decode())
    if not tulokset:
        bot.say("Virhe haussa.")
        return
    tunnisteID = str(tulokset[0]['id'])
    bot.db.set_nick_value(trigger.nick, 'siwaid', tunnisteID)
    bot.say("Siwasi on nyt " + tulokset[0]['store'])

@commands('setvalinta', 'setvalintatalo')
def setvalintatalo(bot, trigger):
    # Jos pelkkä ".setsiwa" ilman kaupunkia nii käyttäjä on homoseksuaali
    if not trigger.group(2):
        bot.say("yritä edes")
        return
    # Sama hakujuttu ku tossa .siwa komennos
    hakuUrl = "http://www.siwa.fi/__snippet/keyword/?chain=Valintatalo&text=" + str(quote(trigger.group(2)))
    tulokset = json.loads(urlopen(hakuUrl).read().decode())
    if not tulokset:
        bot.say("Virhe haussa.")
        return
    tunnisteID = str(tulokset[0]['id'])
    bot.db.set_nick_value(trigger.nick, 'valintataloid', tunnisteID)
    bot.say("Valintatalosi on nyt " + tulokset[0]['store'])
