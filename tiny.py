#-*- coding: utf-8 -*-
"""
tiny.py - Willie Tinychat Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
import json

from willie import web
from willie.module import commands
from urllib import quote

api_url = "http://tiny.joose.fi/api/roominfo/"


@commands("tiny")
def tiny_get(bot, trigger):
    """.tiny <room>"""

    if not trigger.group(2):
        bot.reply("You must specify a room!")
        return
    url = api_url + quote(trigger.group(2).encode('utf-8')) + ".json"
    try:
        resp = json.loads(web.get(url))
    except ValueError:
        bot.reply("No such room!")
        return
    if "error" in resp:
        bot.reply(resp["error"])
        return

    room = str(resp['room'])
    users = str(resp['users'])
    broads = str(resp['broadcasting'])
    total = str(resp['users'])
    userlist = []

    for user in range(0, int(users)):
        info = resp['userlist'][user]
        if info["broadcasting"] == 1:
            userlist.append("\x030"+info["user"]+"\x03")
        else:
            userlist.append(info["user"])

    output = "Tinychat - %s (%s/%s broadcasting): %s - http://tiny.joose.fi/?room=%s" % (room, broads, total, " ".join(sorted(userlist)), room)
    bot.say(output)
