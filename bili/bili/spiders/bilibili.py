# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import FormRequest
from bili.items import BiliItem
from scrapy.conf import settings
from scrapy.shell import inspect_response
import time
import json
import pymongo
import random
import logging

class BilibiliSpider(Spider):
    name = "bilibili"
    allowed_domains = ["bilibili.com"]
    start_urls = (
        'http://www.bilibili.com/',
    )

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Host': 'space.bilibili.com',
            'Origin': 'http://space.bilibili.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://space.bilibili.com/2464864/',
        }
    }

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        self.post = tdb['mid']
        self.current_time = str(round(time.time() * 1000))

    def start_requests(self):
        for mid in range(1, 50950000):
            if self.post.find_one({'_id': mid}) == None:
                url = 'http://space.bilibili.com/ajax/member/GetInfo'
                formdata = {'-': self.current_time,
                        'mid': str(mid)}
                header = {'Referer': 'http://space.bilibili.com/{}/'.format(mid)}
                yield FormRequest(url, callback=self.parse_people, formdata=formdata, headers=header, meta={'mid': mid, 'count': 10})

    def parse_people(self, response):
        mid = response.meta['mid']
        count = response.meta['count']
        if response.status == 404:
            inspect_response(response, self)
        if response.status == (400 or 401 or 403) and count > 0:
            count -= 1
            url = 'http://space.bilibili.com/ajax/member/GetInfo'
            formdata = {'-': self.current_time,
                    'mid': str(mid)}
            header = {'Referer': 'http://space.bilibili.com/{}/'.format(mid)}
            yield FormRequest(url, callback=self.parse_people, formdata=formdata, headers=header, meta={'mid': mid, 'count': count})
        else:
            try:
                jsonBody = json.loads(response.body_as_unicode())
                infos = jsonBody['data']
                item = BiliItem()
                item['mid'] = infos['mid']
                item['name'] = infos['name']
                item['place'] = infos['place']
                item['sex'] = infos['sex']
                item['fans'] = infos['fans']
                item['level'] = infos['level_info']['current_level']
                item['playNum'] = infos['playNum']
                item['brith'] = infos['birthday']
                item['regtime'] = infos['regtime']
                # item['face'] = infos['face']
                yield item
                if infos['mid'][-4:] == '1000':
                    logging.info('crawled {}'.format(infos['mid']))
            except:
                logging.info('Not find mid {}'.format(mid))
