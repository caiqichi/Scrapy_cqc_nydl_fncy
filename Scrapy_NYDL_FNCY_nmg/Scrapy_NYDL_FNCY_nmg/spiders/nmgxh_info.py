from Scrapy_NYDL_FNCY_nmg import upload_replace as ur
from Scrapy_NYDL_FNCY_nmg.pipelines import MongoDBPipeline
from Scrapy_NYDL_FNCY_nmg.items import InfoItem  # 需要修改下爬虫项目名！！！

from scrapy_splash import SplashRequest  # 处理经过渲染的页面！！！

import scrapy
from scrapy.utils import request  # 处理哈希值id（news_id）
import logging
import time
logger = logging.getLogger(__name__)

import json

class NmgxhInfoSpider(scrapy.Spider):
    name = 'nmgxh_info'
    # allowed_domains = ['w']
    start_urls = ['https://news.bjx.com.cn/zt.asp?topic=%C4%DA%C3%C9%B9%C5%B7%E7%B5%E7']
    web_name = '北极星电力新闻网'  # 网站名称
    category = '能源电力'  # 模块
    sub_category = '风能产业'  # 产业
    address = '内蒙古'  # 地址

    mongo = MongoDBPipeline()
    db = mongo.db
    collection = mongo.mongo_collection

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse,
                                 dont_filter=True)

    def parse(self, response):
        li_list = response.xpath('//ul[@class="list_left_ztul"]/li[not(@class)]')
        for li in li_list:
            content_url = li.xpath("./a/@href").extract_first()
            content_url = response.urljoin(content_url)
            title = li.xpath('./a/@title').extract_first()
            issue_time = li.xpath('./span/text()').extract_first()


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

        # # 翻页操作
        # for num in range(2, 11):
        #     next_page = "https://news.bjx.com.cn/zt.asp?topic=%c4%da%c3%c9%b9%c5%b7%e7%b5%e7&page={0}".format(num)
        #     yield scrapy.Request(url=next_page, callback=self.parse)

    def detail_parse(self, response):
        try:
            source = response.xpath(
                '//div[@class="tempa list_copy btemp"]/b[1]/text() | //div[@class="tempa list_copy btemp"]/b[1]/a/text()').extract_first()
            if "来源" in source:
                source = source.split('来源:')[1] if source.split('来源:')[1] is not None and len(
                    source.split('来源:')[1]) != 0 else self.web_name
            else:
                source = source if source is not None and len(source) != 0 else self.web_name
        except:
            source = self.web_name
        try:
            author = response.xpath('/html/body/div[3]/div[1]/div[1]/div[1]/text()[2]').extract_first()
            author = author.split('作者:')[1].strip()
        except:
            author = None

        # 固定模式，改下xpath即可
        content = response.xpath('//div[@class="list_left"]').extract()
        content = ''.join(content)  # 转化成字符串，并且去掉空格

        # 处理图片的通用格式:
        # _xpath1 = '//div[@id="fontzoom"]//img/@src'  # 改下xpath即可
        # images = response.xpath(_xpath1).extract()
        # 处理附件的通用格式
        # _xpath2 = '//*[@class="qt-attachments-list"]//a/@href'  # 改下xpath即可
        # attachments = response.xpath(_xpath2).extract()
        attachments = None
        images = None

        # 使用自定义的函数upload_and_replace来处理图片和附件和内容
        content, images = ur.upload_and_replace(content, images, response)
        content, attachments = ur.upload_and_replace(content, attachments, response)

        # 以下除了item["information_categories"]不固定，其余的全部固定！！！
        item = response.meta["item"]
        item["tags"] = None
        item["information_categories"] = "协会动态"  # 协会动态/行业标准等
        item["news_id"] = response.meta["news_id"]  # id
        item['area'] = None
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
    os.system('scrapy crawl nmgxh_info')  ##改下爬虫名




