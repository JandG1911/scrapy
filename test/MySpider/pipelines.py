# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import json
import codecs
import pymysql
import pymysql.cursors
import pymongo
# from  .items import
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class CleanPipeline(object):

    def __init__(self):
        self.has = set()

    def process_item(self, item, spider):
        if item.keys() >= 5:
            if item in self.has:
                print('error')
            else:
                self.has.add(item)
                return item


class MongodbPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        # if int(item['totalFavorNum']) > 10000 and item['city'] == '杭州市':
        self.post.insert_one(dict(item))
        return item