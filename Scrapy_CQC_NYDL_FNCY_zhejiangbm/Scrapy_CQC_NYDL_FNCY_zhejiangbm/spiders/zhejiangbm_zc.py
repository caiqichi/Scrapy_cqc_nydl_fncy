from Scrapy_CQC_NYDL_FNCY_zhejiangbm import upload_replace as ur
from Scrapy_CQC_NYDL_FNCY_zhejiangbm.pipelines import MongoDBPipeline
from Scrapy_CQC_NYDL_FNCY_zhejiangbm.items import InfoItem  # 需要修改下爬虫项目名！！！

from scrapy_splash import SplashRequest  # 处理经过渲染的页面！！！
import re
import scrapy
from scrapy.utils import request  # 处理哈希值id（news_id）
import logging
import time
from scrapy.http import FormRequest
logger = logging.getLogger(__name__)

import json
class ZhejiangbmZcSpider(scrapy.Spider):
    name = 'zhejiangbm_zc'
    # allowed_domains = ['www']
    # start_urls = ['http://www/']
    web_name = '浙江省生态环境厅'  # 网站名称
    category = '能源电力'  # 模块
    sub_category = '风能产业'  # 产业
    address = '浙江'  # 地址

    mongo = MongoDBPipeline()
    db = mongo.db
    collection = mongo.mongo_collection

    def start_requests(self):
        # for i in range(1,51):
        for i in range(1,2):
            url = "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?standardXxgk=0&isAllList=1&texttype=0&fbtime=-1&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage={0}&sortfield=,compaltedate:0".format(i)
            data = {
                'infotypeId': 'B001AC001',
                'jdid': '1756',
                'area': '002482429',
                'divid': 'div1474328',
                'vc_title': '',
                'vc_number': '',
                'sortfield': ',compaltedate:0',
                'currpage': str(i),
                'vc_filenumber': '',
                'vc_all': '',
                'texttype': '0',
                'fbtime': '-1',
                'standardXxgk': '0',
                'isAllList': '1',
                'texttype': '0',
                'fbtime': '-1',
                'vc_all': '',
                'vc_filenumber': '',
                'vc_title': '',
                'vc_number': '',
                'currpage': str(i),
                'sortfield': ',compaltedate:0',
            }
            yield scrapy.FormRequest(url, callback=self.parse,method="POST",formdata=data,
                                 dont_filter=True)
        # for j in range(1,11):
        for j in range(1, 2):
            url1 = "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?standardXxgk=0&isAllList=1&texttype=0&fbtime=-1&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage={0}&sortfield=,compaltedate:0".format(j)
            data1 = {
                'infotypeId': 'B001G001',
                'jdid': '1756',
                'area': '002482429',
                'divid': 'div1474328',
                'vc_title': '',
                'vc_number': '',
                'sortfield': ',compaltedate:0',
                'currpage': str(j),
                'vc_filenumber': '',
                'vc_all': '',
                'texttype': '0',
                'fbtime': '-1',
                'standardXxgk': '0',
                'isAllList': '1',
                'texttype': '0',
                'fbtime': '-1',
                'vc_all': '',
                'vc_filenumber': '',
                'vc_title': '',
                'vc_number': '',
                'currpage': str(j),
                'sortfield': ',compaltedate:0',
            }
            yield scrapy.FormRequest(url1, callback=self.parse, method="POST", formdata=data1,
                                     dont_filter=True)

    def parse(self, response):
        issue_time_list = re.findall(r"<td align='center' width='80'>(\d+-\d+-\d+)</td>",response.text)
        content_url_list = re.findall(r"<td align='left' width='475' style=.*?<a href='(.*?)' target='_blank' title=",response.text)
        title_list = re.findall(r"title='(.*?)'",response.text)
        for content_url,title,issue_time in zip(content_url_list,title_list,issue_time_list):
            content_url = response.urljoin(content_url)
            title = title
            issue_time = issue_time

            item = InfoItem()
            item["information_source"] = self.web_name
            item["category"] = self.category
            item["sub_category"] = self.sub_category
            item["content_url"] = content_url
            item["title"] = title
            item["issue_time"] = issue_time
            req = scrapy.Request(url=content_url, callback=self.detail_parse, meta={"item": item},
                                 dont_filter=True)
            news_id = request.request_fingerprint(req)  # 必须要求每一个url都有一个唯一的id，所以需要在此处设置
            req.meta['news_id'] = news_id

            if self.db[self.collection].count({'news_id': news_id}):
                continue
            yield req



    def detail_parse(self, response):

        source = self.web_name
        author = None

        # 固定模式，改下xpath即可
        content = response.xpath('//div[@class="main"]').extract()
        content = ''.join(content)  # 转化成字符串，并且去掉空格

        # 处理图片的通用格式:
        # _xpath1 = '//div[@class="text-details"]//img/@src'  # 改下xpath即可
        # images = response.xpath(_xpath1).extract()
        # 处理附件的通用格式
        _xpath2 = '//div[@id="zoom"]//a/@href'  # 改下xpath即可
        attachments = response.xpath(_xpath2).extract()
        # attachments = None
        images = None

        # 使用自定义的函数upload_and_replace来处理图片和附件和内容
        content, images = ur.upload_and_replace(content, images, response)
        content, attachments = ur.upload_and_replace(content, attachments, response)

        # 以下除了item["information_categories"]不固定，其余的全部固定！！！
        item = response.meta["item"]
        item["information_categories"] = "政策法规"
        item["news_id"] = response.meta["news_id"]  # id
        item['area'] = None
        item["tags"] = None
        item["title_image"] = None
        item['attachments'] = attachments
        item['address'] = self.address
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
    os.system('scrapy crawl zhejiangbm_zc')  ##改下爬虫名


