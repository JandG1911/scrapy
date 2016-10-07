# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

class MongodbPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        # if int(item['people']) >= 300 and float(item['score']) >= 7.5:
        item['score'] = float(item['score'])
        item['author'] = r'/'.join(item['author'])
        item['people'] = int(item['people'])
        self.post.insert(dict(item))
        return item

