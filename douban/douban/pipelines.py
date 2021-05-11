# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class DoubanPipeline:
    def open_spider(self, spider):
        client = MongoClient()
        if spider.name == 'movie':
            self.collection = client['douban']['movie']

    def process_item(self, item, spider):
        if spider.name == 'movie':
            self.collection.insert(dict(item))
            # print(item)

        return item
