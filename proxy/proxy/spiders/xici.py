# encoding: utf-8
import re
import chardet
import urlparse
import json
import redis

import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector

base_url = "http://www.xicidaili.com"
redis_conn = redis.Redis()

class ProxySpider(scrapy.Spider):
    name = "xici"
    MAX_PAGE = 1
    start_urls = [
        'http://www.xicidaili.com/wn/',
        'http://www.xicidaili.com/nn/',
    ]

    def parse(self, response):
        iChardet = response.encoding if hasattr(response, 'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet, "ignore")
        hxs = Selector(text=html, type="html")
        for i in hxs.xpath('//table[@id="ip_list"]/tr[@class]'):
            ip = i.xpath('td[3]/text()').extract_first()
            port = i.xpath('td[4]/text()').extract_first()
            times = hxs.xpath('td[8]/div/@title').extract_first()
            if float(re.compile('(\d+.\d+)').findall(times.replace(',', ''))[0]) < 3:
                proxy = "http://%s:%s" % (ip, port)
                print proxy
                print redis_conn.rpush('proxy', proxy)

        next_page = hxs.xpath('//a[@class="next_page"]/@href').extract_first()
        if next_page:
            next_page = urlparse.urljoin(base_url, next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        return

