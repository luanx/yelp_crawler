# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback

from pymongo import MongoClient


class YelpPipeline(object):

    def __init__(self):
        try:
            client = MongoClient(self.MONGODB_SERVER,self.MONGODB_PORT)
            self.db = client[self.MONGODB_DB]
        except Exception as e:
            print self.style.ERROR("ERROR(YelpPipeline): %s"%(str(e),))
            traceback.print_exc()

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('SingleMONGODB_SERVER', 'localhost')
        cls.MONGODB_PORT = crawler.settings.getint('SingleMONGODB_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('SingleMONGODB_DB', 'yelp')
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
        result = self.db['yelp'].insert(item)
        item['_id'] = str(result)
        return item
