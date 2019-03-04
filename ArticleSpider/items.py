# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader
import re
import datetime
from utils import common
from settings import SQL_DATE_FORMAT,SQL_DATETIME_FORMAT


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        num = int(match_re.group(1))
    else:
        num = 0
    return num


def return_value(value):
    return value


def get_time(value):
    time = value.strip().replace('·', '').strip()
    try:
        time = datetime.datetime.strptime(time, "%Y/%m/%d").date()
    except Exception as s:
        time = datetime.datetime.now().date()
    return time


class ArticleItem(scrapy.Item):
    title = scrapy.Field(
    )
    time = scrapy.Field(
        input_processor=MapCompose(get_time)
    )
    url_object_id = scrapy.Field()
    url = scrapy.Field()
    nice = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    bookmark = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()


class zhihuQuestionItem(scrapy.Item):
    title = scrapy.Field()
    answer_num = scrapy.Field()
    follow_num = scrapy.Field()
    watched_num = scrapy.Field()
    content = scrapy.Field()
    comment_number = scrapy.Field()
    topic = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()

    def get_insert_sql(self):
        sql = """insert into zhihuQuestion(title,answer_num,follow_num,watched_num,content,comment_number,topic,url,url_id)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE answer_num = VALUES (answer_num), follow_num = VALUES (follow_num), watched_num = VALUES (watched_num),
         content = VALUES (content), comment_number = VALUES (comment_number), topic = VALUES (topic)
        """
        title = ''.join(self['title'])if 'title' in self else None
        answer_num = common.get_number(''.join(self['answer_num']).replace(',','')) if 'answer_num' in self else None
        follow_num = common.get_number(''.join(self['follow_num'][0]).replace(',','')) if 'follow_num' in self else None
        watched_num = common.get_number(''.join(self['follow_num'][1]).replace(',','')) if 'watched_num' in self else None
        content = ''.join(self['content']) if 'content' in self else None
        comment_number = common.get_number(''.join(self['comment_number']).replace(',','')) if 'comment_number' in self else None
        topic = ','.join(self['topic']) if 'content' in self else None
        url = ''.join(self['url'])
        url_id = ''.join(self['url_id'])
        param = (title, answer_num, follow_num, watched_num, content, comment_number, topic, url, url_id)
        return sql,param


class zhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
    def get_insert_sql(self):
        sql = """insert into zhihuAnswer(zhihu_id,url,question_id,author_id,content,praise_num,comments_num,create_time,update_time,crawl_time)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content = VALUES (content), praise_num = VALUES (praise_num), comments_num = VALUES (comments_num),
         update_time = VALUES (update_time), crawl_time = VALUES (crawl_time)
        """
        zhihu_id = self['zhihu_id'] if 'zhihu_id' in self else None
        url = self['url']
        question_id = self['question_id']
        author_id = self['author_id']
        content = self['content']
        praise_num = self['praise_num']
        comments_num = self['comments_num']
        create_time = datetime.datetime.fromtimestamp(self['create_time']).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self['update_time']).strftime(SQL_DATETIME_FORMAT)
        crawl_time = datetime.datetime.fromtimestamp(self['update_time']).strftime(SQL_DATETIME_FORMAT)
        param = (zhihu_id, url, question_id, author_id, content, praise_num, comments_num, create_time, update_time, crawl_time)
        return sql,param