"""
vimeo.py - Sopel Vimeo Module
Copyright 2015, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
import json
import re

from sopel import web, tools
from sopel.module import commands, example, rule


regex = re.compile('.*(vimeo.com/)([0-9]+)')


def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.SopelMemory()
    bot.memory['url_callbacks'][regex] = vimeo_by_url


@rule('.*(vimeo.com/)([0-9]+)')
def vimeo_by_url(bot, trigger, found_match=None):
    match = found_match or trigger
    videoID = match.group(2)
    apiURL = "https://vimeo.com/api/v2/video/" + videoID + ".json"
    try:
        resp = json.loads(web.get(apiURL))
    except:
        return

    output = u"[Vimeo] "
    output += u"Title: %s" % (str(resp[0]['title']))
    if 'user_name' in resp[0]:
        output += u" | Uploader: %s" % (str(resp[0]['user_name']))
    if 'upload_date' in resp[0]:
        output += u" | Uploaded: %s" % (str(resp[0]['upload_date']))
    if 'duration' in resp[0]:
        output += u" | Duration: %s" % (str(resp[0]['duration']))
    if 'stats_number_of_plays' in resp[0]:
        output += u" | Views : %s" % (str(resp[0]['stats_number_of_plays']))
    if 'stats_number_of_comments' in resp[0]:
        output += u" | Comments: %s" % (str(resp[0]['stats_number_of_comments']))
    if 'stats_number_of_likes' in resp[0]:
        output += u" | Likes: %s" % (str(resp[0]['stats_number_of_likes']))

    bot.say(output)
