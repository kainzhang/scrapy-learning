# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# useful for handling different item types with a single interface
import json
import time
from urllib.request import urlretrieve

from PIL import Image
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver import ActionChains
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

                flag = self.finish_captcha(spider.browser)
                if not flag:
                    print('-' * 20 + '登录失败，将开始匿名爬虫')
                    request.meta['useSelenium'] = False
                else:
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

    def get_img(self, driver):
        # 残缺图片地址
        src1 = driver.find_element_by_id('slideBg').get_attribute('src')
        print(src1)
        src0 = src1.replace('index=1', 'index=0')
        src0 = src0.replace('subsid=3', 'subsid=2')
        print(src0)

        now_str = str(int(round(time.time() * 1000)))
        img0_name = now_str + '-0.png'
        img1_name = now_str + '-1.png'
        urlretrieve(src0, 'douban/captcha_img/' + img0_name)
        urlretrieve(src1, 'douban/captcha_img/' + img1_name)
        time.sleep(3)
        img0 = Image.open('douban/captcha_img/' + img0_name)
        img1 = Image.open('douban/captcha_img/' + img1_name)
        """
        下载的图片尺寸：680 * 390
        验证码图片尺寸：340 * 195 
        """
        img0 = img0.resize((340, 195), Image.ANTIALIAS)
        img1 = img1.resize((340, 195), Image.ANTIALIAS)
        return img0, img1

    def pixel_equal(self, img0, img1, x, y):
        # 比较两张图片同一点上的像数值，差距大于设置标准返回False
        pixel0, pixel1 = img0.load()[x, y], img1.load()[x, y]
        sub_index = 100
        # 比较RGB各分量的值
        if abs(pixel0[0] - pixel1[0]) < sub_index and abs(pixel0[1] - pixel1[1]) < sub_index and abs(
                pixel0[2] - pixel1[2]) < sub_index:
            return True
        else:
            return False

    def get_distance(self, img0, img1):
        distance = 150
        for x in range(distance, img0.size[0]):
            for y in range(img0.size[1]):
                if not self.pixel_equal(img0, img1, x, y):
                    distance = x
                    return distance
        return distance

    def get_track(self, distance):
        print(f'distance= {distance}')
        t = 0.2
        v = 0
        distance -= 43
        tracks = []
        # 减速开始位置
        mid = 0.6 * distance
        s = 0
        while s < distance:
            v0 = v
            a = 30
            if s > mid:
                a = -3
            s0 = v0 * t + 0.5 * a * t * t  # 当前 t 时间的移动距离
            v = v0 + a * t  # 当前速度
            tracks.append((round(s0)))
            s += s0  # 当前位置
        return tracks

    def finish_captcha(self, driver):
        locator = (By.ID, 'tcaptcha_iframe')
        WebDriverWait(driver, 30).until((EC.presence_of_element_located(locator)))
        driver.switch_to.frame('tcaptcha_iframe')
        time.sleep(2)
        cnt = 0
        while True:
            locator = (By.ID, 'slideBg')
            WebDriverWait(driver, 30).until((EC.presence_of_element_located(locator)))

            img0, img1 = self.get_img(driver)
            distance = self.get_distance(img0, img1)
            tracks = self.get_track(distance)

            block = driver.find_element_by_id('tcaptcha_drag_button')

            ActionChains(driver).click_and_hold(block).perform()
            for track in tracks:
                ActionChains(driver).move_by_offset(track, 0).perform()
            ActionChains(driver).release().perform()
            time.sleep(2)

            if driver.title == "登录豆瓣":
                print('-' * 20 + '验证失败，再次尝试')
                if cnt == 5:
                    print('-' * 20 + '验证失败')
                    return False
                reload = driver.find_element_by_id('reload')
                reload.click()
                cnt += 1
            else:
                return True


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
