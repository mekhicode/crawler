# -*- coding: utf-8 -*-

# Scrapy settings for Poi_Gaode project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Poi_Gaode'

SPIDER_MODULES = ['Poi_Gaode.spiders']
NEWSPIDER_MODULE = 'Poi_Gaode.spiders'
DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 30

ITEM_PIPELINES = ['Poi_Gaode.pipelines.PoiGaodePipeline']
CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS_PER_SPIDER = 64
CONCURRENT_SPIDERS = 128

RANDOMIZE_DOWNLOAD_DELAY = True
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Poi_Gaode (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'Poi_Gaode.middlewares.ProxyMiddleware': 100,
    }

RETRY_ENABLED = True
RETRY_TIMES = 2 # initial response + 2 retries = 3 requests
RETRY_HTTP_CODES = [500, 503, 504, 400, 404, 408]
RETRY_PRIORITY_ADJUST = -1

CONCURRENT_REQUESTS = 5
COOKIES_ENABLED = False