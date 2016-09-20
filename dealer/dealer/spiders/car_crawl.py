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
    name = "che"
    MAX_PAGE = 50
    start_urls = [
        "http://www.che168.com/Handler/ScriptCarList_V1.ashx?needData=1",
    ]

    def parse(self, response):
        iChardet = response.encoding if hasattr(response,'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet,"ignore")
        # hxs = Selector(text=html, type="html")
        data = html[31:-2].split(',')
        datas = {}
        index = 0
        for i in range(len(data) / 2):
            key_ = data[index]
            index += 1
            datas[key_] = data[index]
            index += 1

        for k,v in datas.items():
            url = 'http://i.che168.com/Handler/SaleCar/ScriptCarList_V1.ashx?seriesGroupType=2&needData=2&bid=' + k
            yield Request(url=url, callback=self.parse_enter, meta={'name':v})

    def parse_enter(self, response):
        iChardet = response.encoding if hasattr(response,'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet,"ignore")
        data = re.compile('=\'(.*)').findall(html)[0].split(',')
        datas = {}
        index = 0
        for i in range(len(data) / 2):
            print response.meta['name']
            key_ = data[index]
            index += 1
            datas[key_] = data[index]
            index += 1

        for k,v in datas.items():
            url = 'http://i.che168.com/Handler/SaleCar/ScriptCarList_V1.ashx?seriesGroupType=2&needData=3&seriesid=' + k
            yield Request(url=url, callback=self.parse_detail, meta={'name':v})

    def parse_detail(self, response):
        iChardet = response.encoding if hasattr(response,'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet,"ignore")
        print response.meta['name']
        print html