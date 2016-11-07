# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from lagou.items import LagouItem

class ZhaopinSpider(Spider):
    name = "zhaopin"
    allowed_domains = ["lagou.com"]
    start_urls = (
        'http://www.lagou.com/zhaopin/Python',
        'http://www.lagou.com/zhaopin/shujuwajue',
    )
    download_delay = 0.5
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Host': 'www.lagou.com',
        }
    }

    def parse(self, response):
        totalpage = response.xpath('//div[@class="pager_container"]/a[last()-1]/text()').extract()
        totalpage = ''.join(totalpage)
        for page in range(1, int(totalpage) + 1):
            url = response.urljoin(str(page))
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        for sel in response.xpath('//a[@class="position_link"]/@href').extract():
            url = 'http:' + sel
            yield Request(url, callback=self.parse_co)

    def parse_co(self, response):
        item = LagouItem()
        sel = response.xpath('//dl[@class="job_detail"]')
        item['title'] = sel.xpath('dt/h1/text()').extract()
        item['job_request'] = sel.xpath('dd[@class="job_request"]/p/span/text()').extract()
        item['addr'] = response.xpath('//div[@class="work_addr"]/text()').extract()
        item['job_bt3'] = sel.xpath('dd[@class="job_bt"]/*/*/*/text()').extract()
        item['job_bt2'] = sel.xpath('dd[@class="job_bt"]/*/*/text()').extract()
        item['job_bt1'] = sel.xpath('dd[@class="job_bt"]/*/text()').extract()
        yield item