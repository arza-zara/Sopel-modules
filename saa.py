# coding=utf8
"""
weather.py - Willie Open Weather Map Module
Copyright 2014, Marcus Leivo
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).

http://willie.dftba.net
"""
from __future__ import unicode_literals

from willie import web
from willie.module import commands, example

import json
import datetime


def setup(bot):
    # Creates the location columns if they dont exist
    if bot.db and not bot.db.preferences.has_columns('location'):
        bot.db.preferences.add_columns(['location'])


def owm_get(location):
    apiurl = "http://api.openweathermap.org/data/2.5/weather?q=" + location
    resp = json.loads(web.get(apiurl))
    if resp['cod'] == "404":
        return "Error: City not found."

    # Variables
    output = ""
    observation_time = ""
    sunrise = ""
    sunset = ""
    humidity = ""
    temperature = ""
    pressure = ""
    cloudness = ""
    gust = ""
    wind_speed = ""
    wind_direction = ""

    # Times
    if 'dt' in resp:
        # UNIX time -> Readable time (server's timezone)
        observation_time = str(datetime.datetime.fromtimestamp(int(resp['dt'])).strftime('%H:%M:%S'))

    if 'sunrise' in resp['sys']:
        sunrise = "Sunrise: " + \
            str(datetime.datetime.fromtimestamp(int(resp['sys']['sunrise'])).strftime('%H:%M:%S')) + "; "

    if 'sunset' in resp['sys']:
        sunset = "Sunset: " + \
            str(datetime.datetime.fromtimestamp(int(resp['sys']['sunset'])).strftime('%H:%M:%S'))


    # Weather
    if 'humidity' in resp['main']:
        humidity = "Humidity: " + str(resp['main']['humidity']) + "%" + "; "

    if 'temp' in resp['main']:
        temperature = "Temperature: " + str(round(resp['main']['temp'] - 273.15, 1)) + "°C" + "; "

    if 'pressure' in resp['main']:
        pressure = "Air pressure: " + \
            str(resp['main']['pressure']) + "hPa" + "; "

    if 'description' in resp['weather'][0]:
        cloudness = "Sky: " + resp['weather'][0]['description'] + "; "


    # Wind
    if 'gust' in resp['wind']:
        gust = "Gust: " + str(resp['wind']['gust']) + "m/s" + "; "

    if 'speed' in resp['wind']:
        wind_speed = "Wind speed: " + \
            str(resp['wind']['speed']) + "m/s" + "; "

    if 'deg' in resp['wind']:
        wind_direction = "Wind direction: " + \
            str(int(round(resp['wind']['deg'], -1))) + "°" + "; "


    if 'name' in resp:
        output = resp['name'] + " " + observation_time + " - "
    output += temperature
    output += humidity
    output += wind_speed
    output += gust
    output += wind_direction
    output += pressure
    output += cloudness
    output += sunrise
    output += sunset
    output += " (source: openweathermap.org)"

    return output


def location_search(location_to_search):
    search_url = "http://api.openweathermap.org/data/2.5/find?mode=json&q=" + location_to_search
    search_sauce = json.loads(web.get(search_url))

    # Checks if OWM finds the user given location
    if search_sauce['cod'] == "404":
        return False
    elif search_sauce['count'] > 0:
        user_location = search_sauce['list'][0]['name']
        return user_location
    else:
        return False


@commands('sää')
@example('.sää Helsinki')
def saa_owm(bot, trigger):
    user_loc = trigger.group(2)

    # If no location given, tries fetching the location from database
    if not (user_loc and user_loc != ''):

        if trigger.nick in bot.db.preferences:
            user_loc = bot.db.preferences.get(trigger.nick, 'location')

        if not user_loc:
            bot.reply("I don't know where you live. " +
                'Give me a location, like .weather London, or tell me where you live by saying .setlocation London, for example.')
            return

    # Find the proper location name to look up weather data from
    location = location_search(user_loc)
    if location != False:
        bot.say(owm_get(location))
    else:
        bot.reply("Location not found")

@commands('setlocation', 'setwoeid')
@example('.setlocation Columbus, OH')
def update_location(bot, trigger):
    """Set your default weather location."""
    user_location = location_search(trigger.group(2))

    bot.db.preferences.update(trigger.nick, {'location': user_location})
    if user_location is None:
        bot.reply("Location not found.")
    bot.reply('I now have you at ' + user_location)
