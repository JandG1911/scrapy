#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'WW.JG'

__mtime__ = '2016/10/19'

# code is far away from bugs.

"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.zhaopin import ZhaopinSpider

settings = get_project_settings()
process = CrawlerProcess(settings=settings)

process.crawl(ZhaopinSpider)

process.start()