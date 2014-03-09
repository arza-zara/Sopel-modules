#Replies with a link in to the channels stats page (http://yoursite.com/stats/channel
#See also http://pisg.sourceforge.net/
from willie.module import commands, example

@commands('stats')
@example('.stats')
def stats(bot, trigger):
    channel = trigger.sender.replace('#', '')
    link = "http://yoursite.com/stats/" + channel

    if channel == "channel_with_custom_location":
        bot.reply("http://yoursite/obscure_location")

    elif channel == "#no_stats_for this channel":
        bot.reply("Sorry, no stats for this channel.")

    else:
        bot.reply(link)
