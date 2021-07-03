from Scrapy_NYDL_FNCY_chinabm import upload_replace as ur
from Scrapy_NYDL_FNCY_chinabm.pipelines import MongoDBPipeline
from Scrapy_NYDL_FNCY_chinabm.items import InfoItem  # 需要修改下爬虫项目名！！！

from scrapy_splash import SplashRequest  # 处理经过渲染的页面！！！
import re
import scrapy
from scrapy.utils import request  # 处理哈希值id（news_id）
import logging
import time

logger = logging.getLogger(__name__)
import urllib.parse  # utf-8解码
import json

##动态加载数据模块：(固定写法）
from selenium import webdriver
from pydispatch import dispatcher
from scrapy import signals
from selenium.webdriver.chrome.options import Options


class ChinabmxhInfoSpider(scrapy.Spider):
    name = 'chinabmxh_info'
    # allowed_domains = ['w']
    # start_urls = [
    #     'https://www.miit.gov.cn/search-front-server/api/search/info?websiteid=110000000000000&scope=basic&q=&pg=10&cateid=58&pos=title_text%2Cinfocontent%2Ctitlepy&_cus_eq_typename=&_cus_eq_publishgroupname=&_cus_eq_themename=&begin=&end=&dateField=deploytime&selectFields=title,content,deploytime,_index,url,cdate,infoextends,infocontentattribute,columnname,filenumbername,publishgroupname,publishtime,metaid,bexxgk,columnid,xxgkextend1,xxgkextend2,themename,typename,indexcode,createdate&group=distinct&highlightConfigs=%5B%7B%22field%22%3A%22infocontent%22%2C%22numberOfFragments%22%3A2%2C%22fragmentOffset%22%3A0%2C%22fragmentSize%22%3A30%2C%22noMatchSize%22%3A145%7D%5D&highlightFields=title_text%2Cinfocontent%2Cwebid&level=6&sortFields=%5B%7B%22name%22%3A%22deploytime%22%2C%22type%22%3A%22desc%22%7D%5D&p=1',
    #     'https://www.miit.gov.cn/search-front-server/api/search/info?websiteid=110000000000000&scope=basic&q=&pg=10&cateid=59&pos=title_text%2Cinfocontent%2Ctitlepy&_cus_eq_typename=&_cus_eq_publishgroupname=&_cus_eq_themename=&begin=&end=&dateField=deploytime&selectFields=title,content,deploytime,_index,url,cdate,infoextends,infocontentattribute,columnname,filenumbername,publishgroupname,publishtime,metaid,bexxgk,columnid,xxgkextend1,xxgkextend2,themename,typename,indexcode,createdate&group=distinct&highlightConfigs=%5B%7B%22field%22%3A%22infocontent%22%2C%22numberOfFragments%22%3A2%2C%22fragmentOffset%22%3A0%2C%22fragmentSize%22%3A30%2C%22noMatchSize%22%3A145%7D%5D&highlightFields=title_text%2Cinfocontent%2Cwebid&level=6&sortFields=%5B%7B%22name%22%3A%22deploytime%22%2C%22type%22%3A%22desc%22%7D%5D&p=1']
    web_name = '中国人民共和国工业和信息化部'
    category = '能源电力'
    sub_category = '风能产业'
    address = '中国'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        # "Cookie": "_ud_=ccdacf0929a542028896dee0f3aee8d2; _city=%E5%B9%BF%E5%B7%9E%E5%B8%82%E5%A4%A9%E6%B2%B3%E5%8C%BA; jsessionid=rBQdDhroYNmcWIa6Vo3rKUk3i6X1daTtVNgA; __jsluid_h=7f08cc72bf598a0cdce78d533ba01642; __jsluid_s=baa238ebe6e9c00ff3f62215138d2b17; __jsl_clearance_s=1624874070.368|0|12mX5%2BHoE%2F0oNu5YL7G%2B6%2BRvrXE%3D",
        "Cookie": "_ud_=ccdacf0929a542028896dee0f3aee8d2; _city=%E5%B9%BF%E5%B7%9E%E5%B8%82%E5%A4%A9%E6%B2%B3%E5%8C%BA; jsessionid=rBQYnhroYNmeSAbyxt0gVEkCv3ouC6mZj8IA; __jsluid_h=7f08cc72bf598a0cdce78d533ba01642; __jsluid_s=baa238ebe6e9c00ff3f62215138d2b17; __jsl_clearance_s=1624874070.368|0|12mX5%2BHoE%2F0oNu5YL7G%2B6%2BRvrXE%3D"

    }

    headers1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Cookie":" __jsluid_h=7f08cc72bf598a0cdce78d533ba01642; __jsluid_s=baa238ebe6e9c00ff3f62215138d2b17; __jsl_clearance_s=1624874070.368|0|12mX5%2BHoE%2F0oNu5YL7G%2B6%2BRvrXE%3D"
    }

    mongo = MongoDBPipeline()
    db = mongo.db
    collection = mongo.mongo_collection

    lxs = {
        "wenjianfabu": 58,  # 发布文件
        "falvfagui": 59,  # 法律法规
    }




    def start_requests(self):
        # 注意：增加了反爬后，同时带上网站的user_agent和cookie才能访问，可以是固定的cookie，但必须是该网站的cookie。而且翻页操作必须在这里实现。
        for num in range(1, 2):
            url = 'https://www.miit.gov.cn/search-front-server/api/search/info??websiteid=110000000000000&scope=basic&q=&pg=10&cateid={0}&pos=title_text%2Cinfocontent%2Ctitlepy&_cus_eq_typename=&_cus_eq_publishgroupname=&_cus_eq_themename=&begin=&end=&dateField=deploytime&selectFields=title,content,deploytime,_index,url,cdate,infoextends,infocontentattribute,columnname,filenumbername,publishgroupname,publishtime,metaid,bexxgk,columnid,xxgkextend1,xxgkextend2,themename,typename,indexcode,createdate&group=distinct&highlightConfigs=%5B%7B%22field%22%3A%22infocontent%22%2C%22numberOfFragments%22%3A2%2C%22fragmentOffset%22%3A0%2C%22fragmentSize%22%3A30%2C%22noMatchSize%22%3A145%7D%5D&highlightFields=title_text%2Cinfocontent%2Cwebid&level=6&sortFields=%5B%7B%22name%22%3A%22deploytime%22%2C%22type%22%3A%22desc%22%7D%5D&p={1}'
            yield scrapy.Request(url=url.format(self.lxs["wenjianfabu"], num),headers=self.headers,
                                 callback=self.parse, dont_filter=True)  # 表单格式的a必须使用json.dumps转化为字符串
            # yield SplashRequest(url=url.format(self.lxs["wenjianfabu"], num),
            #                      callback=self.parse)

        for num in range(1, 2):
            url = 'https://www.miit.gov.cn/search-front-server/api/search/info??websiteid=110000000000000&scope=basic&q=&pg=10&cateid={0}&pos=title_text%2Cinfocontent%2Ctitlepy&_cus_eq_typename=&_cus_eq_publishgroupname=&_cus_eq_themename=&begin=&end=&dateField=deploytime&selectFields=title,content,deploytime,_index,url,cdate,infoextends,infocontentattribute,columnname,filenumbername,publishgroupname,publishtime,metaid,bexxgk,columnid,xxgkextend1,xxgkextend2,themename,typename,indexcode,createdate&group=distinct&highlightConfigs=%5B%7B%22field%22%3A%22infocontent%22%2C%22numberOfFragments%22%3A2%2C%22fragmentOffset%22%3A0%2C%22fragmentSize%22%3A30%2C%22noMatchSize%22%3A145%7D%5D&highlightFields=title_text%2Cinfocontent%2Cwebid&level=6&sortFields=%5B%7B%22name%22%3A%22deploytime%22%2C%22type%22%3A%22desc%22%7D%5D&p={1}'
            yield scrapy.Request(url=url.format(self.lxs["falvfagui"], num),headers=self.headers,
                                 callback=self.parse, dont_filter=True)  # 表单格式的a必须使用json.dumps转化为字符串
            # yield SplashRequest(url=url.format(self.lxs["falvfagui"], num),
            #                      callback=self.parse)

    def parse(self, response):

        # print(response.text)


        jsonz = json.loads(response.text)

        data = jsonz["data"]
        searchResult = data["searchResult"]
        dataResults = searchResult["dataResults"]
        for i in dataResults:
            groupData = i["groupData"][0]
            data = groupData["data"]

            title = data["title"]
            # print(title)
            content_url = data["jsearch_url"]
            # print(content_url)
            content_url = re.findall(r".*?url=(.*)", content_url)[0]
            content_url = urllib.parse.unquote(content_url)
            content_url = response.urljoin(content_url)
            # "https://www.miit.gov.cn/zwgk/zcwj/wjfb/qt/art/2021/art_7e0cc9ac65614273a23e4888e1f1a085.html&websiteid=110000000000000&cateid=57&infoid=7e0cc9ac65614273a23e4888e1f1a085"
            # content = content_url.decode('utf-8').encode('utf-8')
            # str.decode('utf-8').encode('utf-8')
            # print(content_url)
            issue_time = int(data["deploytime"]) / 1000
            timeArray = time.localtime(issue_time)
            issue_time = time.strftime("%Y-%m-%d", timeArray)  # 时间戳转化为时间格式
            # print(issue_time)

            item = InfoItem()
            item["information_source"] = self.web_name
            item["category"] = self.category
            item["sub_category"] = self.sub_category
            item["content_url"] = content_url
            item["title"] = title
            item["issue_time"] = issue_time
            req = scrapy.Request(url=content_url, callback=self.detail_parse, dont_filter=True,headers=self.headers1,
                                 meta={"item": item})
            # 注意：必须带上headers，headers带有详情页的cookie和user_agent
            # req = SplashRequest(url=content_url, callback=self.detail_parse, dont_filter=True,
            #                      meta={"item": item})
            news_id = request.request_fingerprint(req)  # 必须要求每一个url都有一个唯一的id，所以需要在此处设置
            req.meta['news_id'] = news_id

            req.meta.update({'news_id': news_id, 'title': title})

            if self.db[self.collection].count({'news_id': news_id}):
                continue

            yield req

    def detail_parse(self, response):
        try:
            source = response.xpath(
                '//*[@id="barrierfree_container"]//div[@class="cinfo center"]/span[2]/text()').extract_first() if response.xpath(
                '//*[@id="barrierfree_container"]//div[@class="cinfo center"]/span[2]/text()').extract_first() else self.web_name
            source = source.split('：')[1] if source.split('：')[1] else self.web_name
            # source = source.split('：')[1].split(' ')[0] if source.split('：')[1].split(' ')[0] not in '' else None
        except:
            source = self.web_name

        content = response.xpath(
            '//div[@id="con_con"] | //div[@id="barrierfree_container"] | //body[@id="page_type"]').extract()
        content = ''.join(content)
        # author = None
        author = response.xpath('./a').extract_first() if response.xpath('./a').extract_first() else None

        # 处理图片的通用格式:
        _xpath1 = '//div[@id="con_con"]//img/@src'  # 改下xpath即可
        images = response.xpath(_xpath1).extract()
        # 处理附件的通用格式
        _xpath2 = '//div[@id="con_con"]//a/@href'  # 改下xpath即可
        attachments = response.xpath(_xpath2).extract()

        # 使用自定义的函数upload_and_replace来处理图片和附件和内容
        content, images = ur.upload_and_replace(content, images, response)
        content, attachments = ur.upload_and_replace(content, attachments, response)

        item = response.meta["item"]
        item["information_categories"] = "政策法规"
        item["news_id"] = response.meta["news_id"]  # id
        item['area'] = None
        item["title_image"] = None
        item['attachments'] = attachments
        item['address'] = self.address
        item['tags'] = None
        item['sign'] = '37'
        item['update_time'] = str(int(time.time() * 1000))
        item['cleaning_status'] = 0
        item["source"] = source
        item["author"] = author
        item["content"] = content
        item["images"] = images
        yield item


import os

if __name__ == '__main__':
    os.system('scrapy crawl chinabmxh_info')  ##改下爬虫名
