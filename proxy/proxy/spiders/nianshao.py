# encoding: utf-8
import re
import chardet
import urlparse
import json
import redis

import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector

base_url = "http://www.nianshao.me/"
redis_conn = redis.Redis()

class ProxySpider(scrapy.Spider):
    name = "nianshao"
    MAX_PAGE = 1
    start_urls = [
        'http://www.nianshao.me/?page=1',
    ]

    def parse(self, response):
        iChardet = response.encoding if hasattr(response, 'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet, "ignore")
        hxs = Selector(text=html, type="html")
        for i in hxs.xpath('//tr'):
            ip = i.xpath('td[@style="WIDTH:110PX"]/text()').extract_first()
            port = i.xpath('td[@style="WIDTH:40PX"]/text()').extract_first()
            proxy = "http://%s:%s" % (ip, port)
            print proxy
            print redis_conn.rpush('proxy', proxy)


        next_page = int(re.compile('(\d+)').findall(response.url)[0])
        if next_page < 500:
            next_url = response.url.split('?')[0] + '?page=' + str(next_page)
            yield scrapy.Request(next_url, callback=self.parse)

        return

