# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'mongodb://localhost:27017'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'scrapy_db'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION', 'movies')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]
        self.collection.create_index("id", unique=True)  # 用 id 去重

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            print(f"正在处理 item: {item.get('id')}")
            self.collection.update_one({"id": item["id"]}, {"$set": dict(item)}, upsert=True)
            spider.logger.info(f"insert succeed: {item['id']}")
        except pymongo.errors.DuplicateKeyError:
            spider.logger.info(f"Duplicate item found: {item['id']}")
        return item
