# encoding: utf-8
import re
import chardet
import urlparse
import json
import redis

import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector

base_url = "http://ip84.me/"
redis_conn = redis.Redis()

class ProxySpider(scrapy.Spider):
    name = "ip84"
    MAX_PAGE = 1
    start_urls = [
        'http://ip84.com/gn',
        'http://ip84.com/pn',
        'http://ip84.com/tm',
    ]

    def parse(self, response):
        iChardet = response.encoding if hasattr(response, 'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet, "ignore")
        hxs = Selector(text=html, type="html")
        for i in hxs.xpath('//table[@class="list"]/tr'):
            ip = i.xpath('td[1]/text()').extract_first()
            port = i.xpath('td[2]/text()').extract_first()
            proxy = "http://%s:%s" % (ip, port)
            print proxy
            print redis_conn.rpush('proxy', proxy)


        next_page = hxs.xpath('//a[@class="next_page"]/@href').extract_first()
        if next_page:
            next_page = urlparse.urljoin(base_url, next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        return

