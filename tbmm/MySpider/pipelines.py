# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem


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


class MysqlPipeline(object):

    def __init__(self):
        self.config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'xkyY4220S',
            'db': 'tbmm',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
        }
        self.conn = pymysql.connect(**self.config)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):


        sql ="INSERT INTO tb_model(user_id,avatar_url,city,real_name,total_fan_num,total_favor_num,weight,height)\
                      VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % (item['userId'], item['avatarUrl'], item['city'], \
                      item['realName'], item['totalFanNum'], item['totalFavorNum'], item['weight'], item['height'])
        try:
                self.cursor.execute(sql)
                self.conn.commit()
        except pymysql.Error as e:
                print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        self.conn.close()
        return item