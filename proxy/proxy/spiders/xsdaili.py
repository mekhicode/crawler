# encoding: utf-8
import re
import chardet
import urlparse
import json
import redis

import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector

base_url = "http://www.xsdaili.com/"
redis_conn = redis.Redis()

class ProxySpider(scrapy.Spider):
    name = "xsdaili"
    MAX_PAGE = 1
    start_urls = [
        'http://www.xsdaili.com/mfdl?type=1',
        'http://www.xsdaili.com/mfdl?type=2',
        'http://www.xsdaili.com/mfdl?type=3',
        'http://www.xsdaili.com/mfdl?type=4',
    ]

    def parse(self, response):
        iChardet = response.encoding if hasattr(response, 'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet, "ignore")
        hxs = Selector(text=html, type="html")
        for i in hxs.xpath('//tbody/tr'):
            ip = i.xpath('td[1]/text()').extract_first()
            port = i.xpath('td[2]/text()').extract_first()
            proxy = "http://%s:%s" % (ip, port)
            print proxy
            print redis_conn.rpush('proxy', proxy)


        next_page = hxs.xpath('//a[@class="next"]/@href').extract_first()
        if next_page:
            next_page = urlparse.urljoin(base_url, next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        return

