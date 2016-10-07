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
    download_delay = 2
    allowed_domains = ['book.douban.com']
    start_urls = [
        'https://book.douban.com/tag/'
    ]

    def parse(self, response):
        links = response.xpath('//*[@class="tagCol"]//a/@href').extract()
        for href in links:
            for pageNum in range(0, 100, 20):
                url = response.urljoin(href + "?start=" + str(int(pageNum)) + "&type=T")
                yield Request(url, callback=self.parse_tag_page)

    def parse_tag_page(self, response):
        links = response.xpath('//*[@id="subject_list"]/ul/li')
        for link in links:
            book = link.xpath('div[1]/a/@href').extract()[0]
            yield Request(book, callback=self.parse_book)

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