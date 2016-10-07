# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from sched import scheduler

from scrapy import Item, Field


class DoubanItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    author = Field()
    score = Field()
    people = Field()
    stars5 = Field()
    stars4 = Field()
