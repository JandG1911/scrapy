# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class LagouPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        self.db = tdb['lagou']

    def process_item(self, item, spider):
        job_bt = self.bt(item['job_bt3'], item['job_bt2'], item['job_bt1'])
        if '爬虫' in job_bt:
            pay, city, exp = self.job_request(item['job_request'])
            addr = item['addr'][-1].strip()
            title = item['title'][-1].strip()
            items = {
                'title': title,
                'addr': addr,
                'job_bt': job_bt,
                'pay': pay,
                'city': city,
                'exp': exp,
            }
            self.db.insert(items)
            return item

    def bt(self, item3, item2, item1):
        if item3:
            return ''.join(item3)
        elif item2:
            return ''.join(item2)
        else:
            return ''.join(item1)

    def job_request(self, item):
        pay = item[0]
        city = item[1]
        exp = item[2]
        return pay, city, exp
