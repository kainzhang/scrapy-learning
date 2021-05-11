# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    name = scrapy.Field()
    date_published = scrapy.Field()
    genre = scrapy.Field()
    duration = scrapy.Field()
    rating_value = scrapy.Field()
    director = scrapy.Field()
    author = scrapy.Field()
    actor = scrapy.Field()
    description = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()

    region = scrapy.Field()
    language = scrapy.Field()
    alias = scrapy.Field()


class BookItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    isbn = scrapy.Field()

    # 评分
    rating_value = scrapy.Field()

    # 封面图片
    image = scrapy.Field()
    # 出版社
    press = scrapy.Field()
    # 出品方
    producer = scrapy.Field()
    # 副标题
    subtitle = scrapy.Field()
    # 原作名
    original_title = scrapy.Field()
    # 译者
    translator = scrapy.Field()
    # 出版日期
    pub_date = scrapy.Field()
    # 页数
    paginal_num = scrapy.Field()
    # 定价
    price = scrapy.Field()
    # 装帧
    binding = scrapy.Field()
    # 丛书
    series = scrapy.Field()

