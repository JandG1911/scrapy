#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'WW.JG'

__mtime__ = '2016/10/3'

# code is far away from bugs.

"""


from scrapy_redis.spiders import RedisSpider
from ..items import BookLoader


class Bookspider(RedisSpider):
    name = 'book'
    redis_key = 'myspider:start_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Bookspider, self).__init__(*args, **kwargs)

    def parse(self, response):
        el = BookLoader(response=response)
        sel = response.xpath('//*[@id="wrapper"]')
        title = sel.xpath('h1/span/text()').extract()
        author = sel.xpath('//div[@id="info"]/span[1]/a/text()').extract()
        score = sel.xpath('//strong[@class="ll rating_num "]/text()').re(r' (.*?) ')[0]
        sum = sel.xpath('//div[@class="rating_sum"]/span/a/span/text()').extract()[0]
        el.add_value('title', title)
        el.add_value('author', author)
        el.add_value('score', score)
        el.add_value('sum', sum)
        return el.load_item()