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
        self.dbs = client['douban']

    def process_item(self, item, spider):
        if spider.name == 'movie':
            self.dbs['movie'].insert(dict(item))

        return item
