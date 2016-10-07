#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'WW.JG'

__mtime__ = '2016/10/8'

# code is far away from bugs.

"""

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from ..items import DoubanItem
from scrapy.http import Request

class MySpider(CrawlSpider):
    name = 'doubanc'
    download_delay = 0.5
    allowed_domains = ['book.douban.com']
    start_urls = [
        'https://book.douban.com/tag/'
    ]

    rules = [
        Rule(sle(allow='/subject/\d+/($|\?\w+)'), callback='parse_book', follow=True),
        Rule(sle(allow='/tag/[^/]+/?$'), follow=True),
        Rule(sle(allow='/tag/$'), follow=True),
    ]

    def parse_book(self, response):
        sel = response.xpath('//*[@id="wrapper"]')
        item = DoubanItem()
        item['title'] = sel.xpath('h1/span/text()').extract()[0]
        item['author'] = sel.xpath('//div[@id="info"]/span[1]/a/text()').extract()
        item['score'] = sel.xpath('//strong[@class="ll rating_num "]/text()').re(r' (.*?) ')[0]
        item['people'] = sel.xpath('//span[@property="v:votes"]/text()').extract()[0]
        item['stars5'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/span[2]/text()').extract()[0]
        item['stars4'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/span[4]/text()').extract()[0]
        yield item