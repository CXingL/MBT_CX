import helper
import random
from time import sleep


class Action(helper.Web):
    def __init__(self, driver):
        helper.Web.__init__(self, driver)

    def e_getUrl(self):
        self.driver.get('https://www.baidu.com/')

    def e_inputChinese(self):
        self.driver.find_element_by_xpath('//*[@id="kw"]').clear()
        self.driver.find_element_by_xpath('//*[@id="kw"]').send_keys("基于模型的测试")

    def e_inputEnglish(self):
        self.driver.find_element_by_xpath('//*[@id="kw"]').clear()
        self.driver.find_element_by_xpath('//*[@id="kw"]').send_keys("Model-based testing")

    def e_clickSearch(self):
        self.driver.find_element_by_xpath('//*[@id="su"]').click()

    def e_clickResult1(self):
        self.driver.find_element_by_xpath('//*[@id="1"]/h3/a').click()

    def e_clickResult2(self):
        self.driver.find_element_by_xpath('//*[@id="2"]/h3/a').click()

    def e_closeNewTab(self):
        self.closeNewWindow()
