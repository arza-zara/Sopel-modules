"""
omdb.py - Sopel Open Movie Database Module
Copyright 2015, Marcus Leivo <meicceli@sopel.mail.kapsi.fi>

Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
from sopel import tools, web
from sopel.module import commands, rule
import json
import re


regex = re.compile('.*(imdb.com/title/tt([0-9]+)).*')


def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.SopelMemory()
    bot.memory['url_callbacks'][regex] = omdb_url


def omdb_info(movie_id):
    api_url = "http://www.omdbapi.com/?i=" + movie_id
    api_response = json.loads(web.get(api_url))

    if 'Error' in api_response:
        return api_response['Error']

    title = api_response['Title']
    year = api_response['Year']
    rating = api_response['imdbRating']
    genre = api_response['Genre']
    imdb_link = "http://imdb.com/title/" + movie_id

    output = "[MOVIE] Title: %s | Year: %s | Rating: %s | Genre: %s | IMDB Link: %s" % (title, year, rating, genre, imdb_link)
    return output


@commands('imdb', 'movie', 'omdb')
def omdb_command(bot, trigger):
    if not trigger.group(2):
        bot.say("Yritäs ny vitun autisti")
        return

    search_terms = trigger.group(2)
    api_url = "http://www.omdbapi.com/?s=" + search_terms
    api_response = json.loads(web.get(api_url))

    if 'Error' in api_response:
        return bot.say(api_response['Error'])

    movie_id = api_response['Search'][0]['imdbID']
    bot.say(omdb_info(movie_id))
    return


@rule('.*(imdb.com/title/tt([0-9]+)).*')
def omdb_url(bot, trigger, found_match=None):
    match = found_match or trigger
    movie_id = "tt" + match.group(2)
    bot.say(omdb_info(movie_id))
