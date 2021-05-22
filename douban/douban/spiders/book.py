import json
import re

import scrapy
from douban.items import BookItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['book.douban.com']
    start_urls = ['http://book.douban.com/top250']

    def parse(self, response):
        # 获取当前页面图书列表
        tab_list = response.xpath('//div[@class="article"]//table')
        for tab in tab_list:
            tab_href = tab.xpath('.//div[@class="pl2"]/a/@href').extract_first()
            if tab_href is not None:
                yield scrapy.Request(
                    tab_href,
                    callback=self.parse_info
                )

        # 进入下一页
        nxt_href = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if nxt_href is not None:
            yield scrapy.Request(
                nxt_href,
                callback=self.parse
            )

        # 单条测试
        # yield scrapy.Request(
        #     'https://book.douban.com/subject/6082808/',
        #     self.parse_info
        # )

    def parse_info(self, response):
        item = BookItem()
        data = json.loads(
            response.xpath('//script[@type="application/ld+json"]//text()').extract_first(),
            strict=False
        )
        item['id'] = re.sub(r'\D', "", data['url'])
        item['name'] = data['name']
        item['author'] = [a['name'] for a in data['author']]
        item['url'] = data['url']
        item['isbn'] = data['isbn']

        # Json 中没有的信息
        # 评分
        item['rating_value'] = response.xpath(
            'normalize-space(//strong[@class="ll rating_num "]/text())'
        ).extract_first()
        item['stars5'] = response.xpath('//span[@class="stars5 starstop"]/following::span/text()').extract_first()
        item['stars4'] = response.xpath('//span[@class="stars4 starstop"]/following::span/text()').extract_first()
        item['stars3'] = response.xpath('//span[@class="stars3 starstop"]/following::span/text()').extract_first()
        item['stars2'] = response.xpath('//span[@class="stars2 starstop"]/following::span/text()').extract_first()
        item['stars1'] = response.xpath('//span[@class="stars1 starstop"]/following::span/text()').extract_first()

        # 封面图片
        item['image'] = response.xpath(
            '//a[@class="nbg"]/@href'
        ).extract_first()

        data_aug = response.xpath('//div[@id="info"]')
        # 出版社
        item['press'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "出版社:")]/following::text()[1])'
        ).extract_first()
        # 出品方
        item['producer'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "出品方:")]/following::a/text())'
        ).extract_first()
        # 副标题
        item['subtitle'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "副标题:")]/following::text()[1])'
        ).extract_first()
        # 原作名
        item['original_title'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "原作名:")]/following::text()[1])'
        ).extract_first()

        # 译者 type1
        tmp_translator = data_aug.xpath(
            './/span[contains(./text(), " 译者")]/following-sibling::a/text()'
        ).extract()
        if len(tmp_translator) == 0:
            # 译者 type2
            tmp_translator = data_aug.xpath(
                'normalize-space(.//span[contains(./text(), "译者:")]/following::a/text())'
            ).extract()
        item['translator'] = tmp_translator

        # 出版日期
        item['pub_date'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "出版年:")]/following::text()[1])'
        ).extract_first()
        # 页数
        item['paginal_num'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "页数:")]/following::text()[1])'
        ).extract_first()
        # 定价
        item['price'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "定价:")]/following::text()[1])'
        ).extract_first()
        # 装帧
        item['binding'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "装帧:")]/following::text())'
        ).extract_first()
        # 丛书
        item['series'] = data_aug.xpath(
            './span[contains(./text(), "丛书:")]/following::a/text()'
        ).extract_first()

        yield item
