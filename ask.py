"""
ask.py - Sopel Ask Module
Copyright 2014, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
from sopel.module import commands
from random import choice


@commands('ask', 'kysy')
def rand(bot, trigger):
    vastaukset = ['j xD', 'e xD']

    # Tallentaa viestin ilman annettua komentoa muuttujaan postaus
    if not trigger.group(2):
        bot.say("Vitun neekeri postaas ny joku kysymys :D")
        return
    postaus = trigger.group(2)

    if postaus.find(' vai ') != -1 and postaus.find(' && ') != -1:
        vastaus = ""
        for i in postaus.split(' && '):
            vaihtoehdot = []
            if i.find(' vai ') != -1:
                vaihtoehdot = i.split(' vai ')
                vastaus += choice(vaihtoehdot) + " tietty ja "
            else:
                vastaus += choice(vastaukset) + " ja "
        bot.reply(vastaus[:-4])
        return

    # Tarkistaa esiintyyko viestissa sana "vai"
    elif postaus.find(' vai ') != -1:
        # Leikkaa vastausvaihtoehdot listaan
        vaihtoehdot = postaus.split(' vai ')
        bot.reply(choice(vaihtoehdot) + " tietenki :D")

    elif postaus.find(' && ') != -1:
        vaihtoehdot = postaus.split(' && ')
        output = ""
        for i in vaihtoehdot:
            output += choice(vastaukset) + " ja "
        bot.reply(output[:-4])

    else:
        bot.reply(choice(vastaukset))
