#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'WW.JG'

__mtime__ = '2016/10/3'

# code is far away from bugs.

"""
from scrapy_redis.spiders import RedisSpider
import scrapy
from ..items import BookLoader
from scrapy.http import Request
from redis import Redis
from scrapy import log
from time import sleep


class BookSpider(RedisSpider):
    name = 'bookurl'
    download_delay = 1
    # allowed_domain = ['douban.com']
    # start_urls = ['https://book.douban.com/tag/']

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(BookSpider, self).__init__(*args, **kwargs)
        self.url = 'https://book.douban.com/tag/'


    def parse(self, response):
        links = response.xpath('//*[@class="tagCol"]//a/@href').extract()
        for href in links:
            full_url = response.urljoin(href)
            yield Request(full_url, callback=self.parse_tag_per_page)
            # for pageNum in range(0, 200, 20):
            #     full_url = response.urljoin(href + '/?start=' + str(int(pageNum)) + '&type=S')
            #     yield Request(full_url, callback=self.parse_tag_per_page)

    def parse_tag_per_page(self, response):
        # el = BookLoader(response=response)
        r = Redis()
        links = response.xpath("//ul[@class='subject-list']/ul/li")
        for link in links:
            url = link.xpath('div[1]/a/@href').extract()[0]
            r.lpush('myspider:start_urls', url)
            # yield Request(book, callback=self.parse_book)

    # def parse_book(self, response):
    #     item = BookItem()
    #     sel = response.xpath('//div[@id="wrapper"]')
    #     item['title'] = sel.xpath('h1/span/text()').extract()
    #     item['author'] = sel.xpath('//div[@id="info"]/span[1]/a/text()').extract()
    #     item['content'] = sel.xpath('//div[@class="intro"]/p/text()').extract()
    #     yield item