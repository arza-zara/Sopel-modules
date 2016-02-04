"""
oraakkeli.py - Sopel Lintukoto - Oraakkeli Module
Copyright 2015, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""

from sopel.module import commands, nickname_commands
from sopel import web
import requests

@commands('oraakkeli')
@nickname_commands(r".*")
def oraakkeli(bot, trigger):
    url = "http://www.lintukoto.net/viihde/oraakkeli/index.php?html=0&kysymys="
    query = trigger.group(2) or trigger.group(1)
    vastaus = requests.get(url + query)
    bot.reply(vastaus.text)
