#-*- coding: utf-8 -*-
"""
quotes.py - Willie Quote Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
from willie.module import commands, rate, example
from random import choice
from urllib import unquote as unconv


def setup(bot):
    if bot.db and not bot.db.preferences.has_columns('quotes'):
        bot.db.preferences.add_columns(['quotes'])


@commands('aq', 'addquote')
@example(".addquote <Meicceli> embolalia can't code")
def quote_add(bot, trigger):
    """Adds a quote to a database"""

    # converts the quote to ascii format
    try:
        args = (trigger.group(2).encode('utf-8'))
    except AttributeError:
        bot.say("Postaas ny joku quote")
        return
    orig = ''

    # checks if there are any quotes added and if so, stores them into orig
    try:
        orig = str(bot.db.preferences.get(trigger.sender, 'quotes').encode("utf8"))
    except TypeError:
        pass

    # Checks if the quote we're adding is already added.
    if args in orig:
        bot.reply("Quote on jo databases")
        return

    # generates the new quote string
    # (I%20am%20a%20quote|Me%20too|I%20am%20as%20well|)
    quote = orig + args + '|'

    # adds the quote to the database
    bot.db.preferences.update(trigger.sender, {'quotes': quote.decode("utf8")})
    bot.reply(u"Quote lisätty'd")


@commands('q', 'quote')
def get_conv(bot, trigger):
    """Gets a random quote from the database"""

    # gets all the quotes, removes the trailing "|", and then splits the
    # quotes into quote_list
    try:
        quote_list = bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|")
    # checks if there are any quotes
    except TypeError:
        bot.reply("Quoteja: ei ole")
        return

    # checks if all the quotes have been deleted
    if len(quote_list) == 1 and quote_list[0] == "":
        bot.reply("Quoteja: ei ole")
        return

    # if a quote number is given, this fetches the quote associated with the
    # given number.
    if trigger.group(2):
        try:
            number = int(trigger.group(2))
            if number > 0:
                output = str(number) + ": " + quote_list[number - 1]
            elif number == 0:
                output = str(number + 1) + ": " + quote_list[0]
            else:
                output = str(len(quote_list) + 1 + number) + ": " + quote_list[number]
        except (ValueError, IndexError):
            bot.say(u"Vittuu noi vammaset argumentit :D inputin pitää olla tarpeex pieni numero ja ei mitää vitun tekstii :D jos hakee haluu nii sit vaa .sq vammamopo")
            return
    # if no quote number is given, this picks a quote randomly
    else:
        # (pseudo-)randomly chooses a quote from quote_list
        ans = choice(quote_list)
        # generates the output (7:%20This%20is%20the%20quote)
        output = str(quote_list.index(ans) + 1) + ": " + ans

    # converts the "%20" etc. back into a readable format (7: This is the
    # quote)
    bot.say(unconv(output))


@commands('dq', 'delquote')
@rate(300)
@example('.delquote 3')
def quote_del(bot, trigger):
    """Deletes a quote from the database."""

    del_key = trigger.group(2).split(" ")

    # gets all the quotes, removes the trailing "|", and then splits the
    # quotes into quote_list
    quote_list = bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|")

    # This if-bit allows only me (meicceli) to delete all the quotes, but
    # allows others to delete one quote per 60 seconds (rate is 60)
    if del_key[0].lower() == "all" and trigger.nick.lower() == "meicceli":
        bot.db.preferences.update(trigger.sender, {'quotes': ""})
        bot.say("rip in pieces quotet")
        return
    elif del_key[0].lower() == "all" and trigger.nick.lower() != "meicceli":
        bot.reply("Vitun peelo ei sul oo oikeuxii tähän :D vinkkasin Meiccelille saatana")
        return
    else:
        pass

    for i in (del_key[0]):
        if i not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            bot.say(u"Yritäs ny xdd")
            return

    if int(del_key[0]) > len(quote_list):
        bot.say(u"Yritäs ny xddd")
        return

    # deletes the item by index shown in the beginning of every quote (for
    # example "5: quote" could be deleted with .delquote 5)
    del quote_list[int(del_key[0]) - 1]

    # This bit makes sure that there won't be any "||" found, which would mess
    # up the splitting in .quote (there would be empty strings in the
    # quote_list)
    modified_list = ""
    for i in quote_list:
        modified_list += i + "|"
    if modified_list.find('||') != 1:
        modified_list = modified_list.replace('||', '|')

    # updates the list with the quote removed
    bot.db.preferences.update(trigger.sender, {'quotes': modified_list})
    bot.reply("Quote poistetu")


@commands('sq', 'squote', 'searchquote')
@example('.sq 3, string1 string2')
def quote_search(bot, trigger):
    """Searches quotes. If you want you can use ", " to assign the quote number you'd like to display."""

    args = trigger.group(2)
    if not args:
        bot.say("Annas ny jotai hakutermei")
        return

    # if ", " found, stores the search number into search_number and the query
    # into search_term. If no ", " found, splits search terms with a space
    # (%20)
    if args.find(', ') != -1:
        args = trigger.group(2).split(", ")
        search_term = args[0].encode('utf-8').split("  ")
        search_number = int(args[1])
    else:
        search_term = trigger.group(2).encode('utf-8').split("  ")
        search_number = 1

    # gets all the quotes, removes the trailing "|", and then splits the
    # quotes into quote_list
    quote_list = bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|")

    # this bit performs the search
    for i in search_term:
        findings = [s for s in quote_list if i.decode("utf8").lower() in s.lower()]

    # if quotes are found, store the quote into output.
    try:
        output = "(" + str(findings.index(findings[search_number - 1]) + 1) + "/" + str(len(findings)) + ") - " + \
            str(quote_list.index(findings[search_number - 1]) + 1) + \
            ": " + findings[search_number - 1]
    except IndexError:
        bot.reply(u"Ei löydy midii")
        return
    bot.reply(unconv(output))


@commands('lq')
@rate(1800)
def quote_listi(bot, trigger):
    quote_list = bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|")
    if len(quote_list) == 1 and quote_list[0] == "":
        bot.say("Quoteja: ei ole")
        return
    if not trigger.group(2):
        bot.reply("Quotei on " + str(len(quote_list)) + " kappaletta.")
    else:
        if len(quote_list) > 5:
            for i in bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|"):
                bot.msg(trigger.nick, unconv(i))
            return
        else:
            for i in bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|"):
                bot.say(unconv(i))
            return
