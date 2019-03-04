# -*- coding: utf-8 -*-
import scrapy
import time
import requests
import re
import json
import datetime

try:
    import urlparse as parse
except:
    from urllib import parse

from selenium import webdriver
from scrapy.loader import ItemLoader
from ArticleSpider.items import zhihuQuestionItem,zhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ["www.zhihu.com"]
    start_urls = ["https://www.zhihu.com/"]

    # answer第一页起始请求
    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&limit={1}&offset={2}&sort_by=default&platform=desktop'
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):
        all_urls = response.css('a::attr(href)').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith('https') else False, all_urls)
        for url in all_urls:
            match_obj = re.match('(.*.zhihu.com/question/(\d+))(/|$).*', url)
            if match_obj:
                question_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield scrapy.Request(question_url, headers=self.headers, meta={'url_id': question_id},
                                     callback=self.parse_question)
            else:
                # pass
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        items = ItemLoader(item=zhihuQuestionItem(), response=response)
        items.add_css('title', '.QuestionHeader .QuestionHeader-title::text')
        items.add_css('answer_num', '.List-headerText span::text')
        items.add_css('follow_num', '.NumberBoard-item strong::text')
        items.add_css('watched_num', '.NumberBoard-item strong::text')
        items.add_css('content', '.QuestionRichText span::text')
        items.add_css('comment_number', '.QuestionHeader-Comment button::text')
        items.add_css('topic', '.QuestionHeader-topics .Popover div::text')
        items.add_value('url', response.url)
        items.add_value('url_id', response.meta['url_id'])
        question_item = items.load_item()
        yield scrapy.Request(self.start_answer_url.format(response.meta['url_id'], 20, 0), headers=self.headers, callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        ans_json = json.loads(response.text)
        is_end = ans_json['paging']['is_end']
        is_start = ans_json['paging']['is_start']
        next_url = ans_json['paging']['next']
        previous = ans_json['paging']['previous']
        totals = ans_json['paging']['totals']

        for data in ans_json['data']:
            item = zhihuAnswerItem()
            item['zhihu_id'] = data['id']
            item['url'] = data['url']
            item['question_id'] = data['question']['id']
            item['author_id'] = data['author']['id'] if 'id' in data['author'] else None
            item['content'] = data['content'] if 'content' in data else data['excerpt']
            item['praise_num'] = data['voteup_count']
            item['comments_num'] = data['comment_count']
            item['create_time'] = data['created_time']
            item['update_time'] = data['updated_time']
            item['crawl_time'] = datetime.datetime.now()

            yield item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers,
                                 callback=self.parse_answer)

    def start_requests(self):
        browser = webdriver.Chrome(
            executable_path="D:\Program Files (x86)\py项目\ArticleSpider\ArticleSpider\spiders\chromedriver.exe")
        browser.get('http://www.zhihu.com/signin')
        browser.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys(
            '13043456258')
        browser.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys('cxy52299')
        browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()
        # time.sleep(3)
        cookies = browser.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict, headers=self.headers)]
