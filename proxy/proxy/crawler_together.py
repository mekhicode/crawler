from scrapy import signals
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
crawler = CrawlerProcess(settings)
# print crawler.spiders.list()
for i in crawler.spiders.list():
    # print i
    crawler.crawl(i)
    crawler.start()