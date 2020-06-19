# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
from scrapy.conf import settings
import redis
# from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem

class MythcrawlPipeline(object):
    def __init__(self,dbpool):
        """异步mysql初始化"""
        self.dbpool = dbpool
        host = settings["REDIS_HOST"]
        port = settings["REDIS_PORT"]
        index_db = 0
        auth = ''
        pool = redis.ConnectionPool(host=host, port=port, db=index_db, password=auth)
        self.redisServ = redis.Redis(connection_pool=pool)

    @classmethod
    def from_settings(cls, settings):
        """class 方法 读取配置的mysql连接"""
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor, #游标
            use_unicode=True    #设置编码是否使用Unicode
        )

        dbpool = adbapi.ConnectionPool("pymysql",dbparms)
        return cls(dbpool)



    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        # self.dbpool.runInteraction(self.do_insert, item)
        self.insert_mysql(item)


    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_sql()
        print(insert_sql)
        if insert_sql:
            cursor.execute(insert_sql, params)

    def insert_mysql(self, item):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DBNAME']
        c = "utf8"
        port = 3306
        # 数据库连接
        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
        # 数据库游标
        cue = con.cursor()
        print("mysql connect succes")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        try:
            self.do_insert(cue, item)
            self.redisServ.lpush('myth-theme',item['content'])
            print("insert success")  # 测试语句
        except Exception as e:
            print('Insert error:', e)
            con.rollback()
        else:
            con.commit()
        con.close()

        return item

    # def process_item(self, item, spider):
    #     return item

class RenWuListPipeline(object):
    def __init__(self,dbpool):
        """异步mysql初始化"""
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """class 方法 读取配置的mysql连接"""
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor, #游标
            use_unicode=True    #设置编码是否使用Unicode
        )

        
        dbpool = adbapi.ConnectionPool("pymysql",dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        # self.dbpool.runInteraction(self.do_insert, item)
        self.insert_mysql(item)


    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        
        
        try:
            update_sql, params = item.update_sql()
            # print(update_sql)
            cursor.execute(update_sql)
        except Exception as e:
            print(e.__traceback__.tb_frame.f_globals["__file__"])   # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)                        # 发生异常所在的行数
        
        insert_sql = item.get_sql()
        try:
            if insert_sql:
                cursor.execute(insert_sql) 
        except:
            print(insert_sql)

    def insert_mysql(self, item):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DBNAME']
        c = "utf8"
        port = 3306
        # 数据库连接
        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
        # 数据库游标
        cue = con.cursor()
        print("mysql connect succes")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        try:
            self.do_insert(cue, item)
            print("insert success")  # 测试语句
        except Exception as e:
            print('Insert error:', e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])   # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)                        # 发生异常所在的行数
            con.rollback()
        else:
            con.commit()
        con.close()

        return item

class ReissImgDownloadPipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        'referer': 'https://baike.baidu.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        print(item)
        if item['image_urls']:
            for image_url in item['image_urls']:
                self.default_headers['referer'] = image_url
                yield Request(image_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        print(results)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths

        self.insertData(item)
        return item
        

    def insertData(self, item):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DBNAME']
        conn = pymysql.connect(host=host, user=user, password=psd, database=db,charset='utf8')
        cur = conn.cursor()
        print(item)
        renwu_id = item["renwu_id"]
        img_path = 'renwu/images/' + item["image_paths"][0]
        sql = "insert into wx_renwu_img(renwu_id,img_path) values(%s,%s)"
        print(sql)
        cur.execute(sql, (renwu_id, img_path))
        conn.commit()
        conn.close()
        return item

