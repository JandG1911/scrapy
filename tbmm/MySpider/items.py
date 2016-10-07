# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class tbModelItem(scrapy.Item):
    city = scrapy.Field()
    height = scrapy.Field()
    realName = scrapy.Field()
    totalFanNum = scrapy.Field()
    totalFavorNum = scrapy.Field()
    userId = scrapy.Field()
    weight = scrapy.Field()