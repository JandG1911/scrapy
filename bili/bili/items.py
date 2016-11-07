# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class BiliItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mid = Field()
    name = Field()
    fans = Field()
    place = Field()
    sex = Field()
    level = Field()
    playNum = Field()
    brith = Field()
    regtime = Field()
    # face = Field()
