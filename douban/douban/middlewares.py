# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# useful for handling different item types with a single interface
import json
import time

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# 使用 Selenium 实现手动豆瓣用户登录
class DoubanSeleniumMiddleware:
    def process_request(self, request, spider):
        # 判断是否需要使用 Selenium
        use_selenium = request.meta.get('useSelenium')
        if use_selenium:
            print('-' * 15 + '正在登录！')
            with open('douban/userinfo.json', mode='r', encoding='utf-8') as f:
                user = json.load(f)['douban']
            login_url = 'https://accounts.douban.com/passport/login'
            try:
                print('-' * 15 + request.url)
                spider.browser.get(login_url)
                locator = (By.CLASS_NAME, 'account-tab-account')
                WebDriverWait(spider.browser, 30).until(EC.presence_of_element_located(locator))
                spider.browser.find_element_by_class_name('account-tab-account').click()
                spider.browser.find_element_by_id('username').send_keys(user['username'])
                spider.browser.find_element_by_id('password').send_keys(user['password'])
                time.sleep(2)
                spider.browser.find_element_by_xpath('//a[contains(./text(), "登录豆瓣")]').click()

                locator = (By.CLASS_NAME, 'nav-user-account')
                WebDriverWait(spider.browser, 30).until((EC.presence_of_element_located(locator)))
                selenium_cookies = spider.browser.get_cookies()
                # print(f'[Selenium Cookies] = {selenium_cookies}')
            except Exception as e:
                print(e)
                return HtmlResponse(url=request.url, status=500, request=request)
            else:
                request.cookies = selenium_cookies
                request.meta['useSelenium'] = False

class DoubanSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
