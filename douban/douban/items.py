# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


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
