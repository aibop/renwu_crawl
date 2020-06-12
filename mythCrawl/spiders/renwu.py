# -*- coding: utf-8 -*-
import scrapy,traceback,re,json, requests

from mythCrawl.items import RenwuItem
import urllib
# from scrapy_redis.spiders import RedisSpider

from w3lib.html import remove_tags

import pymysql

from scrapy.utils.project import get_project_settings

from bs4 import BeautifulSoup
import bs4
import lxml

# class MythSpider(RedisSpider):
class RenwuSpider(scrapy.Spider):
    name = 'renwu_baike'
    redis_key = 'myth:theme:start_urls'
    allowed_domains = ['baike.baidu.com']
    # start_urls = ['https://baike.baidu.com/item/炎帝']

    def start_requests(self):
        settings = get_project_settings()
        root = settings['MYSQL_USER']
        password = settings['MYSQL_PASSWORD']
        db_name = settings['MYSQL_DBNAME']
        host = settings['MYSQL_HOST']
        connect = pymysql.connect(user=root, password=password, db=db_name, host=host, port=3306, charset='utf8')
        cursor = connect.cursor()

        cursor.execute('SELECT * FROM wx_renwu_lists limit 100')
        rows = cursor.fetchall()
        for row in rows:
            print(row[3])
            url = 'https://baike.baidu.com/item/' + row[3]
            yield scrapy.Request(url=url, meta={'renwu': row}, dont_filter=True)

    def parse(self, response):
        request_url = response.request.url
        print(request_url)

        
        main_content = response.xpath('//div[@class="main-content"]').extract_first()
        # print(main_content)
        soup = BeautifulSoup(main_content, "lxml")

        div1 = soup.find_all(attrs={'class':'para-title level-2'})
        infos = {}
        for div in div1:
            div2 = soup.find(attrs={'class':'anchor-list '})
            txt = get_content_between_tables(div, div2)

            info = ''
            title = ''
            for v in txt:
                title = v['title']
                
                content = v['content']
                info += content

            title = self.info_fields(title)

            
            if title:
                infos[title] = info

        print(infos)

        item = RenwuItem()
        item['infos'] = infos

        renwu = response.meta['renwu']
        renwu_id = renwu[0]

        renwu_info = response.xpath('//div[@class="lemma-summary"]').extract_first()
        content = self.go_remove_tag(renwu_info) if renwu_info else ''
        print(content)
        
        item['renwu_id'] = renwu_id
        item['alias_name'] = ''
        item['details'] = content
        item['nationality'] = renwu[6]
        item['zihao'] = ''
        item['generation'] = renwu[12]
        item['nation'] = renwu[7]
        item['birthplace'] = renwu[8]
        item['birthdate'] = renwu[9]
        item['dearth_time'] = ''
        item['master_works'] = ''
        item['achieve'] = ''
        item['ancestral_home'] = ''
        item['official'] = ''
        item['confer'] = ''
        item['posthumous_title'] = ''
        item['investiture'] = ''
        item['tomb'] = ''
        item['era_name'] = ''
        item['foreign_name'] = ''
        item['occupation'] = ''
        item['belief'] = ''

        basic_info_arr = response.xpath('//dl[contains(@class,"basicInfo-block")]')
        for dd in basic_info_arr:
            names = dd.xpath('./dt')
            for d in names:
                name = d.xpath('./text()').extract_first()
                name = self.go_remove_tag(name)
                field = self.field_get(name)
                value = d.xpath('./following-sibling::dd').xpath('string(.)').extract_first()
                value = self.go_remove_tag(value)
                print(name)
                print(field)
                print(value)
                if field and not item[field]:
                    item[field] = value

        yield item
        # print(item)  
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

    def field_get(self, content):
        fields = {
            # '本名':name,
            '别名':'alias_name',
            '别称':'alias_name',
            '国籍':'nationality',
            '字号':'zihao',
            '所处时代':'generation',
            '民族族群':'nation',
            '民族':'nation',
            '出生地':'birthplace',
            '出生时间':'birthdate',
            '去世时间':'dearth_time',
            '主要作品':'master_works',
            '主要成就':'achieve',
            '祖籍':'ancestral_home',
            '官职':'official',
            '追赠':'confer',
            '谥号':'posthumous_title',
            '封爵':'investiture',
            '陵墓':'tomb',
            '年号':'era_name',
            '外文名':'foreign_name',
            '职业':'occupation',
            '信仰':'belief'
        }

        if content in fields:
            return fields[content]
        return ''

    def info_fields(self,content):
        fields = {
            '民间传说':'folklore',
            '来历传说':'folklore',
            '趣闻轶事':'folklore',
            '相关争议':'controversy',
            '生平事迹':'life_story',
            '生平经历':'life_story',
            '人物生平':'life_story',
            '活动区域':'movement_area',
            '文献记载':'records',
            '史书记载':'records',
            '史籍记载':'records',
            '主要成就':'achievement',
            '历史评价':'historical',
            '轶事典故':'folklore',
            '文学成就':'achievement',
            '人物简介':'life_story',
            '主要作品':'master_works',

            # '主要成就':'achieve',
            # '祖籍':'ancestral_home',
            # '官职':'official',
            # '追赠':'confer',
            # '谥号':'posthumous_title',
            # '封爵':'investiture',
            # '陵墓':'tomb',
            # '年号':'era_name',
            # '外文名':'foreign_name',
            # '职业':'occupation',
            # '信仰':'belief'
        }

        if content in fields:
            return fields[content]
        return ''


    # def start_requests(self):
    #     for i in self.start_urls:
    #         yield scrapy.Request(i, meta={
    #             'dont_redirect': True,
    #             'handle_httpstatus_list': [302]
    #         }, callback=self.parse) 


