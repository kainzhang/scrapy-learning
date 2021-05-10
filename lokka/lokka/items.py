# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LokkaItem(scrapy.Item):
    title = scrapy.Field()
    category_1 = scrapy.Field()
    category_2 = scrapy.Field()
    publish_date = scrapy.Field()
    content = scrapy.Field()
    href = scrapy.Field()