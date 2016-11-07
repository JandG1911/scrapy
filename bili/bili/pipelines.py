# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import time
import os
import urllib.request as ur
from scrapy.conf import settings


class BiliPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        self.post = tdb['bili']
        self.mid = tdb['mid']

    def process_item(self, item, spider):
        regtime = time.strftime('%Y-%m-%d', time.localtime(int(item['regtime'])))
        brith = item['brith'][-5:]
        sex = item['sex'] or '保密'
        place = item['place'] or '未知'
        items = {
            'mid': item['mid'],
            'name': item['name'],
            'sex': sex,
            'place': place,
            'fans': item['fans'],
            'level': item['level'],
            'playNum': item['playNum'],
            'brith': brith,
            'regtime': regtime,
        }
        self.post.insert(items)
        self.mid.insert({'_id': int(item['mid'])})
        # self.DownloadImg(item['mid'], item['face'])
        return item

    def DownloadImg(self, name, url):
        dir_path = '{}'.format(settings['IMAGES_STORE'])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = '{0}\{1}.jpg'.format(dir_path, name)
        with open(file_path, 'wb') as f:
            conn = ur.urlopen(url)
            f.write(conn.read())
        f.close()