My willie modules
=================

My willie IRC BOT modules. All modules are created by me and licensed under GNU
LGPLv3, except ip.py and lastfm.py (see inside the files for more information).
Note that some modules require "bs4" (BeautifulSoup 4).

ask.py
------
Answers a question with an answer defined in the module.

You may also ask an "or" question by simply splitting choices with the word
`or`. The bot will then randomly pick a choice.

If you want to, you can ask multiple questions at once. Just split your
questions with `&&` and the bot will answer each question accordingly.

bmi.py
------
Calculates your bmi and checks if your bmi is in astral tier or not.
Output is in Finnish.

book.py
-------
Search books from [Goodreads.com](https://www.goodreads.com/) and get information
about Goodreads-links leading to a book on Goodreads. An API key is needed and can
be requested [here](https://www.goodreads.com/api/keys).

distance.py
-----------
Calculates the trip distance and trip duration between up to 10 given locations.

es.py
-----
You'll never understand this one.

fml.py
------
Gets a random fml from [fmylife.com](http://fmylife.com).

ilmatieteenlaitos.py
--------------------
A weather module for Finnish cities. Scrapes weather data from
[ilmatieteenlaitos.fi](http://ilmatieteenlaitos.fi) and gives out accurate
readings. **Requires BeautifulSoup4**

ip.py
-----
This is a modified version of the original ip.py found
[here](https://github.com/embolalia/willie). This version outputs:
* Hostname
* **IP-address**
* ISP
* Country
* **City**
* Region
* **Coordinates**
* **Time Zone**

You can now also use the .ip command to check users' hostname information with
.ip `<username>`, e.g. ".ip Meicceli"

kuha.py
-------
Retrieves random stultifying phrases from [lannistajakuha.com](http://lannistajakuha.com/random)
**Requires BeautifulSoup4**

lastfm.py
---------
This is a modified version of the original lastfm.py found
[here](https://github.com/mulcare/willie-modules). This version has an
additional with which you can generate a link to view your
[lastfm collage](http://tapmusic.net/lastfm/).

quotes.py
---------
With this module you can add, delete, get, list, and search quotes. The quotes
are stored into an SQL database.

saa.py (OWM weather)
--------
This module uses the OWM api to get current weather data. The api is kinda quirky
and may or may not give correct readings.

sanakirja-org.py
----------------
Translates words via [sanakirja.org](http://sanakirja.org/). Syntax is the same as it
is with translate.py, so to translate from English to Swedish, type .sk :en :se valentine.
If no languages are given, translates from English to Finnish. Also, if only one language
is given, the word is translated from the given language into Finnish.
**Requires BeautifulSoup4**

stats.py
--------
Outputs a link to the channel's stats' page, if there is one.

thoreau-quote.py
----------------
Uses the Goodreads' website for retrieving quotes from Henry Thoreau.
**Requires BeautifulSoup4**

unicafe.py
----------
Supports multiple Unicafes in Helsinki. Gets their menus.
**Requires BeautifulSoup4**

urbaanisanakirja.py
-------------------
Gets the definition for a Finnish slang word from
[urbaanisanakirja.com](http://urbaanisanakirja.com).
**Requires BeautifulSoup4**

yle.py
------
Finds the latest news from [yle.fi](http://yle.fi/uutiset/) and outputs the
articles if wanted. I made this module just for the lols and it really isn't very
convenient for actually checking the news.
