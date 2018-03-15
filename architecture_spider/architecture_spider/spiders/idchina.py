# -*- coding: utf-8 -*-

import logging
import scrapy
try:
    import simplejson as json
except ImportError:
    import json

from ..items import ArchitectureItem
from ..utils import md5

logger = logging.getLogger(__name__)


class IdchinaSpider(scrapy.Spider):
    name = 'idchina'
    base_url = 'http://mixinfo.id-china.com.cn'
    allowed_domains = ['id-china.com.cn']
    start_urls = ['http://mixinfo.id-china.com.cn/col-2-1.html', ]

    def parse(self, response):
        docs = response.xpath('//div[@id="left"]/div[@id="infolist"]/ul/li')
        for doc in docs:
            item = ArchitectureItem()
            url = doc.xpath('a/@href').extract_first()
            category = doc.xpath('em/a/text()').extract_first()
            item['url'] = self.base_url + url
            item['site'] = self.base_url
            item['category'] = category
            item['document_id'] = md5(url)
            req = scrapy.Request(self.base_url + url, callback=self.parse_doc, meta={'item': item, 'page': 1})
            yield req
        next_page = response.xpath('//div[@id="left"]/div[@class="pages"]/a')[-1]
        text = next_page.xpath('text()').extract_first()
        if u'下一页' in text:
            url = next_page.xpath('@href').extract_first()
            req = scrapy.Request(self.base_url + url, callback=self.parse)
            yield req

    def parse_doc(self, response):
        item = response.meta.get('item')
        page = response.meta.get('page', 1)
        info = response.xpath('//div[@id="left"]/div[@id="info"]')
#        logger.error( str(dir(item)))
        if not item.get('content', None):
            item['content'] = {}
            item['name'] = info.xpath('h3/text()').extract_first().strip()
            info_top = info.xpath('div[@class="info_top"]/p[@class="p_left"]/text()').extract_first().strip()
            date_index = info_top.find(u'时间:')
            source_index = info_top.find(u'来源:')
            if date_index > -1:
                item['date'] = info_top[date_index:].split()[-1]
            if source_index > -1:
                item['source'] = info_top[source_index:].split()[1]
        content = info.xpath('div[@id="info_nr"]/p')
        content_detail = self.get_content_detail(content)
        # ???
        item['content'].update({
            'page{}'.format(page): content_detail
        })
        next_page = info.xpath('div[@class="pages"]/a')
        if next_page:
            next_page = next_page[-1]
            text = next_page.xpath('text()').extract_first()
            if u'下一页' in text:
                url = next_page.xpath('@href').extract_first()
                page += 1
                req = scrapy.Request(self.base_url + url, callback=self.parse_doc, meta={'item': item, 'page': page})
                yield req
            else:
                yield item
        else:
            # ???
            item['content'] = json.dumps(item['content'])
            yield item

    def get_content_detail(self, content):
        result = []
        for item in content:
            text = item.xpath('text()').extract_first().strip()
            img = item.xpath('img').xpath('@src').extract_first()
            if text:
                result.append(text)
            if img:
                result.append(img)
        return result
