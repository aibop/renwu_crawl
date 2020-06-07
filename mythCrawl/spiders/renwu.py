# -*- coding: utf-8 -*-
import scrapy,traceback,re
import json
# from mythCrawl.items import MythcrawlItem
import urllib
# from scrapy_redis.spiders import RedisSpider

from w3lib.html import remove_tags

# class MythSpider(RedisSpider):
class RenwuSpider(scrapy.Spider):
    name = 'renwu_baike'
    redis_key = 'myth:theme:start_urls'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/炎帝']

    def parse(self, response):
        request_url = response.request.url
        print(request_url)

        renwu_info = response.xpath('//div[@class="lemma-summary"]').extract_first()
        content = self.go_remove_tag(renwu_info)
        print(content)

        alias_name = response.xpath('//dd[@class="basicInfo-item value"][2]/text()').extract_first()
        print(alias_name)

        nationality_arr = response.xpath('//dl[contains(@class,"basicInfo-block")]')
        nationality_tmp = []
        for dd in nationality_arr:
            names = dd.xpath('./dt')
            for d in names:
                name = d.xpath('./text()').extract_first()
                value = d.xpath('./following-sibling::dd').xpath('string(.)').extract_first()
                print(name)
            
                print(value)
            
        #     value = dd.xpath('./dd/text()').extract()
        #     nationality_tmp.append({'name':name,'value':value})

        # print(nationality_tmp)

        # next_page = response.xpath('//div[@class="pg1"]/a/text()').extract()
        # pages = []
        # for page in next_page:
        #     if page == '下一页' or page == '上一页':
        #         continue

        #     pages.append(int(page))

        # max_page = max(pages)
        # n_page = int(current_page) + 1
        # if n_page < max_page:
        #     url = 'http://www.360wa.com/shentucao/' + str(n_page)
        #     print(url)
        #     yield scrapy.Request(url, callback=self.parse)

        # list = response.xpath('//div[@class="p1"]')
        # for li in list:
        #     try:
        #         item = MythcrawlItem()
        #         contents = li.xpath('./div/a/p[2]/text()').extract()
        #         content = ''
        #         for cont in contents:
        #             content += cont

        #         author = li.xpath('./div/div[1]|./div/div[1]/a').xpath('string(.)').extract_first().strip()
        #         item['content'] = content
        #         item['author'] = author
        #         item['lipic'] = ''
        #         item['review_num'] = 0



        #         yield item
        #     except Exception as e:
        #         traceback.print_exc()
        #         print(e)
        #         continue
    
    def go_remove_tag(self,  value):
        content = remove_tags(value)
        return re.sub(r'[\t\r\n\s]', '', content)