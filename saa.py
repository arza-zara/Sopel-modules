# coding=utf8
"""
weather.py - Willie Open Weather Map Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).

http://willie.dftba.net
"""
from __future__ import unicode_literals

from willie import web
from willie.module import commands, example

import json
import datetime
import time
import os


def setup(bot):
    # Creates the location columns if they dont exist
    if bot.db and not bot.db.preferences.has_columns('location'):
        bot.db.preferences.add_columns(['location'])


# Gets the weather
def owm_get(location):
    apiurl = "http://api.openweathermap.org/data/2.5/weather?units=metric&q=" + location
    resp = json.loads(web.get(apiurl))
    if resp['cod'] == "404":
        return "Error: City not found."

    # VARIABLES
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

    # TIMES
    # If OWM finds coordinates for the location, tries getting localized sunrise and -set
    if "coord" in resp:
        timeurl = "http://api.geonames.org/timezoneJSON?username=meicceli&lat=" + str(resp["coord"]["lat"]) + "&lng=" + str(resp["coord"]["lon"])
        suntime = json.loads(web.get(timeurl))

        if 'dt' in resp:
            # Localize the time
            os.environ['TZ'] = suntime['timezoneId']
            time.tzset()
            time.tzname
            # UNIX time -> Readable time (server's timezone)
            observation_time = str(datetime.datetime.fromtimestamp(int(resp['dt'])).strftime('%H:%M:%S'))

        # Checks if sunrise and suntime are available and if so, gets them
        if "sunrise" in suntime:
            sunrise = "Sunrise: " + suntime["sunrise"].split(" ")[1] + "; "
        if "sunset" in suntime:
            sunset = "Sunset: " + suntime["sunset"].split(" ")[1] + "; "

    # If OWM cant get the coordinates, tries getting sunrise and sunset from OWM itself. The UNIX time from the api will then not be converted into
    # the location's timezone. Instead it converts the UNIX time to your the server's time Willie is running on.
    else:
        if 'sunrise' in resp['sys']:
            sunrise = "Sunrise: " + str(datetime.datetime.fromtimestamp(int(resp['sys']['sunrise'])).strftime('%H:%M:%S')) + "; "

        if 'sunset' in resp['sys']:
            sunset = "Sunset: " + str(datetime.datetime.fromtimestamp(int(resp['sys']['sunset'])).strftime('%H:%M:%S'))

    # WEATHER
    if 'humidity' in resp['main']:
        humidity = "Humidity: " + str(resp['main']['humidity']) + "%" + "; "

    if 'temp' in resp['main']:
        # Must convert kelvins into Celsius and Fahrenheit
        temp_celsius = str(resp['main']['temp'])
        temperature = "Temperature: " + temp_celsius + "°C; "

    if 'pressure' in resp['main']:
        pressure = "Air pressure: " + \
            str(resp['main']['pressure']) + "hPa" + "; "

    if 'description' in resp['weather'][0]:
        cloudness = resp['weather'][0]['description'] + "; "

    # WIND
    if 'gust' in resp['wind']:
        gust = "Gust: " + str(resp['wind']['gust']) + "m/s" + "; "

    if 'speed' in resp['wind'] and 'deg' in resp['wind']:
        wind_speed = "Wind: " + str(resp['wind']['speed']) + "m/s (" + wind_dir(resp['wind']['deg']) + "); "

    # Generates the output
    if 'name' in resp and 'country' in resp['sys']:
        output = resp['name'] + ", " + resp['sys']['country'] + " " + observation_time + " - "
    output += temperature
    output += wind_speed
    output += gust
    output += humidity
    output += pressure
    output += cloudness
    output += sunrise
    output += sunset
    output += "(openweathermap.org)"

    return output


# Converts wind direction (degrees) into a readable format
def wind_dir(degrees):
    if (degrees >= 354.38 or degrees < 39.38):
        return 'North'
    elif (degrees >= 39.38 and degrees < 84.38):
        return 'Northeast'
    elif (degrees >= 84.38 and degrees < 129.38):
        return 'East'
    elif (degrees >= 129.38 and degrees < 174.38):
        return 'Southeast'
    elif (degrees >= 174.38 and degrees < 219.38):
        return 'South'
    elif (degrees >= 219.38 and degrees < 264.38):
        return 'Southwest'
    elif (degrees >= 264.38 and degrees < 309.38):
        return 'West'
    elif (degrees >= 309.38 and degrees < 354.38):
        return 'Northwest'


# Search for the given location
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


@commands('sää', 'wea', 'weather')
@example('.wea Helsinki')
def saa_owm(bot, trigger):
    user_loc = trigger.group(2)

    # If no location given, tries fetching the location from database
    if not (user_loc and user_loc != ''):

        if trigger.nick in bot.db.preferences:
            user_loc = bot.db.preferences.get(trigger.nick, 'location')

        if not user_loc:
            bot.reply("I don't know where you live. Give me a location, like .weather London, or tell me where you live by saying .setlocation London, for example.")
            return

    # Find the proper location name to look up weather data from
    location = user_loc
    if location is not False:
        bot.say(owm_get(location))
    else:
        bot.reply("Location not found")


@commands('setlocation')
@example('.setlocation Columbus, OH')
def update_location(bot, trigger):
    """Set your default weather location."""
    user_location = location_search(trigger.group(2))

    if user_location is (None or False):
        bot.reply("Location not found.")
        return

    bot.db.preferences.update(trigger.nick, {'location': user_location})
    bot.reply('I now have you at ' + user_location)
