#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'WW.JG'

__mtime__ = '2016/10/21'

# code is far away from bugs.

"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.bilibili import BilibiliSpider

settings = get_project_settings()
process = CrawlerProcess(settings=settings)

process.crawl(BilibiliSpider)

process.start()