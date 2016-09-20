# encoding: utf-8
import re
import chardet
import urlparse
import requests
import json
import copy

import scrapy
from scrapy.selector import Selector

base_url = "https://www.zhihu.com/"

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    MAX_PAGE = 10
    start_urls = [
        "https://www.zhihu.com",
    ]

    def parse(self, response):
        import requests
        s = requests.Session()
        data = {'password': 'xxx', 'email': 'xxx', 'captcha_type': 'cn', 'remember_me': True}
        s.post("https://www.zhihu.com/login/email", data=data,
                   headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                            "Referer": "https://www.zhihu.com", "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"})
        cookies = dict()
        for i in s.cookies:
            cookies[i.name] = i.value
        yield scrapy.Request("https://www.zhihu.com/people/mekhi-t/followees",
                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                                          "Referer": "https://www.zhihu.com", "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                                          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                                 callback=self.listing_parse, cookies=cookies)


    def listing_parse(self, response):
        msgs = response.body['msg']
        if msgs:
            for msg in msgs:
                hxs = Selector(text=msg, type="html")
                print "浏览:", hxs.xpath('//div[@class="zm-profile-vote-num"]/text()').extract_first()
                print "问题:", hxs.xpath('//a[class="question_link"]/text()').extract_first()
                for i in hxs.xpath('//div[@class="meta zg-gray"]/text').extract():
                    print i


        offset = int(response.meta['offset']) + 20
        yield scrapy.FormRequest("https://www.zhihu.com/node/ProfileFollowedQuestionsV2",
                                 formdata={'method': 'next', 'params': {"offset": 60}},
                                 callback=self.listing_parse, meta={'offset': offset})

    def detail_parse(self, response):
        iChardet = response.encoding if hasattr(response, 'encoding') else chardet.detect(response.body)['encoding']
        html = response.body.decode(iChardet,"ignore")
        hxs = Selector(text=html, type="html")
        title = hxs.xpath('//h1/span[@property]/text()').extract_first()
        print title