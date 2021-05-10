import logging
import scrapy
from lokka.items import LokkaItem  # ignore it, pycharm is sb

logger = logging.getLogger(__name__)


class LokkameSpider(scrapy.Spider):
    name = 'lokkame'
    allowed_domains = ['lokka.me']
    start_urls = ['https://lokka.me/archives/']

    def parse(self, response):
        # 处理start_url地址对应的响应
        li_list = response.xpath('//div[@class="columns"]/div[1]//article/div/div')
        for li in li_list:
            item = LokkaItem()
            item['title'] = li.xpath("./a/text()").extract_first()
            item['category_1'] = li.xpath("./div//a[1]/text()").extract_first()
            item['category_2'] = li.xpath("./div//a[2]/text()").extract_first()
            item['publish_date'] = li.xpath("./time/@datetime").extract_first()
            item['href'] = 'https://lokka.me' + li.xpath("./a/@href").extract_first()
            yield scrapy.Request(
                item['href'],
                callback=self.parse_detail,
                meta={'item': item}
            )

        # 进入下一页
        nxt_btn = response.xpath('//div[contains(@class, "pagination-next") '
                                 'and not(contains(@class, "is-invisible"))]')
        nxt_url = nxt_btn.xpath('./a/@href').extract_first()
        if nxt_url is not None:
            yield scrapy.Request(
                'https://lokka.me' + nxt_url,
                callback=self.parse,
            )

    # 获取详情页内容
    def parse_detail(self, response):
        item = response.meta['item']
        item['content'] = response.xpath('//div[@class="content"]//p/text()').extract()
        yield item
