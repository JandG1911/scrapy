#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'WW.JG'

__mtime__ = '2016/11/3'

# code is far away from bugs.

"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.soda import SodaSpider

settings = get_project_settings()
process = CrawlerProcess(settings=settings)

for i in range(5):
    process.crawl(SodaSpider)

    process.start()