# coding=utf8
"""
ask.py - Willie Oraakkeli Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""

from willie.module import commands, nickname_commands
import requests


@commands('oraakkeli')
@nickname_commands(r".*")
def oraakkeli(bot, trigger):
    url = "http://www.lintukoto.net/viihde/oraakkeli/index.php?html=0&kysymys="
    query = trigger.group(2) or trigger.group(1)
    vastaus = requests.get(url + query)
    bot.reply(vastaus.text)
