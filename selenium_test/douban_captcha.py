import json
import time
from urllib.request import urlretrieve

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_img(driver):
    # 残缺图片地址
    src1 = driver.find_element_by_id('slideBg').get_attribute('src')
    print(src1)
    src0 = src1.replace('index=1', 'index=0')
    src0 = src0.replace('subsid=3', 'subsid=2')
    print(src0)

    now_str = str(int(round(time.time() * 1000)))
    img0_name = now_str + '-0.png'
    img1_name = now_str + '-1.png'
    urlretrieve(src0, './captcha_img/' + img0_name)
    urlretrieve(src1, './captcha_img/' + img1_name)
    time.sleep(3)
    img0 = Image.open('./captcha_img/' + img0_name)
    img1 = Image.open('./captcha_img/' + img1_name)
    """
    下载的图片尺寸：680 * 390
    验证码图片尺寸：340 * 195 
    """
    img0 = img0.resize((340, 195), Image.ANTIALIAS)
    img1 = img1.resize((340, 195), Image.ANTIALIAS)
    return img0, img1


def pixel_equal(img0, img1, x, y):
    # 比较两张图片同一点上的像数值，差距大于设置标准返回False
    pixel0, pixel1 = img0.load()[x, y], img1.load()[x, y]
    sub_index = 100
    # 比较RGB各分量的值
    if abs(pixel0[0] - pixel1[0]) < sub_index and abs(pixel0[1] - pixel1[1]) < sub_index and abs(
            pixel0[2] - pixel1[2]) < sub_index:
        return True
    else:
        return False


def get_distance(img0, img1):
    distance = 150
    for x in range(distance, img0.size[0]):
        for y in range(img0.size[1]):
            if not pixel_equal(img0, img1, x, y):
                distance = x
                return distance
    return distance


def get_track(distance):
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


def finish_captcha(driver):
    locator = (By.ID, 'tcaptcha_iframe')
    WebDriverWait(driver, 30).until((EC.presence_of_element_located(locator)))
    driver.switch_to.frame('tcaptcha_iframe')
    time.sleep(2)

    while True:
        locator = (By.ID, 'slideBg')
        WebDriverWait(driver, 30).until((EC.presence_of_element_located(locator)))

        img0, img1 = get_img(driver)
        distance = get_distance(img0, img1)
        tracks = get_track(distance)

        block = driver.find_element_by_id('tcaptcha_drag_button')

        ActionChains(driver).click_and_hold(block).perform()
        for track in tracks:
            ActionChains(driver).move_by_offset(track, 0).perform()
        ActionChains(driver).release().perform()
        time.sleep(2)

        if driver.title == "登录豆瓣":
            print('failed, try once again')
            reload = driver.find_element_by_id('reload')
            reload.click()
        else:
            break


def main():
    with open('douban_user.json', mode='r', encoding='utf-8') as f:
        data = json.load(f)
    user = data['user1']

    login_url = 'https://accounts.douban.com/passport/login'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(login_url)

    locator = (By.CLASS_NAME, 'account-tab-account')
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator))
    driver.find_element_by_class_name('account-tab-account').click()
    driver.find_element_by_id('username').send_keys(user['username'])
    driver.find_element_by_id('password').send_keys(user['password'])
    time.sleep(1)
    driver.find_element_by_xpath('//a[contains(./text(), "登录豆瓣")]').click()

    finish_captcha(driver)


if __name__ == '__main__':
    main()
