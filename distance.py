#-*- coding: utf-8 -*-
"""
distance.py - Willie Trip Distance & Duration Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
from __future__ import unicode_literals
import json

from willie import web
from willie.module import commands, example


# API URL
api_url = 'http://open.mapquestapi.com/directions/v2/routematrix?key=Fmjtd|luur2q08nh%2Cb5%3Do5-9ab20u&unit=k&from='


@commands('matka', 'dist')
@example(".dist Los Angeles|Seattle")
def dist(bot, trigger):
    """
    .dist <city1> <city2> [pedestrian], or <city1>|<city2>|[pedestrian] if there is whitespace in the names.
    """

    # checks if locations are not given
    if not trigger.group(2):
        bot.reply("'.dist <city1> <city2>' or if there is any whitespace in a city's name then '.dist <city1>|<city2>'")
        return

    args = ''
    # Splits the locations into args. (Los Angeles|Seattle -> ['Los Angeles', 'Seattle'])
    # if no '|' is found then uses spaces to split (Los Angeles Seattle -> ['Los', 'Angeles', 'Seattle'])
    if trigger.group(2).find('|') != -1:
        args = trigger.group(2).split('|')
    else:
        args = trigger.group(2).split(' ')

    # <---- STORING ---->
    # Store the locations into variables

    # Accepted formats for using walking route
    pedestrian_route = ['pedestrian', 'walk', 'walking']

    # Handles cases with two arguments e.g. "London Paris" or "London|Paris"
    if len(args) == 2:
        start = args[0]
        destination = args[1]
        method = "fastest"
    # Handles all the cases with more than two arguments
    elif len(args) >= 3:
        # By default, uses quickest drive time route
        method = "fastest"
        # Checks if the 3rd argument is in pedestrian_route, if not, default is used (quickest drive time route)
        if args[2].lower() in pedestrian_route:
            method = "pedestrian"
        start = args[0]
        destination = args[1]
    else:
        bot.reply("'.dist <city1> <city2>' or if there is any whitespace in a city's name then '.dist <city1>|<city2>'")
        return

    # <---- ALIASES ---->
    if start.lower() == "hese":
        start = "helsinki"
    if destination.lower() == "hese":
        destination = "helsinki"

    if start.lower() == "perse":
        start = "turku"
    if destination.lower() == "perse":
        destination = "turku"

    # <---- RETRIEVES URL DATA ---->
    # Generates the url where to lookup data.
    url = api_url + start + '&to=' + destination + "&routeType=" + method
    resp = json.loads(web.get(url))

    # Checks if given locatios are supported
    if resp['info']['statuscode'] != 0:
        error_message = resp['info']['messages'][0]
        if error_message.find('pedestrian') != -1:
            bot.reply("Exceeded pedestrian maximum gross distance for locations")
            return
        else:
            bot.reply(error_message)
            return

    # <---- OUTPUT ---->
    # Stores the data into variables and generates the output
    else:
        # Gets the distance and converts the distance into an appropriate format
        length = resp['distance'][-1]
        if 1 > length >= 0:
            length = str(round(float(length), 2) * 1000) + "m"
        elif 10 > length >= 1:
            length = str(round(length, 1)) + "km"
        else:
            length = str(int(round(length, 0))) + "km"

        # Gets the duration (which unfortunately, is in seconds)
        duration = resp['time'][-1]
        days = ""
        hours = ""
        minutes = ""
        # Counts how many days and stores the modulus (hours and minutes) into duration
        if duration >= 86400:
            days = int(duration / 86400)
            duration = duration % 86400
        # Counts the hours the same way days are counted
        if duration >= 3600:
            hours = int(duration / 3600)
            duration = duration % 3600
        # Counts the minutes and rounds up if there are 30 or more seconds left
        # over
        if duration >= 60:
            if duration % 60 >= 30:
                minutes = int(duration / 60) + 1
            else:
                minutes = int(duration / 60)

        # Generates the duration output
        duration = ""
        if days != "":
            duration += str(days) + "d "
        if hours != "":
            duration += str(hours) + "h "
        if minutes != "":
            duration += str(minutes) + "min "
        if duration == "":
            duration = "Less than half a minute."

        routetype = ""
        if method == "pedestrian":
            routetype = "(Walking route)"
        bot.reply('Distance: ' + length + ', Duration: ' + duration + routetype)
        return
