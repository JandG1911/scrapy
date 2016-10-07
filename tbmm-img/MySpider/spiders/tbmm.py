import json

from scrapy.contrib.spiders import CrawlSpider
from scrapy import Spider
from ..items import tbModelItem
from scrapy.http import Request
from scrapy.http import FormRequest, Request
from scrapy import log



class tbmmSpider(Spider):
    name = "tbmm"
    download_delay = 0.5
    allow_domians = ["mm.taobao.com"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'authority': 'mm.taobao.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'origin': 'https://mm.taobao.com',
            'referer': 'https://mm.taobao.com/search_tstar_model.htm?spm=719.1001036.1998606017.2.KDdsmP',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'cookie': 'cna=/oN/DGwUYmYCATFN+mKOnP/h; tracknick=adimtxg; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; thw=cn; v=0; cookie2=1b2b42f305311a91800c25231d60f65b; t=1d8c593caba8306c5833e5c8c2815f29; _tb_token_=7e6377338dee7; CNZZDATA30064598=cnzz_eid%3D1220334357-1464871305-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1464871305; CNZZDATA30063600=cnzz_eid%3D1139262023-1464874171-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1464874171; JSESSIONID=8D5A3266F7A73C643C652F9F2DE1CED8; uc1=cookie14=UoWxNejwFlzlcw%3D%3D; l=Ahoatr-5ycJM6M9x2/4hzZdp6so-pZzm; mt=ci%3D-1_0'
        },
    }

    def start_requests(self):
        url = "https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8"
        for i in range(1, 20):
            formdata = {"q": "",
                        "viewFlag": "A",
                        "sortType": "default",
                        "searchStyle": "",
                        "searchRegion": "city:",
                        "searchFansNum": "",
                        "currentPage": str(i),
                        "pageSize": "100"}
            yield FormRequest(url, callback=self.parse_model, formdata=formdata)

    def parse_model(self, response):
        jsonBody = json.loads(response.body_as_unicode())
        models = jsonBody['data']['searchDOList']
        for dict in models:
            item = tbModelItem()
            item['city'] = dict['city']
            item['height'] = dict['height']
            item['realName'] = dict['realName']
            item['totalFavorNum'] = dict['totalFavorNum']
            item['userId'] = dict['userId']
            item['weight'] = dict['weight']
            yield Request('https://mm.taobao.com/self/aiShow.htm?spm=719.7763510.1998643336.1.IVVQk8&userId=%d' % item['userId'],
                          callback=self.parse_aixiu, meta={'item': item})

    def parse_aixiu(self, response):
        item = response.meta['item']
        item['image_urls'] = []
        # item['image_urls'] = response.xpath('//img/@src').extract()[1:-2]
        for img in response.xpath('//img')[1:-2]:
            image = img.xpath('@src').extract()[0]
            image = 'https:' + str(image)
            item['image_urls'].append(image)
        yield item
