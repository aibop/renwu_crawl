# -*- coding: utf-8 -*-

# Scrapy settings for mythCrawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import platform, os

BOT_NAME = 'mythCrawl'

SPIDER_MODULES = ['mythCrawl.spiders']
NEWSPIDER_MODULE = 'mythCrawl.spiders'

# scrapy-redis使用时需启用，用于指定调度器和过滤器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mythCrawl (+http://www.yourdomain.com)'
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# Obey robots.txt rules
# 是否遵循机器人协议，关闭
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'mythCrawl.middlewares.MythcrawlSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'mythCrawl.middlewares.MythcrawlDownloaderMiddleware': 543,
   'mythCrawl.my_middlewares.UserAgent.RotateUserAgentMiddleware': 551,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'mythCrawl.pipelines.MythcrawlPipeline': 300,
   # 'mythCrawl.pipelines.RenWuListPipeline': 300,
   'mythCrawl.pipelines.ReissImgDownloadPipeline': 301,
    # 'scrapy_redis.pipelines.RedisPipeline': 301
}



if platform.system() == 'Windows':
   CONFIG_PATH = 'D:\data_dir'
   REDIS_HOST = '127.0.0.1'
   REDIS_PORT = 6379
   REDIS_PARAMS = {'password': ''}

   MYSQL_HOST = "127.0.0.1"
   MYSQL_DBNAME = "wx-apply"
   MYSQL_USER = "root"
   MYSQL_PASSWORD = "123456"

else:
   CONFIG_PATH = '/root/data_dir'
   REDIS_HOST = '39.104.131.59'
   REDIS_PORT = 6379
   REDIS_PARAMS = {'password': 'oFtu01ReAFqO68D'}
   SENTINEL_PORT = 26379
   HOST_SLAVE = '172.18.11.136'

   MYSQL_HOST = "39.104.131.59"
   MYSQL_DBNAME = "wx-apply"
   MYSQL_USER = "root"
   MYSQL_PASSWORD = "y4NuTl0gcX3qUNCEuPReCFqVK"





# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPERROR_ALLOWED_CODES  = [302]
MEDIA_ALLOW_REDIRECTS = True


# 获取当前目录绝对路径
project_dir = os.path.abspath(os.path.dirname(__file__))
# 获取images存储路径
# IMAGES_STORE = os.path.join(project_dir,'images')
IMAGES_URLS_FIELD = "image_urls"  # 对应item里面设定的字段，取到图片的url
IMAGES_RESULT_FIELD = "image_path"
prodir = os.path.abspath(os.path.dirname(__file__))
# IMAGES_STORE = 'E:\\tobox\\reiss\\images' # 设置图片保存path
IMAGES_STORE = 'F:\\lee\\wx-apply\\public\\renwu\\images' # 设置图片保存path