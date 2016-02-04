"""
es.py - Sopel Euro Shopper Energy Drink DB Module
Copyright 2015, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
from sopel.tools import Identifier
from sopel.module import commands, example
from sopel.formatting import color, colors
from operator import itemgetter
from random import randint
import json


class Kayttaja:

    def __init__(self, nimimerkki, esLista):
        self.nimimerkki = nimimerkki
        self.esLista = esLista


class ES:

    def __init__(self, merkki, arvosanat):
        self.merkki = merkki
        arvosana = 0
        arvioita = 0
        arvostelijoita = 0
        arvosanalista = []
        for userGrades in arvosanat:
            arvostelijoita += 1
            userArvosana = 0
            userArvioita = 0
            for grade in userGrades:
                arvioita += 1
                userArvioita += 1
                userArvosana += float(grade)
                arvosanalista.append(float(grade))
            if userArvioita > 0:
                arvosana += userArvosana / userArvioita
        self.arvostelijoita = arvostelijoita
        self.arvioita = arvioita
        self.arvosana = arvosana / arvostelijoita
        self.arvosanalista = arvosanalista

    def __getitem__(self, key):
        return self.arvosana

    def __str__(self):
        return self.merkki + " = " + onkoHyvaES(self.arvosana)


def onkoEs(es):
    if es.find(".") != -1:
        args = es.upper().split(".")
    else:
        return False
    if len(args) < 2:
        return False
    ekaLuku = args[0]
    tokaLuku = args[1]

    ekaSallitut = ["1", "2", "3", "4"]
    tokaSallitut = ["0", "1", "2", "3", "4", "5", "6",
                    "7", "8", "9", "A", "B", "C", "D", "E"]

    if (ekaLuku in ekaSallitut) and (tokaLuku in tokaSallitut):
        return True
    else:
        return False


def onkoArvosana(arvosana):
    args = arvosana.split("/")
    if len(args) < 2:
        args.append("5")
    if 0 <= float(args[0]) <= 5 and args[1] == "5":
        return True
    else:
        return False


def onkoHyvaES(arvosana):
    if arvosana >= 4:
        return color(str(arvosana), colors.GREEN)
    else:
        return color(str(arvosana), colors.RED)


def isFloat(luku):
    try:
        float(luku)
        return True
    except ValueError:
        return False


@commands('addes')
@example('.addes 1.9 4.5/5')
def addes(bot, trigger):
    if not trigger.group(2):
        bot.say("yritä edes")
#    if (trigger.sender != "#neekeri"
#            and trigger.sender != "#intellektuelli"
#            and (trigger.nick.lower()[:5] != "tuoli"
#            or trigger.nick.lower() != "meicceli")):
#        bot.say("Täl kannul vaan tuolil ja" +
#                " meiccelil on oikeudet arvostella ES")
#        return
    db_fiilu = str(bot.config.es.dbfiilu)

    # avaa ja lataa json fiilun
    f = open(db_fiilu, 'r+')
    resp = json.load(f)
    # fixaa homon "bugin"
    resp = {Identifier(key): value for key, value in resp.iteritems()}

    # tsekkaa onko input sallitussa muodossa
    args = trigger.group(2).split(" ")
    es = args[0].upper()
    arvosana = args[1].replace("/5", "")
    if not isFloat(arvosana) or (not (onkoEs(es) and onkoArvosana(arvosana))):
        bot.say("inputin pitää olla muotoo es ja sit"
                + " arvosana jogiin asteikol esim .addes 1.9 4.5/5")
        f.close()
        return

    # lisaa kayttajalle uuden Es arvosanan
    esat = {}
    # jos kayttaja on aiemmin lisannyt Es niin haetaan kayttajan Es dict
    # ja asetetaan se esat muuttujaan etteivat aiemmat arvosanat poistu
    if trigger.nick in resp:
        esat = resp[trigger.nick]
    arvosanat = []
    if len(esat) > 0 and es in esat:
        arvosanat = esat[es]
    arvosanat.append(arvosana)
    esat[es] = arvosanat
    resp[trigger.nick] = esat
    bot.say("ES lisatty'd")

    f.seek(0)
    json.dump(resp, f)
    f.close()


@commands('deles')
def deles(bot, trigger):
    db_fiilu = str(bot.config.es.dbfiilu)
    f = open(db_fiilu, 'r+')
    resp = json.load(f)
    resp = {Identifier(key): value for key, value in resp.iteritems()}

    args = trigger.group(2).split(" ")
    es = args[0]
    args.append("")
    if not (onkoEs(es)):
        if not (es.lower() == "all" or es.lower() == "kaikki"):
            bot.say("yritäs ny sen inputin kans")
            f.close()
            return

    if trigger.nick in resp:
        if es.lower() == "all" or es.lower() == "kaikki":
            resp[trigger.nick] = {}
            bot.say("kaikki sun es arvostelut heivattu'd vittuun")
        elif es in resp[trigger.nick] and args[1].lower() == "undo":
            del resp[trigger.nick][es][-1]
            if len(resp[trigger.nick][es]) == 0:
                del resp[trigger.nick][es]
        elif es in resp[trigger.nick]:
            del resp[trigger.nick][es]
            bot.say("es poistettu!")
    else:
        bot.say("esää: ei ole")
        return

    f.close()
    f = open(db_fiilu, 'w')
    json.dump(resp, f)
    f.close()


@commands('getes', 'es')
@example('.getEs 1.9')
def getes(bot, trigger):
    db_fiilu = str(bot.config.es.dbfiilu)
    f = open(db_fiilu, 'r')
    resp = json.load(f)
    resp = {Identifier(key): value for key, value in resp.iteritems()}

    kayttajat = luoESkayttajat(resp)
    esOliot = luoESoliot(resp)

    # Argumentteja: ei ole
    if not trigger.group(2):
        randomES = esOliot[randint(0, len(esOliot) - 1)]
        merkki = randomES.merkki
        arvosana = onkoHyvaES(round(randomES.arvosana, 2))
        arvioita = randomES.arvioita
        arvostelijoita = randomES.arvostelijoita
        bot.say("merkki: %s; arvosana: %s; arvostelijoita: %s; arvioitu %s kertaa"
                % (merkki, arvosana, arvostelijoita, arvioita))
        return

    args = trigger.group(2).split(" ")
    # Argumenttina vain topX
    if args[0][:3] == "top" and (args[0] not in resp):
        if not isInt(args[0][3:]):
            bot.say("yritäs ny sen top listan koon (ei se havumäki) kanssa")
            return
        bot.say(topESat(esOliot, int(args[0].split("top")[-1])))
        return

    nikki = args[0].lower()
    # Argumenttina nimimerkki
    if nikki in resp:
        # Nimimerkin lisäksi muita argumentteja
        if len(args) > 1:
            es = args[1].upper()
            # toinen argumentti topX
            if es[:3] == "top" and isInt(es.split("top")[-1]):
                bot.say(userTopES(kayttajat, nikki, int(es.split("top")[-1])))
                return
            # toinen argumentti ES
            elif onkoEs(es):
                if not es in resp[nikki]:
                    bot.say("esää: ei ole")
                    return
                userGrades = sorted(resp[nikki][es], reverse=True)
                total = sum(float(grade) for grade in userGrades)
                arvosana = onkoHyvaES(round(total / len(userGrades), 2))
                bot.say("Arvosana: %s; Kaikki arvosanat: %s"
                        % (arvosana, ", ".join(userGrades)))
                return
        else:
            bot.say(userTopES(kayttajat, nikki, -1))
            return

    # Argumenttina pelkkä ES
    if onkoEs(args[0]):
        es = args[0].upper()
        if len(args) > 1 and (args[1].lower() == "all" or args[1].lower() == "kaikki"):
            for olio in esOliot:
                if es == olio.merkki:
                    esOlio = str(olio)
                    arvosanalista = sorted(olio.arvosanalista)[::-1]
                    bot.say("%s (arvosanat: %s)" % (esOlio, str(arvosanalista)[1:-1]))
                    return
        else:
            for olio in esOliot:
                if es == olio.merkki:
                    esOlio = str(olio)
                    arvioita = olio.arvioita
                    arvostelijoita = olio.arvostelijoita
                    bot.say("%s (arvostelijoita %s, arvosteltu %s kertaa)"
                            % (esOlio, arvostelijoita, arvioita))
                    return
        bot.say("ESää: ei ole")
        return

    bot.say("Inputtis kusee. Luultavasti hakemaas nikkii/esää"
            + " ei oo databases. Tai sit oot kehari xd"
            + " Inputin pitää olla muotoo [nimimerkki] [es|top<int>]")

    f.close()


def luoESkayttajat(resp):
    kayttajat = []
    for nimimerkki in resp:
        esOliot = []
        # Luo käyttäjän ESistä ES oliolistan
        for es in resp[nimimerkki]:
            arvosanat = []
            arvosanat.append(resp[nimimerkki][es])
            esOliot.append(ES(es, arvosanat))
        user = Kayttaja(nimimerkki, esOliot)
        kayttajat.append(user)
    return kayttajat


def luoESoliot(resp):
    # Luodaan ensin lista ESista joita on arvosteltu
    esat = []
    for nimimerkki in resp:
        for es in resp[nimimerkki]:
            if es not in esat:
                esat.append(es)
    esat.sort()

    # Luodaan ES oliot
    luodutESoliot = []
    for es in esat:
        arvosanat = []
        # Haetaan nikin takaa käyttäjän arvosanalista ja lisätään
        # se arvosanat listaan
        for nick in resp:
            if es in resp[nick]:
                # Appendaa listan arvosanoista
                arvosanat.append(resp[nick][es])
        luodutESoliot.append(ES(es, arvosanat))
    return luodutESoliot


def topESat(esOliot, montako):
    # Montako ESaa toplistaan
    if montako == -1 or montako > len(esOliot):
        montako = len(esOliot)
    # Sorttaa ES arvosanojen mukaan
    esatTopList = sorted(esOliot, key=itemgetter('arvosana'), reverse=True)
    output = ""
    for i in range(montako):
        es = esatTopList[i].merkki
        #arvosana = str(onkoHyvaES(esatTopList[i].arvosana))
        arvosana = str(round(esatTopList[i].arvosana, 2))
        if (i == 0):
            es = color(es, 42)
            output += es + " = " + arvosana
        elif (i == 1):
            es = color(es, colors.SILVER)
            output += es + " = " + arvosana
        elif (i == 2):
            es = color(es, 53)
            output += es + " = " + arvosana
        else:
            output += es + " = " + arvosana
        output += "/5, "
    return output[:-2]


def userTopES(kayttajat, nikki, montako):
    userES = []
    for user in kayttajat:
        if user.nimimerkki.lower() == nikki.lower():
            userES = user.esLista
    return topESat(userES, montako)


def isInt(luku):
    try:
        int(luku)
        return True
    except ValueError:
        return False
