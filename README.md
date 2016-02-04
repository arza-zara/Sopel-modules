My Sopel modules
=================

My Sopel IRC BOT modules. All modules are created by me (excluding ip-lookup.y) and license
under Eiffel Forum License 2. Note that some modules require "bs4" (BeautifulSoup 4).

almanakka.py
------------
Outputs whose name day it is and which occasion takes place today if any.

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

getstrike.py
------------
Find torrents from [getstrke.net](https://getstrike.net)

ilmatieteenlaitos.py
--------------------
A weather module for Finnish cities. Scrapes weather data from
[ilmatieteenlaitos.fi](http://ilmatieteenlaitos.fi) and gives out accurate
readings. **Requires BeautifulSoup4**

ip-lookup.py
-----
This is a modified version of the original ip.py found
[here](https://github.com/embolalia/Sopel). This version outputs:
* Hostname
* **IP-address**
* ISP
* Country
* **City**
* Region
* **Coordinates**
* **Time Zone**

You can now also use the .ip command to check users' hostname information with
`.ip <username>`, e.g. `.ip Meicceli`

kuha.py
-------
Retrieves random stultifying phrases from [lannistajakuha.com](http://lannistajakuha.com/random)
**Requires BeautifulSoup4**

lastfm.py
---------
Fetches now playing information from last.fm with `.np <username>`. Also includes `.col` and `.fmstatus`.

omdb.py
-------
Fetches information when an imdb link is posted. Can also find movie information.

oraakkeli.py
------------
Answers questions with the command `.oraakkeli`, or by calling your bot eg.
`Sopel, how are you?`. Gets the answers from [lintukoto.net](http://www.lintukoto.net/viihde/oraakkeli/index.php).

s-ryhma.py
----------
Find the opening hours of any Alepa, Prisma, Sale or S-market. Use `.sryhmä` to search any of the stores, or `.alepa` to only search for Alepas.

sanakirja-org.py
----------------
Translates words via [sanakirja.org](http://sanakirja.org/). Syntax is the same as it
is with translate.py, so to translate from English to Swedish, type `.sk :en :se valentine`.
If no languages are given, translates from English to Finnish. Also, if only one language
is given, the word is translated from the given language into Finnish.
**Requires BeautifulSoup4**

siwa.py
-------
Find the opening hours of any Siwa or Valintatalo.

suomisanakirja.py
-----------------
Finds definitions for Finnish words.

unicafe.py
----------
Supports multiple Unicafes in Helsinki. Gets their menus.
**Requires BeautifulSoup4**

urbaanisanakirja.py
-------------------
Gets the definition for a Finnish slang word from
[urbaanisanakirja.com](http://urbaanisanakirja.com).
**Requires BeautifulSoup4**

vimeo.py
--------
Find information on any Vimeo-link.
