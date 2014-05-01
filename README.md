My willie modules
=================

My willie IRC BOT modules. All modules are created by me and licensed under GNU
LGPLv3, except ip.py and lastfm.py (see inside the files for more information).
Note that the modules "urbaanisanakirja.py" and "fml.py" have a dependency
"bs4" (BeautifulSoup 4).

ask.py
------
Answers a question with an answer defined in the module.

You may also ask an "or" question by simply splitting choices with the word
"or". The bot will then randomly choose an answer.

If you want to, you can ask multiple questions at once. Just split your
questions with "&&" and the bot will answer each question accordingly.

bmi.py
------
Calculates the bmi from given arguments and compares the bmi with
[this chart](https://en.wikipedia.org/wiki/Body_mass_index#Categories).

Input is `<weight> <height>`(kilograms and metres/centimetres).

distance.py
-----------
Calculates the trip distance and trip duration between two given locations.

fml.py
------
Gets a random fml from [fmylife.com](http://fmylife.com/random). There are
problems with fmls that include non-ascii characters but I'm too lazy to try
and fix that myself.
**Requires BeautifulSoup4**

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

stats.py
--------
Outputs a link to the channel's stats' page, if there is one.

tiny.py
-------
A tinychat module for [tiny.joose.fi]

urbaanisanakirja.py
-------------------
Gets the definition for a Finnish slang word for [urbaanisanakirja.com].
**Requires BeautifulSoup4**

yle.py
------
Finds the latest news from [yle.fi] and outputs the articles if wanted. I made
this module just because and it really isn't very convenient for actually
checking the news.
