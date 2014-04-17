"""
ask.py - Willie Ask Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""

from willie.module import commands
from random import choice


@commands('ask')
def rand(bot, trigger):
    answers = ['yes.', 'no.', 'maybe.']

    #Saves the message without the ".ask " part into a variable
    message = trigger.group().replace('.ask ', '')

    #Checks if there's the word "or" in the message
    if message.find(' or ') != -1:
        #Cuts the user given choices into a list
        user_choices = message.split(' or ')
        bot.reply(choice(user_choices) + " of course!")

    #If there is no word "or" in the user's message,
    #then just reply with a pseudorandom answer
    else:
        bot.reply(choice(answers))
