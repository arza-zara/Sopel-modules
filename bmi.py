"""
bmi.py - Willie Simple bmi-counter (SI-units) Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
from willie.module import commands, example


@commands('bmi')
@example('.bmi 60 1.90')
def bmi(bot, trigger):
    args = trigger.group()[5:].split()
    #Makes sure that both weight and height are given
    if len(args) < 2:
        bot.reply(".bmi <weight> <height>")
        return

    #Saves the first given argument as weight and the second argument as height
    #Converts the decimal pointer into a dot if needed
    weight = str(args[0]).replace(',', '.')
    #Converts the decimal pointer into a dot if needed
    height = str(args[1]).replace(',', '.')

    #Makes sure that there are only digits (and an decimal pointer)
    #in the given weight
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
    for i in range(len(weight)):
        if str(weight[i]) not in numbers:
            bot.reply(".bmi <weight> <height>")
            return

    #Makes sure that there are only digits (and an decimal pointer)
    #in the given height
    for i in range(len(height)):
        if str(height[i]) not in numbers:
            bot.reply(".bmi <weight> <height>")
            return

    #Calculates the bmi and responds accordingly
    else:
        #If the given height is over 3 (metres), the user has presumably
        #given the height in centimetres rather than in metres. This
        #converts the height from centimetres into metres.
        if float(height) > 3:
            height = float(float(height) / 100)

        #Calculates the body mass index
        bodymassindex = float(weight) / float(height) ** 2

        #Calculates how much the user has to lose weight
        #in order to be considered as normal weight
        to_lose = float(weight) - float(height) ** 2 * 17.0
        to_gain = -1 * to_lose

        #Compares the user's bmi into this chart
        #https://en.wikipedia.org/wiki/Body_mass_index#Categories
        if bodymassindex < 15.0:
            bot.reply("Your BMI is %s, very severely underweight. You have to gain %skg to become normal weight." % (bodymassindex, to_gain))
        elif 15.0 <= bodymassindex < 16.0:
            bot.reply("Your BMI is %s, severely underweight. You have to gain %skg to become normal weight." % (bodymassindex, to_gain))
        elif 16.0 <= bodymassindex < 18.5:
            bot.reply("Your BMI is %s, underweight. You have to gain %skg to become normal weight." % (bodymassindex, to_gain))
        elif 18.5 <= bodymassindex < 25.0:
            bot.reply("Your BMI is %s, healthy weight." % (bodymassindex))
        elif 25.0 <= bodymassindex < 30.0:
            bot.reply("Your BMI is %s, overweight. You have to lose %skg to become normal weight." % (bodymassindex, to_lose))
        elif 30.0 <= bodymassindex < 35.0:
            bot.reply("Your BMI is %s, moderately obese. You have to lose %skg to become normal weight." % (bodymassindex, to_lose))
        elif 35.0 <= bodymassindex < 40.0:
            bot.reply("Your BMI is %s, severely obese. You have to lose %skg to become normal weight." % (bodymassindex, to_lose))
        else:
            bot.reply("Your BMI is %s, very severely obese. You have to lose %skg to become normal weight." % (bodymassindex, to_lose))
