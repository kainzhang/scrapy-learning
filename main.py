from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':
    driver = webdriver.Chrome('/Users/kainzhang/PycharmProjects/chromedriver')
    driver.set_window_size(1400, 800)
    driver.get("https://www.baidu.com")
    key_str = "diablo"
    elem = driver.find_element_by_xpath('.//input[@id="kw"]')
    elem.send_keys(key_str)
    elem = driver.find_element_by_xpath('.//input[@id="su"]')
    elem.send_keys(Keys.ENTER)