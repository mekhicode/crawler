__author__ = 'mekhitang'
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
import re
import chardet
from scrapy.selector import Selector
from scrapy.http import Request
from Poi_Gaode.items import PoiGaodeItem
import pymongo


class PoiSpider(BaseSpider):
    name = "gaode"
    MAX_PAGE = 50
    start_urls = [
        "http://www.poi86.com/poi/amap.html"
    ]
    base_url = "http://www.poi86.com"
    conn = pymongo.Connection(host='127.0.0.1', port=27017)
    db = conn['Poi_China']
    poi = db["poi"]

    def parse(self, response):
        hxs = Selector(text=response.body.decode(chardet.detect(response.body)['encoding'], "ignore"), type="html")
        nodes = hxs.xpath('//div[@class="col-md-2"]/a')
        print "========start============"
        for node in nodes:
            dealer_url = node.xpath('@href').extract()
            if dealer_url is not None:
                dealer_url = self.base_url + dealer_url[0]
                yield Request(url=dealer_url, callback=self.parse_enter)

    def parse_enter(self, response):
        hxs = Selector(text=response.body.decode(chardet.detect(response.body)['encoding'],"ignore"), type="html")
        nodes = hxs.xpath('//ul[@class="list-group"]/li')
        for node in nodes:
            dealer_url = self.base_url + node.xpath('a/@href').extract()[0]
            yield Request(url=dealer_url, callback=self.parse_city)

    def parse_city(self, response):
        hxs = Selector(text=response.body.decode(chardet.detect(response.body)['encoding'],"ignore"), type="html")
        nodes = hxs.xpath('//ul[@class="list-group"]/li')
        for node in nodes:
            dealer_url = self.base_url + node.xpath('a/@href').extract()[0]
            yield Request(url=dealer_url, callback=self.parse_area)

    def parse_area(self, response):
        hxs = Selector(text=response.body.decode(chardet.detect(response.body)['encoding'],"ignore"), type="html")
        nodes = hxs.xpath('//table/tr/td/a')
        for node in nodes:
            points = node.xpath('@href').extract()[0]
            dealer_url = self.base_url + points
            yield Request(url=dealer_url, callback=self.parse_point)
        next_page = hxs.xpath(u'//*[contains(text(),"下一页")]/..')
        if len(next_page.xpath('@class').extract()) < 1:
            next_url = next_page.xpath('a/@href').extract()[0]
            dealer_url = self.base_url + next_url
            yield Request(url=dealer_url, callback=self.parse_area)



    def parse_point(self, response):
        hxs = Selector(text=response.body.decode(chardet.detect(response.body)['encoding'],"ignore"), type="html")
        js_code = hxs.xpath(u'//text()[contains(.,"var lng = ")]').extract()[0]
        lng = re.compile('var lng = (.*);').findall(js_code)[0]
        lat = re.compile('var lat = (.*);').findall(js_code)[0]
        title = hxs.xpath(u'//h1/text()').extract()[0]
        nodes = hxs.xpath(u'//ul[@class="list-group"]/li')
        iList = []
        for node in nodes:
            i = node.xpath('text() | a/text()').extract()
            if len(i) > 1:
                iList.append(i[1].strip())
            else:
                iList.append(i[0].strip())
        item = PoiGaodeItem()
        data = {
            'lng': lng,
            'lat': lat,
            'title': title,
            'province': iList[0],
            'city': iList[1],
            'area': iList[2],
            'address': iList[3],
            'phone': iList[4],
            'class_': iList[5]
        }
        item['data_result'] = data
        return item
        #self.insert_mongo(data)

    def insert_mongo(self, data):
        self.poi.insert(data)