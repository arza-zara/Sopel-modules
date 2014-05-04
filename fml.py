# coding=utf8
"""
fml.py - Willie FMyLife Module, now in a very compact form!
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
from __future__ import unicode_literals;from willie import web;from willie.module import commands;import xml.etree.ElementTree as ET
@commands('fml')
def fmylife(bot, trigger): bot.say(ET.fromstring(web.get('http://api.fmylife.com/view/random?language=en&key=<YOUR_API_KEY>')).find('items/item/text').text)
