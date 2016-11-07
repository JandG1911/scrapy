import re
import random
import base64
import pymongo
from scrapy import log

class RandomProxy(object):
    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        fin = open(self.proxy_list)
		client = pymongo.MongoClient(host='127.0.0.1', port=27017)
		self.post = client['Proxy']['proxy']
		self.proxies = self.post.find_one({})

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta or self.proxies == None:
            return

        proxy_address = '{}://{}:{}'.format(self.proxies['http'], self,proxies['_id'], self.proxies['port'])

        request.meta['proxy'] = proxy_address
        
    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        log.msg('Removing failed proxy <%s>, %d proxies left' % (
                    proxy, self.post.find({}).count())
        try:
            self.post.remove(self.proxies)
        except ValueError:
            pass