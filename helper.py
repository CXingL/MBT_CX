# -*- coding: utf-8 -*-
from time import sleep
import random
import string
import json
from faker import Faker
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *


class Public(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30)
        self.faker = Faker()
        self.faker_jp = Faker('ja_JP')
        self.faker_us = Faker('en_US')
        self.faker_cn = Faker('zh_CN')

    @staticmethod
    def randomString(count, base=True):
        """
            生成一个指定长度的随机字符串，base 控制是否有符号
        """
        if base:
            return ''.join(random.choices(string.ascii_letters + string.digits, k=count))
        else:
            return ''.join(random.choices(string.ascii_letters + string.digits + string.whitespace + string.punctuation,
                                          k=count))

    @staticmethod
    def saveTestData(var, value):
        """
        保存数据至 test_data 文件中,格式为 json
        """
        try:
            with open("test_data.json", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        data[var] = value
        with open("test_data.json", 'w') as f:
            json.dump(data, f, indent=4)
        sleep(1)

    @staticmethod
    def getTestData(var):
        """
        从 test_data 文件中读取数据，并验证是否一致
        """
        with open('test_data.json', 'r') as f:
            data = json.load(f)
        return data[var]


class Android(Public):
    def __int__(self, driver):
        Public.__init__(self, driver)

    def swipeAndClick(self, ele, down=True):
        """
        滑动屏幕并点击某一元素，默认向下滑动, down 为 false 时向上滑动
        """
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        i = 0
        while i < 8:
            try:
                self.driver.find_element_by_id(ele).click()
                break
            except NoSuchElementException:
                if down:
                    self.driver.swipe(width / 2, height * 0.8, width / 2, height * 0.2)
                else:
                    self.driver.swipe(width / 2, height * 0.2, width / 2, height * 0.8)
                i += 1
                sleep(1)


class Ios(Public):
    def __int__(self, driver):
        Public.__init__(self, driver)

    def swipeAndClick(self, ele, down=True):
        """
        滑动屏幕并点击某一元素，默认向下滑动, down 为 false 时向上滑动
        """
        i = 0
        while i < 4:
            if self.driver.find_element_by_ios_predicate(ele).is_displayed():
                self.driver.find_element_by_ios_predicate(ele).click()
                break
            else:
                if down:
                    self.driver.execute_script("mobile: scroll", {"direction": "down"})
                else:
                    self.driver.execute_script("mobile: scroll", {"direction": "up"})
                i += 1
                sleep(2)


class Web(Public):
    def __int__(self, driver):
        Public.__init__(self, driver)

    def closeNewWindow(self):
        """
        # 关闭新打开的标签页
        # 获取当前窗口和所有窗口的句柄
        """
        sleep(1)
        handle = self.driver.current_window_handle
        handles = self.driver.window_handles
        # 对窗口进行遍历，并关闭新窗口
        for newhandle in handles:
            if newhandle != handle:
                self.driver.switch_to_window(newhandle)
                self.driver.close()
                self.driver.switch_to_window(handle)
        sleep(0.6)
