import json

import scrapy
from douban.items import MovieItem


# 豆瓣电影 TOP250 爬虫
class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # 获取当前页面电影列表
        li_list = response.xpath('//div[@class="article"]//li')
        for li in li_list:
            li_href = li.xpath('.//div[@class="hd"]//a/@href').extract_first()
            if li_href is not None:
                yield scrapy.Request(
                    li_href,
                    callback=self.parse_info
                )

        # 进入下一页
        nxt_href = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if nxt_href is not None:
            yield scrapy.Request(
                'https://movie.douban.com/top250' + nxt_href,
                callback=self.parse
            )

    # 获取电影详细信息
    def parse_info(self, response):
        item = MovieItem()
        data = json.loads(
            response.xpath('//script[@type="application/ld+json"]//text()').extract_first(),
            strict=False
        )
        item['name'] = data['name']
        item['image'] = data['image']
        item['url'] = 'https://movie.douban.com' + data['url']
        item['date_published'] = data['datePublished']
        item['genre'] = data['genre']
        item['duration'] = data['duration']
        item['rating_value'] = data['aggregateRating']['ratingValue']
        item['description'] = data['description']
        item['director'] = [d['name'] for d in data['director']]
        item['author'] = [a['name'] for a in data['author']]
        item['actor'] = [a['name'] for a in data['actor']]
        yield item
