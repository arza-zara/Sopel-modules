# coding: utf8
"""
getstrike.py - Willie GetstrikeModule
Copyright © 2015, Marcus Leivo

Licensed under the GNU Lesser General Public
License Version 3 (or greater at your wish).
"""

import json
from willie.module import commands
from urllib import quote, urlopen


def gs_search(hakutermit):
    apiURL = "https://getstrike.net/api/torrents/search/?q=" + quote(hakutermit.encode("utf8"))
    resp = json.loads(urlopen(apiURL).read())[1][0]

    output = ""
    if 'torrent_title'in resp:
        output += "Title: " + resp['torrent_title'] + " | "
    if 'page' in resp:
        output += "Page: " + (resp['page']) + " | "
    if 'download_link':
        output += "Download: " + (resp['download_link']) + " | "
    if 'size' in resp:
        output += "Size: " + resp['size'] + " | "
    if 'seeds' in resp and 'leeches' in resp:
        output += "Seeds/Leeches: " + resp['seeds'] + "/" + resp['leeches'] + " | "
    try:
        return output[:-3]
    except:
        return None


@commands('torrent', 'ts')
def getstrike(bot, trigger):
    if not (trigger.group(2)):
        bot.say("Postaas ny ees yks hakutermi")
        return
    hakutermit = trigger.group(2)
    output = gs_search(hakutermit)
    if output is None:
        bot.say("Ei löytyny ketään")
        return
    bot.say(output)
