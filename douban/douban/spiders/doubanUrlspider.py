#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'WW.JG'

__mtime__ = '2016/10/3'

# code is far away from bugs.

"""
# from scrapy.contrib.spiders import CrawlSpider, Rule
from ..items import DoubanItem
from scrapy import Spider
from scrapy.http import Request
# from scrapy.linkextractors import LinkExtractor as sle
from scrapy import log


class Myspider(Spider):
    name = 'douban'
    download_delay = 1.25
    allowed_domains = ['book.douban.com']
    start_urls = [
        'https://book.douban.com/tag/'
    ]

    def parse(self, response):
        links = response.xpath('//*[@class="tagCol"]//a/@href').extract()
        for href in links:
            url = response.urljoin(href)
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        for sel in response.xpath('//div[@class="info"]'):
            item = DoubanItem()
            item['title'] = sel.xpath('h2/a/text()').extract()
            item['score'] = sel.xpath('div[2]/span[2]/text()').extract()
            item['people'] = sel.xpath('div[2]/span[3]/text()').re('(\d+)人')
            item['pub'] = sel.xpath('div[@class="pub"]/text()').extract()
            # item['price'] = sel.xpath('div[3]/div[2]/span/a/text()').re('(\d+\.\d+)')
            item['content'] = sel.xpath('p/text()').extract()
            item['tag'] = response.xpath('//div[@id="content"]/h1/text()').re(': (.*)$')
            yield item

        next = response.xpath('//span[@class="next"]/a/@href').extract()
        if next:
            url = response.urljoin(next[0])
            yield Request(url, callback=self.parse_item)