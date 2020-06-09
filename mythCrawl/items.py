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

    def get_sql(self):
        sql = """
                insert into myth_themes (content,author,lipic,review_num)
                VALUES (%s,%s,%s,%s)
            """
        params = (
            self['content'], self['author'], self['lipic'], self['review_num']
        )

        return sql, params

    def update_sql(self):
        sql = """
                update wx_renwu_lists set alias_name=%s,nationality=%s,nation=%s,birthplace=%s,birthdate=%s,occupation=%s,achieve=%s,generation=%s,ancestral_home=%s
                    official=%s,confer=%s,posthumous_title=%s,investiture=%s,dearth_time=%s,zihao=%s,master_works=%s,tomb=%s,era_name=%s,foreign_name=%s,belief=%s,details=%s)
                where id = %s
            """

        sql = "update wx_renwu_lists set alias_name='"+self['alias_name']+"',nationality='"+self['nationality']+"',nation='"+self['nation']+"',birthplace='"+self['birthplace']+"',\
            birthdate='"+self['birthdate']+"',occupation='"+self['occupation']+"',achieve='"+self['achieve']+"',generation='"+self['generation']+"',ancestral_home='"+self['ancestral_home']+"' ,\
            official='"+self['official']+"',confer='"+self['confer']+"',posthumous_title='"+self['posthumous_title']+"',investiture='"+self['investiture']+"',\
            dearth_time='"+self['dearth_time']+"',zihao='"+self['zihao']+"',master_works='"+self['master_works']+"',tomb='"+self['tomb']+"',\
            era_name='"+self['era_name']+"',foreign_name='"+self['foreign_name']+"',belief='"+self['belief']+"',details='"+self['details']+"' \
            where id = '"+str(self['renwu_id'])+"'"
        params = (
            # self['alias_name'], self['nationality'], self['nation'], self['birthplace'], self['birthdate'], self['occupation'], self['achieve'], self['generation'], 
            # self['ancestral_home'], self['official'], self['confer'], self['posthumous_title'], self['investiture'], self['dearth_time'], self['zihao'], self['master_works'], 
            # self['tomb'], self['era_name'], self['foreign_name'], self['belief'], self['details'], self['renwu_id'] 
        )

        return sql, params

