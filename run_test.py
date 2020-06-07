import sys,time
import os
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# print(rootPath)
# sys.path.append(rootPath)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scrapy import cmdline


cmdline.execute("scrapy crawl renwu_baike".split())






