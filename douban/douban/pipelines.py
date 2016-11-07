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
        # author = pub[0]
        tag = item['tag'][0]
        hashed = self.hashed(title, tag)
        if hashed not in self.hash:
            self.hash.append(hashed)
            author, press = self.desc(pub)
            score = float(item['score'][0]) if item['score'] else ''
            people = int(item['people'][0]) if item['people'] else ''
            content = item['content'][0] if item['content'] else ''
            try:
                items = {
                    'hash': hashed,
                    'title': title,
                    'author': author,
                    'content': content,
                    'score': score,
                    'people': people,
                    'press': press,
                    'tag': tag,
                }
                self.post.insert(items)
                return item
            except:
                items = {
                    'title': title,
                    'content': content,
                    'score': score,
                    'people': people,
                    'tag': tag,
                }
                self.error.insert(items)
                return item

    def desc(self, pub):
        if len(pub) > 4:
            author = "/".join(pub[:-3])
            press = "/".join(pub[-3:])
        else:
            if ('-' or '/' or '年') in pub[-1]:
                author = "/".join(pub[:-2])
                press = "/".join(pub[-2:])
            else:
                author = pub[0]
                press = "/".join(pub[-3:])
        return author, press

    def hashed(self, title, author):
        m = hashlib.md5()
        pwd = (title + author).encode('utf-8')
        m.update(pwd)
        return m.hexdigest()