def go_remove_tag(value):
    content = remove_tags(value)
    return re.sub(r'[\t\r\n\s]', '', content)

def have_next(ele):
    try:
        ele.next()
    except:
        return False
    return True

def is_child(child, father):
    if child in father:
        return True
    seek_list = father.contents
    for i in seek_list:
        if isinstance(i, bs4.element.NavigableString):
            pass
        elif child in i:
            return True
        else:
            flag = is_child(child, i)
            if flag == True:
                return True
    return False

def get_content_between_tables(pre, nxt):
    #如果第二个table在第一个里面
    txt = []
    pre_title = pre.find('h2').text
    prefix = pre.find('span').text
    pre_title = pre_title.replace(prefix,'')

    nxt_name = nxt.attrs['class']
    if is_child(nxt, pre):
        cur = pre.next_element
        while cur != nxt and cur is not None:
            if isinstance(cur, bs4.element.NavigableString):
                txt += cur
            cur = cur.next_element
    #类似并列关系
    else:
        #先找到pre结束的下一个元素
        cur = pre.next_element
        while is_child(cur, pre):
            cur = cur.next_element

        while cur != nxt and cur is not None:
            cur_name = ''
            if not isinstance(cur, bs4.element.NavigableString) :
                cur_name = cur.attrs['class'] if 'class' in cur.attrs else ''

            if nxt_name == cur_name:
                print(nxt)
                break
            else:
                if isinstance(cur, bs4.element.NavigableString):
                    # txt += cur
                    next_cur = go_remove_tag(cur)
                    if next_cur:
                        tmp = {
                            'title':pre_title,
                            'content':next_cur
                        }
                        txt.append(tmp)
                cur = cur.next_element


        #获取内容
        # while cur != nxt and cur is not None:
        #     if isinstance(cur, bs4.element.NavigableString):
        #         # txt += cur
        #         next_cur = go_remove_tag(cur)
        #         if next_cur:
        #             tmp = {
        #                 'title':pre_title,
        #                 'content':next_cur
        #             }
        #             txt.append(tmp)
        #     cur = cur.next_element

    return txt