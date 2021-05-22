# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    date_published = scrapy.Field()
    genre = scrapy.Field()
    duration = scrapy.Field()
    director = scrapy.Field()
    author = scrapy.Field()
    actor = scrapy.Field()
    description = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    imdb = scrapy.Field()

    rating_value = scrapy.Field()
    stars5 = scrapy.Field()
    stars4 = scrapy.Field()
    stars3 = scrapy.Field()
    stars2 = scrapy.Field()
    stars1 = scrapy.Field()

    region = scrapy.Field()
    language = scrapy.Field()
    alias = scrapy.Field()


class BookItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    isbn = scrapy.Field()

    # 评分
    rating_value = scrapy.Field()
    stars5 = scrapy.Field()
    stars4 = scrapy.Field()
    stars3 = scrapy.Field()
    stars2 = scrapy.Field()
    stars1 = scrapy.Field()

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


class CommentItem(scrapy.Item):
    id = scrapy.Field()

    # 评论类型：电影评论，图书评论
    comment_type = scrapy.Field()
    # 所属对象的id：电影id，图书id
    dad_id = scrapy.Field()
    author = scrapy.Field()
    author_url = scrapy.Field()
    rating_val = scrapy.Field()
    pub_date = scrapy.Field()
    content = scrapy.Field()

