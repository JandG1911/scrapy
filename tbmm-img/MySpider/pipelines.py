# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib.request as ur
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request


class ImgPipeline(object):

    def process_item(self, item, spider):
        if item['totalFavorNum'] >= 20000:
            spider.logger.info(msg='开始抓取%s的图片' % item['realName'])
            file = item['realName'] + '[' + item['city'] + ']' + item['height'] + '-' + item['weight']
            dir_path = r'%s\%s' % (settings['IMAGES_STORE'], file)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for img_url in item['image_urls']:
                name = img_url.split('/')[-1]
                file_path =r'%s\%s' % (dir_path, name)
                if os.path.exists(file_path):
                    continue
                with open(file_path, 'wb') as f:
                    conn = ur.urlopen(img_url)
                    f.write(conn.read())
                f.close()
        return item


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = '+'.join(request.url.split('/')[-2:])
        return 'full/%s' % (image_guid)

    def get_media_request(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)