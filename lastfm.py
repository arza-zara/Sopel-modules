"""
lastfm.py - last.fm checker for willie bot
Modified by Meicceli

Original can be found here https://github.com/mulcare/willie-modules
Licensing: https://github.com/mulcare/willie-modules/blob/master/LICENSE
"""
from willie import web
from willie.module import commands, example
from bs4 import BeautifulSoup
import json
import sys
import urllib

#Postaa taa luvux 1 jos haluut tulostaa api urlin
postapiurl = 0

#randomin apikey = 1d234424fd93e18d503758bf2714859e
#mun apikey      = 782c02b1c96ae181d83850f050509103

@commands('fm', 'np', 'last', 'lastfm')
def lastfm(willie, trigger):
    user = ''
    if trigger.group(2):
        user = trigger.group(2).replace("@", trigger.nick)
    if not (user and user != ''):
        user = willie.db.get_nick_value(trigger.nick, 'lastfm_user')
        if not user:
            willie.reply("Invalid username given or no username set. Use .fmset to set a username.")
            return
    #username variable prepared for insertion into REST string
    user = user.lower()
    quoted_user = web.quote(user)
    #json formatted output for recent track
    try:
        recent_page = web.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=782c02b1c96ae181d83850f050509103&format=json" % (quoted_user))
    except Exception, e:
        willie.say("last.fm is currently having technical difficulties. See .fmstatus for more information.")
        return

    try:
        recent_track = json.loads(recent_page)['recenttracks']['track'][0]
    except KeyError:
        willie.say("Couldn't find user")
        sys.exit(0)
    #artist and track name pulled from recent_track
    quoted_artist = web.quote(recent_track['artist']['#text'])
    quoted_track = web.quote(recent_track['name'])
    #json formatted track info
    trackinfo_page = urllib.urlopen("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&artist=%s&track=%s&username=%s&api_key=782c02b1c96ae181d83850f050509103&format=json" % (quoted_artist, quoted_track, quoted_user))
    if trigger.nick.lower() == "meicceli" and postapiurl == 1:
       willie.say("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&artist=%s&track=%s&username=%s&api_key=782c02b1c96ae181d83850f050509103&format=json" % (quoted_artist, quoted_track, quoted_user))
    #track playcount and loved stats
    trackinfo = json.loads(trackinfo_page.read())['track']
    try:
        playcount = trackinfo['userplaycount']
    except KeyError:
        playcount = "unknown"
    loved = int(trackinfo['userloved'])
    album = '(' + recent_track['album']['#text'] + ') '
    if len(recent_track['album']['#text']) == 0:
        album = ''

    try:
        if loved > 0:
            willie.say('\x035' + u'\u2665' +'\x03 %s - %s %s(%s plays)' % (recent_track['artist']['#text'], recent_track['name'], album, playcount))
        else:
            willie.say('%s - %s %s(%s plays)' % (recent_track['artist']['#text'], recent_track['name'], album, playcount))
    except KeyError:
        willie.say("Couldn't find any recent tracks")


