# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LagouItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    job_request = Field()
    addr = Field()
    job_bt3 = Field()
    job_bt2 = Field()
    job_bt1 = Field()