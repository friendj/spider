import time
import selenium
from selenium import webdriver
from scrapy.selector import Selector
import scrapy
import requests
try:
    import urlparse as parse
except:
    from urllib import parse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
header = {
        'HOST': "www.zhihu.com",
        'Referer': "https://www.zhihu.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
class zhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com']


    def parse(self, response):
        pass


    def start_requests(self):
        browser = webdriver.Chrome(executable_path="D:\Program Files (x86)\py项目\ArticleSpider\ArticleSpider\spiders\chromedriver.exe")
        browser.get('http://www.zhihu.com/signin')
        browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys('13043456258')
        browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys('cxy52299')
        browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()
        time.sleep(3)
        browser.close()

        print(browser.get_cookies)
        return ''

    def check_login(self, response):
        print('1')
        print(response.text)



