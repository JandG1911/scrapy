# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from sched import scheduler

from sched import scheduler
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join



class BookItem(Item):
    title = Field()
    author = Field()
    score = Field()
    sum = Field()

class BookLoader(ItemLoader):
    default_item_class = BookItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()