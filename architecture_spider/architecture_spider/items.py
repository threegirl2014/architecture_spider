# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArchitectureItem(scrapy.Item):
    url = scrapy.Field()
    site = scrapy.Field()
    document_id = scrapy.Field()

    name = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
