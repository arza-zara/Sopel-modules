# coding: utf8
"""
book.py - Willie Goodreads Module
Copyright © 2015, Marcus Leivo

Licensed under the GNU Lesser General Public
License Version 3 (or greater at your wish).
"""
from __future__ import unicode_literals
from willie import tools
from willie.config import ConfigurationError
from willie.module import commands, rule, example
from urllib import quote, urlopen
import re
import xml.etree.ElementTree as ET


regex = re.compile('.*(goodreads.com/book/show/)([0-9]+)')


def setup(bot):
    try:
        key = str(bot.config.goodreads.apikey)
    except:
        raise ConfigurationError('Could not find the Goodreads \
                                 API key in the config file.')
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.WillieMemory()
    bot.memory['url_callbacks'][regex] = book_by_url


def configure(config):
    """
    The Goodreads API key can be obtained on
    https://www.goodreads.com/api/keys
    | [goodreads] | example | purpose |
    | ----------- | ------- | ------- |
    | apikey | 1b3cfe15768ba29 | Goodreads API key |
    """
    if config.option('Configure Goodreads? (You will need an api key \
                     from https://www.goodreads.com/api/keys)', False):
        config.interactive_add('goodreads', 'apikey', 'API key')


def book_info(book_id, key):
    apifiilu = urlopen("https://www.goodreads.com/book/show/" +
                       book_id + "?format=xml&key=" + key)
    try:
        tree = ET.parse(apifiilu)
    except:
        return None
    root = tree.getroot()
    infot = {}

    infot["id"] = book_id

    infot['title'] = root[1][1].text
    infot['pubyear'] = root[1][14][10].text
    infot['ratingscount'] = root[1][14][13].text
    infot['avgrating'] = root[1][15].text
    infot['pages'] = root[1][16].text

    authors = []
    for author in root[1][23].iter('author'):
        authors.append(author[1].text)
    infot['authors'] = authors

    return infot


@rule('.*(goodreads.com/book/show/)([0-9]+).*')
def book_by_url(bot, trigger, found_match=None):
    match = found_match or trigger

    book_id = match.group(2)
    key = str(bot.config.goodreads.apikey)

    infot = book_info(book_id, key)
    if infot is None:
        return

    title = infot['title']
    authors = infot['authors']
    year = infot['pubyear']
    ratingscount = infot['ratingscount']
    rating = infot['avgrating']
    pages = infot['pages']

    output = "[Goodreads] "
    if title is not None:
        output += "Title: " + title

    if authors is not None:
        output += " | "
        allAuthors = authors[0]
        for author in range(1, len(authors)):
            if len(allAuthors) > 100:
                break
            allAuthors += ", " + authors[author]
        if allAuthors.find(",") != -1:
            output += "Authors: " + allAuthors
        else:
            output += "Author: " + allAuthors

    if year is not None:
        output += " | "
        output += "Year: " + year

    if rating is not None:
        output += " | "
        output += "Rating: " + rating

        if ratingscount is not None:
            output += " (%s ratings)" % (ratingscount)

    if pages is not None:
        output += " | "
        output += "Pages: " + pages

    bot.say(output)


@commands('book', 'kirja')
@example('.book Walden')
def book_by_keywords(bot, trigger):
    """Search a book on Goodreads."""
    key = str(bot.config.goodreads.apikey)
    apifiilu = urlopen("https://www.goodreads.com/search/index.xml?key=" +
                       key + "&q=" + quote(trigger.group(2).encode("utf8")))
    tree = ET.parse(apifiilu)
    root = tree.getroot()
    try:
        eka = root[1][6][0]
    except:
        bot.say("Nothing found.")
        return

    book_id = eka[8][0].text
    title = eka[8][1].text
    author = eka[8][2][1].text
    year = eka[4].text

    rating = eka[7].text
    ratingscount = eka[5].text

    output = "[Goodreads Search] "
    if title is not None:
        output += "Title: " + title
    if author is not None:
        output += " | "
        output += "Author: " + author
    if year is not None:
        output += " | "
        output += "Year: " + year
    if rating is not None:
        output += " | "
        output += "Rating: " + rating
        if ratingscount is not None:
            output += " (%s ratings)" % (ratingscount)
    output += " | Link: https://goodreads.com/book/show/" + book_id
    bot.say(output)
