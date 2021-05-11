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
        elif spider.name == 'book':
            self.collection = client['douban']['book']

    def process_item(self, item, spider):
        if spider.name == 'movie':
            self.collection.insert(dict(item))
            # print(item)

        if spider.name == 'book':
            for key in item:
                if isinstance(item[key], str) and item[key] == '':
                    item[key] = None
                elif isinstance(item[key], list):
                    item[key] = [i for i in item[key] if i != '']
            self.collection.insert(dict(item))
            # print(item)

        return item

