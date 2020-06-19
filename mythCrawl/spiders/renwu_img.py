# -*- coding: utf-8 -*-
import scrapy,traceback,re,json, requests

from mythCrawl.items import RenwuItem
import urllib
# from scrapy_redis.spiders import RedisSpider

from w3lib.html import remove_tags

import pymysql
from ..items import ReissImgsItem

from scrapy.utils.project import get_project_settings

from bs4 import BeautifulSoup
import bs4
import lxml

# class MythSpider(RedisSpider):
class RenwuSpider(scrapy.Spider):
    name = 'renwu_img'
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

        cursor.execute("SELECT * FROM wx_renwu_lists where cate_code !='list_shijie' and cate_code!='list_riben'\
             and cate_code!='list_riben' and cate_code!='list_xiandai' and cate_code!='list_deguo' and cate_code!='list_meiguo' and cate_code!='list_yingguo'\
                 and cate_code!='list_yidali' and cate_code!='list_chaoxian' and cate_code!='list_eguo' and cate_code!='list_faguo' and cate_code!='list_faguo' and cate_code!='list_xianya'")


        # cursor.execute("SELECT * FROM wx_renwu_lists where id=7005")
        rows = cursor.fetchall()

        # cursor.execute('SELECT * FROM wx_renwu_info')
        # is_crawls = cursor.fetchall()

        # crawled = []
        # for cr in is_crawls:
        #     crawled.append(cr[1])

        # print(crawled)
        for row in rows:
            renwu_id = row[0]
            # if renwu_id not in crawled:
            url = 'https://baike.baidu.com/item/' + row[3]
            if row[3] == '雷神':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/2428'
            elif row[3] == '范无救':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/23119759'
            elif row[3] == '仓颉':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/735'
            elif row[3] == '无当圣母':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/10384652'
            elif row[3] == '谢必安':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/10207021'
            elif row[3] == '吴刚':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/747'
            elif row[3] == '闻仲':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/2926894'
            elif row[3] == '孟婆':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/172504'
            elif row[3] == '阿羞':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/22174598'
            elif row[3] == '花木兰':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/6456'
            elif row[3] == '韩子高':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/1979472'
            elif row[3] == '避水金睛兽':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/6108800'
            elif row[3] == '火德星君':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/1899985'
            elif row[3] == '沃丁':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/5802968'
            elif row[3] == '姬静':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/3576376'
            elif row[3] == '伯邑考':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/10441358'
            elif row[3] == '周公':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/131359'
            elif row[3] == '孙膑':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/133572'
            elif row[3] == '庄子':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/8074'
            elif row[3] == '晏婴':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/982275'
            elif row[3] == '司马错':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/883006'
            elif row[3] == '郑袖':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/3919894'
            elif row[3] == '魏美人':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/18899252'
            elif row[3] == '申不害':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/1407321'
            elif row[3] == '楚灵王':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/7273818'
            elif row[3] == '齐襄王':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/1855061'
            elif row[3] == '乐羊':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/641151'
            elif row[3] == '王龁':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/9839282'
            elif row[3] == '鲁仲连':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/578311'
            elif row[3] == '羊斟':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/23222378'
            elif row[3] == '宋平公':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/4406195'
            elif row[3] == '共姬':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/9197043'
            elif row[3] == '项羽':
                url = 'https://baike.baidu.com/item/'+ row[3] + '/7005'
            
            yield scrapy.Request(url=url, meta={'renwu': row}, dont_filter=True)

    def parse(self, response):
        request_url = response.request.url
        print(request_url)

        renwu = response.meta['renwu']
        renwu_id = renwu[0]

        img = response.xpath('//div[@class="summary-pic"]/a/img/@src').extract_first()
        item = ReissImgsItem()
        item['renwu_id'] = renwu_id
        item['image_urls'] = [img]
        yield item

        
    
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
            '主要功绩':'achievement',
            '记载':'folklore',
            '史料记载':'records',
            '历史功绩':'achievement',
            '传说':'folklore',
            '八卦杂谈':'records',
            '人物经历':'life_story',
            '主要成就':'achievement',
            '故里争辩':'historical',
            '后世考证':'historical',
            '相关历史':'records',
            '神话人物':'folklore',
            '个人轶事': 'folklore',
            '古今记述':'life_story',
            '古代史料':'records',
            '巴蜀传说':'folklore',
            '版本1':'folklore',
            '典籍记载':'records',
            '相关传说':'folklore',
            '相关记载':'records',
            '早年':'folklore',
            '疑云':'records',
            '角色原型':'records',
            '烛龙':'records',
            '人物设定':'life_story',
            '文学记载':'records',
            '传说之一':'folklore',
            '传说之二':'folklore',
            '传说之三':'folklore',
            '传说之四':'folklore',
            '评价':'historical',
            '出场':'folklore',
            '原著原文':'records',
            '人物介绍':'life_story',
            '角色设定':'life_story',
            '相关资料':'historical',
            '相关故事':'folklore',
            '人物简述':'historical',
            '原著描写':'records',
            '历史考证':'historical',
            '原著引用':'historical',
            '人物来历':'folklore',
            '人物引述':'historical'

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

        self.record_err(content)
        return ''


    # def start_requests(self):
    #     for i in self.start_urls:
    #         yield scrapy.Request(i, meta={
    #             'dont_redirect': True,
    #             'handle_httpstatus_list': [302]
    #         }, callback=self.parse) 

    def record_err(self, content):
        settings = get_project_settings()
        root = settings['MYSQL_USER']
        password = settings['MYSQL_PASSWORD']
        db_name = settings['MYSQL_DBNAME']
        host = settings['MYSQL_HOST']
        connect = pymysql.connect(user=root, password=password, db=db_name, host=host, port=3306, charset='utf8')
        cursor = connect.cursor()

        sql = "insert into wx_renwu_field (name) VALUES ('"+content+"')"
        print(sql)
        cursor.execute(sql)
        connect.commit()

        # 关闭cursor对象
        cursor.close()
        # 关闭connection对象
        connect.close()


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
    pre_title = pre.find('h2')
    if not pre.find('h2'):
        pre_title = pre.find('h3')

    pre_title = pre_title.text
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