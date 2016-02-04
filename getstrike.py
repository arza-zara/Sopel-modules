"""
getstrike.py - Sopel Getstrike Module
Copyright 2015, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
import json
from sopel.module import commands
from urllib.parse import quote
from urllib.request import urlopen


def shortenTorrentURL(url):
    resp = json.loads((urlopen("http://sumc.tk/yourls-api.php?signature=0d847f729b&format=json&action=shorturl&url=" + quote(url))).read().decode())
    return resp['shorturl']


def gs_search(hakutermit):
    apiURL = "https://getstrike.net/api/torrents/search/?q=" + quote(hakutermit)
    resp = json.loads(urlopen(apiURL).read().decode())[1][0]

    output = ""
    if 'torrent_title'in resp:
        output += "Title: " + resp['torrent_title'] + " | "
    if 'page' in resp:
        output += "Page: " + shortenTorrentURL(resp['page']) + " | "
    if 'download_link':
        output += "Download: " + shortenTorrentURL(resp['download_link']) + " | "
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
