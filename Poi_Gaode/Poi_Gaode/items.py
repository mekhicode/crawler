# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PoiGaodeItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    lng = Field()
    lat = Field()
    title = Field()
    province = Field()
    city = Field()
    area = Field()
    address = Field()
    phone = Field()
    class_ = Field()
    type_ = Field()
    data_result = Field()
