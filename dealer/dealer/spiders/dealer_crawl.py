# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
import re
import chardet

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class DealerFESpider(BaseSpider):
    name = "fe"
    MAX_PAGE = 50
    start_urls = [
        "http://dealer.autohome.com.cn/",
    ]
    base_url = "http://dealer.autohome.com.cn"

    def parse(self, response):
        iChardet = response.encoding if hasattr(response,'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet,"ignore")
        hxs = Selector(text=html, type="html")
        nodes = hxs.xpath('//ul[@class="cityfilter-list"]/li[@id]/dl')
        for i in nodes:
            try:
                province = i.xpath('dt/a/text()').extract()[0]
                # print province
                for i in i.xpath('dd/a'):
                    url = i.xpath('@href').extract()[0]
                    city = i.xpath('text()').extract()[0]
                    # print city
                    data = {
                        'province': province,
                        'city': city
                    }
                    yield Request(url=self.base_url+url, callback=self.parse_enter)
            except:
                pass

        # yield Request(url=dealer_url, callback=self.parse)

    def parse_enter(self, response):
        hxs = Selector(text=response.body.decode(chardet.detect(response.body)['encoding'],"ignore"), type="html")
        nodes = hxs.xpath('//div[@class="list-ul-text js-search-area"]/a')
        for node in nodes:
            try:
                area = node.xpath('text()').extract()[0]
                if area != u"全部":
                    data = {}
                    area_id = node.xpath('@data-value').extract()[0]
                    data['area_id'] = area_id
                    url = node.xpath('@href').extract()[0]
                    yield Request(url=self.base_url+url, callback=self.parse_detail, meta=data)
            except:
                pass

    def parse_detail(self, response):
        hxs = Selector(text=response.body.decode(chardet.detect(response.body)['encoding'],"ignore"), type="html")
        nodes = hxs.xpath('//div[@class="dealer-cont  "]/div')
        data = {
            'area_id': response.meta['area_id'],
        }
        for node in nodes:
            data['name'] = node.xpath('h3/a/@js-dname').extract()[0]
            data['car_type'] = node.xpath('h3/a/@js-dbrand').extract()[0]
            data['dealer_id'] = node.xpath('h3/a/@js-did').extract()[0]
            data['address'] = node.xpath('dl/dd/div[@title]/@title').extract()[1]
            for k,v in data.items():
                print k, v
        next_page = hxs.xpath(u'//*[contains(text(),"下一页")]')
        print next_page.xpath('@href').extract()[0]
        if next_page.xpath('@href').extract()[0] != 'javascript:void(0);':
            next_url = next_page.xpath('@href').extract()[0]
            dealer_url = self.base_url + next_url
            yield Request(url=dealer_url, callback=self.parse_detail)