@commands('col')
@example('.col neekeri 1month 4x4 true false true')
def col(willie, trigger):
    """user, type, size, caption, artistonly, playcount"""
    modes = trigger.group()[5:].split()
    user = trigger.group(2)
    if not (user and user != ''):
        user = willie.db.get_nick_value(trigger.nick, 'lastfm_user')
        if not user:
            willie.reply("Invalid username given or no username set. Use .fmset to set a username.")
            return
    if len(modes) == 1:
        willie.say('http://tapmusic.net/lastfm/collage.php?user=%s&type=7day&size=3x3' % (modes[0]))
    elif len(modes) == 2:
        willie.say('http://tapmusic.net/lastfm/collage.php?user=%s&type=%s&size=3x3' % (modes[0], modes[1]))
    elif len(modes) == 3:
        willie.say('http://tapmusic.net/lastfm/collage.php?user=%s&type=%s&size=%s' % (modes[0], modes[1], modes[2]))
    elif len(modes) == 4:
        willie.say('http://tapmusic.net/lastfm/collage.php?user=%s&type=%s&size=%s&caption=%s' % (modes[0], modes[1], modes[2], modes[3]))
    elif len(modes) == 5:
        willie.say('http://tapmusic.net/lastfm/collage.php?user=%s&type=%s&size=%s&caption=%s&artistonly=%s' % (modes[0], modes[1], modes[2], modes[3], modes[4]))
    elif len(modes) == 6:
        willie.say('http://tapmusic.net/lastfm/collage.php?user=%s&type=%s&size=%s&caption=%s&artistonly=%s&playcount=%s' % (modes[0], modes[1], modes[2], modes[3], modes[4], modes[5]))
    elif len(modes) > 6:
        willie.say('Too many arguments! Input has to be: User Period Size Caption ArtistOnly Playcount')
    else:
        willie.say('http://tapmusic.net/lastfm/collage.php?user=%s&type=7day&size=3x3' % (user))



@commands('col2')
def col2(willie, trigger):
    modes = trigger.group()[5:].split()
    user = trigger.group(2)
    if not (user and user != ''):
        user = willie.db.get_nick_value(trigger.nick, 'lastfm_user')
        if not user:
            willie.reply("Invalid username given or no username set. Use .fmset to set a username.")
            return
    if len(modes) == 1:
        willie.say('http://nsfcd.com/lastfm/collage.php?user=%s&type=7day&size=3x3' % (modes[0]))
    elif len(modes) == 2:
        willie.say('http://nsfcd.com/lastfm/collage.php?user=%s&type=%s&size=3x3' % (modes[0], modes[1]))
    elif len(modes) == 3:
        willie.say('http://nsfcd.com/lastfm/collage.php?user=%s&type=%s&size=%s' % (modes[0], modes[1], modes[2]))
    elif len(modes) == 4:
        willie.say('http://nsfcd.com/lastfm/collage.php?user=%s&type=%s&size=%s&caption=%s' % (modes[0], modes[1], modes[2], modes[3]))
    elif len(modes) == 5:
        willie.say('http://nsfcd.com/lastfm/collage.php?user=%s&type=%s&size=%s&caption=%s&artistonly=%s' % (modes[0], modes[1], modes[2], modes[3], modes[4]))
    elif len(modes) == 6:
        willie.say('http://nsfcd.com/lastfm/collage.php?user=%s&type=%s&size=%s&caption=%s&artistonly=%s&playcount=%s' % (modes[0], modes[1], modes[2], modes[3], modes[4], modes[5]))
    elif len(modes) > 6:
        willie.say('Too many arguments! Input has to be: User Period Size Caption ArtistOnly Playcount')
    else:
        willie.say('http://nsfcd.com/lastfm/collage.php?user=%s&type=7day&size=3x3' % (user))



@commands('fmset')
@example('.fmset daftpunk69')
def update_lastfm_user(bot, trigger):
    if not trigger.group(2):
        bot.reply("homo")
        return
    user = trigger.group(2)
    bot.db.set_nick_value(trigger.nick, 'lastfm_user', user)
    bot.reply('Thanks, ' + user)

@commands('fmstatus', 'npstatus')
def fmstatusget(bot, trigger):
    bot.say(get_lastfm_status())

def get_lastfm_status():
    url = "http://status.last.fm/"
    soup = BeautifulSoup(web.get(url))
    output = ""
    statukset = soup.find_all('td', attrs={"class": "statussvc"})
    tilat = soup.find_all('span', attrs={"class": True})
    output = ""
    for i in range(len(statukset)):
        name = statukset[i].text
        status = tilat[i].text[2:]
        output += name + " " + status + "; "
    return(output[:-2])


lastfm.rate = 0
lastfm.priority = 'low'
