# -*- coding: utf-8 -*-
import scrapy,traceback
import json
from mythCrawl.items import MythcrawlItem
import urllib
from scrapy_redis.spiders import RedisSpider

# class MythSpider(RedisSpider):
class MythSpider(scrapy.Spider):
    name = 'myth'
    redis_key = 'myth:theme:start_urls'
    allowed_domains = ['www.360wa.com']
    start_urls = ['http://www.360wa.com/shentucao']

    def parse(self, response):
        request_url = response.request.url
        print(request_url)

        current_page = response.xpath('//span[@class="current"]/text()').extract_first()
        next_page = response.xpath('//div[@class="pg1"]/a/text()').extract()
        pages = []
        for page in next_page:
            if page == '下一页' or page == '上一页':
                continue

            pages.append(int(page))

        max_page = max(pages)
        n_page = int(current_page) + 1
        if n_page < max_page:
            url = 'http://www.360wa.com/shentucao/' + str(n_page)
            print(url)
            yield scrapy.Request(url, callback=self.parse)

        list = response.xpath('//div[@class="p1"]')
        for li in list:
            try:
                item = MythcrawlItem()
                contents = li.xpath('./div/a/p[2]/text()').extract()
                content = ''
                for cont in contents:
                    content += cont

                author = li.xpath('./div/div[1]|./div/div[1]/a').xpath('string(.)').extract_first().strip()
                item['content'] = content
                item['author'] = author
                item['lipic'] = ''
                item['review_num'] = 0



                yield item
            except Exception as e:
                traceback.print_exc()
                print(e)
                continue