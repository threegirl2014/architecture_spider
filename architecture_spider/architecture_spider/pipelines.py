# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymongo
from pymongo.errors import WriteError
from .items import ArchitectureItem

logger = logging.getLogger(__name__)


class ArchitectureSpiderPipeline(object):

    collection_name = 'architecture_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[self.collection_name].create_index([('document_id', pymongo.ASCENDING),
                                                    ('date', pymongo.ASCENDING)],
                                                   unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ArchitectureItem):
            try:
                self.db[self.collection_name].insert_one(dict(item))
            except WriteError, e:  # DuplicateKeyError
                logger.warn('---- duplicate ----: {}'.format(item['url']))
        return item
