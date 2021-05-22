import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main():
    PAGE_TIMEOUT = 30
    WINDOW_WIDTH = 960
    WINDOW_HEIGHT = 720

    with open('douban_user.json', mode='r', encoding='utf-8') as f:
        data = json.load(f)
    user = data['user1']

    request_url = 'https://accounts.douban.com/passport/login'
    browser = webdriver.Chrome()
    browser.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    browser.set_page_load_timeout(PAGE_TIMEOUT)

    try:
        browser.get(request_url)
        locator = (By.CLASS_NAME, 'account-tab-account')
        WebDriverWait(browser, PAGE_TIMEOUT).until(EC.presence_of_element_located(locator))
        browser.find_element_by_class_name('account-tab-account').click()
        browser.find_element_by_id('username').send_keys(user['username'])
        browser.find_element_by_id('password').send_keys(user['password'])
        time.sleep(2)
        browser.find_element_by_xpath('//a[contains(./text(), "登录豆瓣")]').click()

        locator = (By.CLASS_NAME, 'nav-user-account')
        WebDriverWait(browser, PAGE_TIMEOUT).until((EC.presence_of_element_located(locator)))
        selenium_cookies = browser.get_cookies()
        print(f'Selenium Cookies = {selenium_cookies}')

    except Exception as e:
        print(f'Exception = {e}')

    # cookie = [item["name"] + ":" + item["value"] for item in selenium_cookies]
    # processed_cookie = {}
    # for elem in cookie:
    #     tmp_str = elem.split(':')
    #     processed_cookie[tmp_str[0]] = tmp_str[1]
    # print(f'Processed Cookies = {processed_cookie}')

    finally:
        browser.close()

if __name__ == '__main__':
    main()
