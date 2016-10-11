#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'WW.JG'

__mtime__ = '2016/10/2'

# code is far away from bugs.

"""

from scrapy.conf import settings
import random

class ProcessHeaderMidware(object):

    def process_request(self, request, spider):
        ua = random.choice(settings.get('USER_AGENT_LIST'))
#        spider.logger.info(msg='now entring download midware.')
        if ua:
            request.headers['User-Agent'] = ua
 #           spider.logger.info(
  #              'User-Agent is: {} {}'.format(request.headers.get('User-Agent'), request)
   #         )
