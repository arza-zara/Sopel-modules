# -*- coding: utf-8 -*-
"""
siwa.py - Willie Siwa Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
from willie.module import commands
from urllib import quote, urlopen
from bs4 import BeautifulSoup
import datetime


def setup(bot):
    if bot.db and not bot.db.preferences.has_columns('siwaid'):
        bot.db.preferences.add_columns(['siwaid'])

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
    # Jos trigger.group(2) niin ei hae databasesta
    if trigger.group(2):
        kauppaurl = "http://www.siwa.fi/fi/kaupat-ja-aukioloajat/?nearestStore=" + str(quote(trigger.group(2).encode('utf8')))
    kauppasivu = ""
    if not (trigger.group(2) and trigger.group(2) != ""):

        # hommaa siwa IDn databasesta ja tallentaa urlin kauppasivu muuttujaan
        if trigger.nick in bot.db.preferences:
            kauppasivu = "http://www.siwa.fi/fi/kaupat-ja-aukioloajat/?id=" + bot.db.preferences.get(trigger.nick, 'siwaid')
        else:
            bot.say("homo")
            return

    # Jos käyttäjä ei oo tallentanu siwaa itelleen .setsiwa komennol nii
    # tää hakee kaupan sivun kauppaurlin kautta (ensimmäinen hakutulos)
    if kauppasivu == "":
        soup = BeautifulSoup(urlopen(kauppaurl).read())
        for a in soup.find_all("a", href=True):
            if a['href'].find("id=") != -1:
                # splitillä turha paska urlista vittuun
                kauppasivu = a['href'].split("&")[0]
                break

    # Jos "kaupat-ja-aukioloajat" paskaa ei löydy kauppasivult nii
    # haku failas (paska hakija)
    if kauppasivu.find("kaupat-ja-aukioloajat") == -1:
        bot.say("Virhe haussa")
        return

    # Hakee kaupan soossit
    soup = BeautifulSoup(urlopen(kauppasivu).read())

    # ark, la, su
    paivat = soup.find_all("span", attrs={"class": "weekdays"})

    # aukioloajat
    ajat = soup.find_all("span", attrs={"class": "time-inteval"})

    # jos ajat kusee nii kysees 24/7 siwa (esim. etelä-esplanadi)
    try:
        if not ajat[0].string.lower() == "Avoinna 24h".lower():
            count = siwacount(ajat)
        else:
            count = ""
    # jos ajat kusee eik oo 24/7 siwa niin kysees on avaamaton siwa
    except IndexError:
        count = "; " + soup.find("p", attrs={"class": "launch-info"}).string.encode('utf8')

    # kaupan tiedot (osoite, postinumero)
    store_details = soup.find("div", attrs={"id": "store-details"}).find("p").string.split(" | ")

    output = store_details[-1][:-1] + " " + store_details[1] + ", " + store_details[0][1:] + "; "
    for i in range(len(paivat)):
        output += "%s %s, " % (paivat[i].string, ajat[i].string)
    bot.say(output[:-2].replace("  ", " ") + count.decode('utf8'))


@commands('setsiwa')
def setsiwa(bot, trigger):
    # Jos pelkkä ".setsiwa" ilman kaupunkia nii käyttäjä on homoseksuaali
    if not trigger.group(2):
        bot.say("yritä edes")
        return
    # Sama hakujuttu ku tossa .siwa komennos
    kauppaurl = "http://www.siwa.fi/fi/kaupat-ja-aukioloajat/?nearestStore=" + quote(trigger.group(2).encode('utf8'))
    kauppasivu = ""
    soup = BeautifulSoup(urlopen(kauppaurl).read())
    for a in soup.find_all("a", href=True):
        if a['href'].find("id=") != -1:
            kauppasivu = a['href']
            bot.db.preferences.update(trigger.nick, {'siwaid': str(kauppasivu.split("&")[0].split("id=")[-1])})
            break
    if kauppasivu == "":
        bot.say("Virhe haussa")
        return
    # splitillä turha paska urlista vittuun
    soup = BeautifulSoup(urlopen(kauppasivu.split("&")[0]).read())
    store_details = soup.find("div", attrs={"id": "store-details"}).find("p").string.split(" | ")
    output = store_details[-1][:-1] + ", " + store_details[0][1:]
    bot.say("Siwasi on nyt " + output)
