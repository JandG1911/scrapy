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
    download_delay = 1.5
    allowed_domains = ['book.douban.com']
    start_urls = [
        'https://book.douban.com/tag'
    ]
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS":{
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'book.douban.com',
            'Referer': 'https://www.douban.com/',
        },
    }

    rules = [
        Rule(sle(allow='/tag/[^/]+/?$'), callback='parse_item', follow=True),
        Rule(sle(allow='/tag/\?.*$'), follow=True),
    ]

    def parse_item(self, response):
        for sel in response.xpath('//div[@class="info"]'):
            item = DoubanItem()
            item['title'] = sel.xpath('h2/a/text()').extract()
            item['score'] = sel.xpath('div[2]/span[2]/text()').extract()
            item['people'] = sel.xpath('div[2]/span[3]/text()').re('(\d+)人')
            item['pub'] = sel.xpath('div[@class="pub"]/text()').extract()
            item['price'] = sel.xpath('div[3]/div[2]/span/a/text()').re('(\d+\.\d+元)')
            item['content'] = sel.xpath('p/text()').extract()
            yield item
