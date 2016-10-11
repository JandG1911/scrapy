# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import re
import hashlib
from scrapy.conf import settings


class MongodbPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        self.post = tdb[settings['MONGODB_DOCNAME']]
        self.error = tdb['error']
        self.hash = []

    def process_item(self, item, spider):
        pub = item['pub'][0].strip().split('/')
        title = item['title'][0].strip()
        author = pub[0]
        hashed = self.hashed(title, author)
        if hashed not in self.hash:
            if len(pub) > 3:
                self.hash.append(hashed)
                score = float(item['score'][0]) if item['score'] else ''
                people = int(item['people'][0]) if item['people'] else ''
                content = item['content'][0] if item['content'] else ''
                press, date = self.press_date(pub)
                price = self.price(item['price'], pub)
                perter = self.interperter(pub)
                items = {
                    'hash': hashed,
                    'title': title,
                    'author': author,
                    'content': content,
                    'score': score,
                    'people': people,
                    'interperter': perter,
                    'press': press,
                    'date': date,
                    'price': price,
                }
                self.post.insert(items)
                return item
            else:
                score = float(item['score'][0]) if item['score'] else ''
                people = int(item['people'][0]) if item['people'] else ''
                content = item['content'][0] if item['content'] else ''
                items = {
                    'title': title,
                    'content': content,
                    'score': score,
                    'people': people,
                }
                self.error.inserts(items)
                return item

    def price(self, item, pub):
        if ('-'or '/' or '年') in pub[-1]:
            return ''
        elif item:
            return item[0]
        else:
            return pub[-1]

    def interperter(self, pub):
        if len(pub) > 4:
            return pub[1]
        else:
            return ''

    def press_date(self, pub):
        if ('-'or '/' or '年') not in pub[-1]:
            press = pub[-3]
            date = pub[-2].replace('年', '-').replace('月', '')
            return press, date
        else:
            press = pub[-2]
            date = pub[-1].replace('年', '-').replace('月', '')
            return press, date

    def hashed(self, title, author):
        m = hashlib.md5()
        pwd = (title + author).encode('utf-8')
        m.update(pwd)
        return m.hexdigest()
