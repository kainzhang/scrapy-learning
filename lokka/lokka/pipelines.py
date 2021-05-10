# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

from pymongo import MongoClient
from lokka.items import LokkaItem

client = MongoClient()
collection = client['lokkame']['blog']


class LokkaPipeline:
    def process_item(self, item, spider):
        # 用 spider.name 判断
        # if spider.name == 'lokkame':
        #     collection.insert(dict(item))

        # 用 item 类判断
        if isinstance(item, LokkaItem):
            item['content'] = self.process_content(item['content'])
            print(item)
            collection.insert(dict(item))  # 插入数据库

        return item

    def process_content(self, content):
        content = [re.sub(r'\xa0|\s', ' ', i) for i in content]  # \xa0 替换为空格
        content = [i for i in content if len(i) > 0]  # 去除列表中的空字符串
        return content
