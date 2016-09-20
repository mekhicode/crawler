# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class PoiGaodePipeline(object):
    conn = pymongo.Connection(host='127.0.0.1', port=27017)

    def process_item(self, item, spider):
        '''
        data = {
            'lng': item['lng'],
            'lat': item['lat'],
            'title': item['title'],
            'province': item['province'],
            'city': item['city'],
            'area': item['area'],
            'address': item['address'],
            'phone': item['phone'],
            'class_': item['class_'],
            'type_': item['type_']
        }'''
        data = item['data_result']

        db = self.conn['Poi_China']
        poi = db["poi"]
        poi.insert(data)
        return item
