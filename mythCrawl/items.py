# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MythcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    lipic = scrapy.Field()
    review_num = scrapy.Field()

    def get_sql(self):
        sql = """
                insert into myth_themes (content,author,lipic,review_num)
                VALUES (%s,%s,%s,%s)
            """
        params = (
            self['content'], self['author'], self['lipic'], self['review_num']
        )

        return sql, params
