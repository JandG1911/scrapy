#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'WW.JG'

__mtime__ = '2016/10/30'

# code is far away from bugs.

"""
from scrapy.dupefilters import RFPDupeFilter

class SeenURLFilter(RFPDupeFilter):
    def __init__(self, path=None, debug=False):
        self.urls_seen = set()
        RFPDupeFilter.__init__(self, path, debug)

    def request_seen(self, request):
        # if request.url in self.urls_seen:
        return False
        # else:
        #     self.urls_seen.add(request.url)