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
