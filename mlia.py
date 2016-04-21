"""
mlia.py - Sopel My Life is Average Module
Copyright 2014, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
from sopel import web
from sopel.module import commands
from random import randint, choice
from bs4 import BeautifulSoup as BS


def get_mlia():
    site = "http://mylifeisaverage.com/" + str(randint(1, 11000))

    try:
        source = BS(web.get(site))
    except:
        return False

    stories = source.find_all('div', {'class': 'story'})
    story = choice(stories).find_next('div', {'class': 'sc'})

    return story.text.strip()


@commands('mlia')
def mlia(bot, trigger):

    story = ""
    while len(story) >= 400 and story != "":
        story = get_mlia()
        if not story:
            return bot.say("I'm dooooooooooown!")
    bot.say(story)
