# -*- coding: utf-8 -*-

import scrapy
import re
import datetime
from  scrapy.http import Request
from urllib import parse
from ArticleSpider.items import ArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader
global a
a=0
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']


    def parse(self, response):
        print(response.text)
        url_selector = response.css('#archive .floated-thumb .post-thumb a')
        for i in url_selector:
            image = i.css("img::attr(src)").extract_first("")
            post = i.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post),meta={"front_image_url":image},callback=self.parse_detail)
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        print("next_url:",next_url)
        # if next_url:
        #     yield Request(url=next_url, callback=self.parse)


    def parse_detail(self,response):
        # 提取文章的具体字段
        re_selector = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        re2_selector = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first("")
        re3_selector = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first("")
        re4_selector = 0
        b = re.match(".*?(\d+).*",response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract_first(""))
        if b:
            re4_selector = b.group(1)
        items = ArticleItem()
        # global a
        # if re_selector:
        #     f=open("D:\Program Files (x86)\py项目\spider.txt","a")
        #     f.write(re_selector)
        #     a=a+1
        #     print('title:',re_selector)
        #     items['title'] = re_selector
        #     if re2_selector:
        #         time = re2_selector.strip().replace('·','').strip()
        #         try:
        #             time = datetime.datetime.strptime(time,"%Y/%m/%d").date()
        #         except Exception as s:
        #             time = datetime.datetime.now().date()
        #         print('time:', time)
        #         items['time'] = time
        #     else:
        #         print('time:none')
        #         items['time'] = 0
        #     if re3_selector:
        #         print('nice:',re.match(".*?(\d+).*",re3_selector).group(1))
        #         items['nice'] = re.match(".*?(\d+).*",re3_selector).group(1)
        #     else:
        #         print('nice:',0)
        #         items['nice'] = 0
        #     if re4_selector:
        #         print('bookmark:', re4_selector)
        #         items['bookmark'] = re4_selector
        #     else:
        #         print('bookmark:', 0)
        #         items['bookmark'] = 0
        # print(response.meta.get("front_image_url",""))
        # items['front_image_url'] = [response.meta.get("front_image_url","")]
        # print(response.url)
        # items['url'] = response.url
        # items['url_object_id'] = get_md5(response.url)
        # print(a)
        item_loader = ArticleItemLoader(item=ArticleItem(),response=response)
        item_loader.add_xpath("title",'//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath("time",'//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_xpath("nice",'//span[contains(@class,"vote-post-up")]/h10/text()')
        item_loader.add_xpath('bookmark','//span[contains(@class,"bookmark-btn")]/text()')
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',get_md5(response.url))
        item_loader.add_value('front_image_url',response.meta.get("front_image_url",""))
        items = item_loader.load_item()
        yield items
