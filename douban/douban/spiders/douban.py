# encoding: utf-8
import re
import chardet
import urlparse
import json
import copy

import scrapy
from scrapy.selector import Selector

base_url = "https://movie.douban.com/"

units = {
    'USD': '$',
    'GBP': '£',
    'CNY': '¥',
    'EUR': '€',
}

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    MAX_PAGE = 10
    start_urls = [
        "https://movie.douban.com/",
    ]

    def parse(self, response):
        # years = [1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
        years = [2012, 2013, 2014]

        for i in years:
            url = base_url + "tag/" + str(i)
            yield scrapy.Request(url, callback=self.listing_parse)

    def listing_parse(self, response):
        iChardet = response.encoding if hasattr(response, 'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet,"ignore")
        hxs = Selector(text=html, type="html")
        for i in hxs.xpath('//tr[@class="item"]'):
            url = i.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url, callback=self.detail_parse)

        next_url = hxs.xpath('//link[@rel="next"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(next_url, callback=self.listing_parse)

    def detail_parse(self, response):
        iChardet = response.encoding if hasattr(response, 'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet,"ignore")
        hxs = Selector(text=html, type="html")
        title = hxs.xpath('//h1/span[@property]/text()').extract_first()
        print title
        info = hxs.xpath('//div[@id="info"]')
        info = info.xpath('string(.)').extract()
        for i in info:
            print i
        rating_num = hxs.xpath('//strong[@class="ll rating_num"]/text()').extract_first()  # 评分
        votes = hxs.xpath('//span[@property="v:votes"]/text()').extract_first()  # 多少人评价
        rating_per = hxs.xpath('//span[@class="rating_per"]/text()').extract()  # 评分占比
        summary = '\n'.join(hxs.xpath('//span[@property="v:summary"]/text()').extract())  # 简介
        detail_image = hxs.xpath('//img[@rel="v:image"]/@src').extract_first()  # 海报缩略图
        print rating_num
        print votes
        print rating_per
        print summary
        print detail_image
        print "="*30



# 平衡