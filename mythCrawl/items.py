# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import pymysql

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

class RenwuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    renwu_id = scrapy.Field()
    alias_name = scrapy.Field()
    nationality = scrapy.Field()
    nation = scrapy.Field()
    birthplace = scrapy.Field()
    birthdate = scrapy.Field()
    occupation = scrapy.Field()
    achieve = scrapy.Field()
    generation = scrapy.Field()
    ancestral_home = scrapy.Field()
    official = scrapy.Field()
    confer = scrapy.Field()
    posthumous_title = scrapy.Field()
    investiture = scrapy.Field()
    dearth_time = scrapy.Field()
    zihao = scrapy.Field()
    master_works = scrapy.Field()
    tomb = scrapy.Field()
    era_name = scrapy.Field()
    foreign_name = scrapy.Field()
    belief = scrapy.Field()
    details = scrapy.Field()

    # 人物更多信息
    life_story = scrapy.Field()
    life_introduced = scrapy.Field()
    achievement = scrapy.Field()
    celebrated = scrapy.Field()
    historical_evaluation = scrapy.Field()
    master_works = scrapy.Field()
    infos = scrapy.Field()

    def get_sql(self):
        infos = self['infos']

        if infos:
            sql = "insert into wx_renwu_info (renwu_id,field_id,content) VALUES "
            for vo in infos:
                content = vo['content']
                content = pymysql.escape_string(content)
                field_id = vo['fid']
                sql += "('" + str(self['renwu_id']) + "' , '" + str(field_id) + "' , '"+ content + "'),"

            sql = sql[:-1]
            return sql
        return ''

    def update_sql(self):
        sql = """
                update wx_renwu_lists set alias_name=%s,nationality=%s,nation=%s,birthplace=%s,birthdate=%s,occupation=%s,achieve=%s,generation=%s,ancestral_home=%s
                    official=%s,confer=%s,posthumous_title=%s,investiture=%s,dearth_time=%s,zihao=%s,master_works=%s,tomb=%s,era_name=%s,foreign_name=%s,belief=%s,details=%s)
                where id = %s
            """

        generation = pymysql.escape_string(self['generation']) if self['generation'] else ''
        master_works = pymysql.escape_string(self['master_works']) if self['master_works'] else ''
        details = pymysql.escape_string(self['details']) if self['details'] else ''
        belief = pymysql.escape_string(self['belief']) if self['belief'] else ''

        sql = "update wx_renwu_lists set alias_name='"+self['alias_name']+"',nationality='"+self['nationality']+"',nation='"+self['nation']+"',birthplace='"+self['birthplace']+"',\
            birthdate='"+self['birthdate']+"',occupation='"+self['occupation']+"',achieve='"+self['achieve']+"',generation='"+generation+"',ancestral_home='"+self['ancestral_home']+"' ,\
            official='"+self['official']+"',confer='"+self['confer']+"',posthumous_title='"+self['posthumous_title']+"',investiture='"+self['investiture']+"',\
            dearth_time='"+self['dearth_time']+"',zihao='"+self['zihao']+"',master_works='"+master_works+"',tomb='"+self['tomb']+"',\
            era_name='"+self['era_name']+"',foreign_name='"+self['foreign_name']+"',belief='"+belief+"',details='"+details+"' \
            where id = '"+str(self['renwu_id'])+"'"
        params = (
            # self['alias_name'], self['nationality'], self['nation'], self['birthplace'], self['birthdate'], self['occupation'], self['achieve'], self['generation'], 
            # self['ancestral_home'], self['official'], self['confer'], self['posthumous_title'], self['investiture'], self['dearth_time'], self['zihao'], self['master_works'], 
            # self['tomb'], self['era_name'], self['foreign_name'], self['belief'], self['details'], self['renwu_id'] 
        )

        return sql, params

class ReissImgsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()
    renwu_id = scrapy.Field()
    image_paths = scrapy.Field()

