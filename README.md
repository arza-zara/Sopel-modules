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

distance.py
-----------
Calculates the trip distance and trip duration between up to 10 given locations.

fml.py
------
Gets a random fml from [fmylife.com](http://fmylife.com).

ilmatieteenlaitos.py
--------------------
A weather module for Finnish cities. Scrapes weather data from
[ilmatieteenlaitos.fi](http://ilmatieteenlaitos.fi) and gives out accurate
readings. Requires BeautifulSoup4.

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

stats.py
--------
Outputs a link to the channel's stats' page, if there is one.

tiny.py
-------
A tinychat module for [tiny.joose.fi](http://tiny.joose.fi)

unicafe.py
----------
Supports multiple Unicafes in Helsinki. Gets their menus.

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
