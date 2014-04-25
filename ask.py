"""
ask.py - Willie Ask Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
from willie.module import commands
import random


@commands('homopaska')
def randeoaie(bot, trigger):
    answers = ['y', 'n']

    # Stores the message into the variable
    message = trigger.group(2)

    # Checks if the message has both "or" and "&&" in it
    if message.find(' or ') != -1 and message.find(' && ') != -1:
        answer = ""
        # Splits the questions and iterates through them
        for i in message.split(' && '):
            # Answers the "or" questions and appends the answer into
            if i.find(' or ') != -1:
                choices = i.split(' or ')
                answer += random.choice(choices) + " of course! and "
            # Answers the questions without "or"
            else:
                answer += random.choice(answers) + " and "
        bot.reply(answer[:-5])
        return

    # Checks if there is only "or"-questions in the message
    elif message.find(' or ') != -1:
        choices = message.split(' or ')
        bot.reply(random.choice(choices) + " of course!")

    # Checks if there are multiple questions without "or"
    elif message.find(' && ') != -1:
        choices = message.split(' && ')
        output = ""
        for i in choices:
            output += random.choice(answers) + " and "
        bot.reply(output[:-5])

    else:
        bot.reply(random.choice(answers))
