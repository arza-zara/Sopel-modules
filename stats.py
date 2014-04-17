"""
stats.py - Willie Stats URL Generator Module
Replies with a link to the channel's stats page (http://yoursite.com/stats/channel)

Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).

See also http://pisg.sourceforge.net/
"""
from willie.module import commands, example

@commands('stats')
@example('.stats')
def stats(bot, trigger):
    channel = trigger.sender.replace('#', '')
    link = "http://yoursite.com/stats/" + channel

    if channel == "channel_with_custom_location":
        bot.reply("http://yoursite/obscure_location")

    elif channel == "#no_stats_for_this_channel":
        bot.reply("Sorry, no stats for this channel.")

    else:
        bot.reply(link)
