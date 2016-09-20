# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
import re
import chardet
import pymongo

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class DealerContentSpider(BaseSpider):
    conn = pymongo.MongoClient(host='192.168.33.10', port=27017)
    db = conn['Poi_China']
    poi = db["poi"]
    name = "diming"
    MAX_PAGE = 50
    start_urls = [
        "http://www.diming.org/e/tags/?tagname=%E5%9C%B0%E4%BA%A7%E5%B0%8F%E5%8C%BA",
    ]
    base_url = "http://www.diming.org"

    def parse(self, response):
        iChardet = response.encoding if hasattr(response,'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet,"ignore")
        hxs = Selector(text=html, type="html")
        nodes = hxs.xpath('//ol/li/a')
        for i in nodes:
            url = i.xpath('@href').extract()[0]
            yield Request(url=self.base_url+url, callback=self.parse_enter)
        next_page = hxs.xpath(u'//*[contains(text(),"下一页")]')
        if len(next_page.xpath('@href').extract()) > 0:
            next_url = next_page.xpath('@href').extract()[0]
            dealer_url = self.base_url + next_url
            yield Request(url=dealer_url, callback=self.parse)

    def parse_enter(self, response):
        hxs = Selector(text=response.body.decode(chardet.detect(response.body)['encoding'],"ignore"), type="html")
        name = hxs.xpath('//div[@class="slides"]/h2/text()').extract()[0]
        context = hxs.xpath('//div[@class="slides"]/p/text()').extract()[0]
        print name, context
        url = response.url
        nodes = hxs.xpath('//div[@class="slides"]/div/ul/li')
        data = []
        for i in nodes:
            data.append(i.xpath('text()').extract())
        self.poi.insert({"url": url, "name": name, "context": context, "data": data})
        return