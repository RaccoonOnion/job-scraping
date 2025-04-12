# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import sys

# Add the root folder to the path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))) not necessary in docker
from infra.mongodb_connector import MongoDBConnector
class MongoPipeline:
    collection_name = os.environ.get('MONGO_COLLECTION', 'raw_jobs') # Collection name

    def open_spider(self, spider):
        spider.logger.info("Opening MongoDB connection for pipeline.")
        try:
            self.connector = MongoDBConnector()
        except ConnectionError as e:
            spider.logger.error(f"Failed to open MongoDB connection: {e}")
            # Optionally, you could raise DropItem or CloseSpider exception here
            # depending on how critical MongoDB is.
            self.connector = None # Ensure connector is None if connection failed

    def close_spider(self, spider):
         spider.logger.info("Closing MongoDB connection.")
         if self.connector:
            self.connector.close_connection()

    def process_item(self, item, spider):
        if self.connector:
            adapter = ItemAdapter(item)
            item_dict = adapter.asdict()
            # Insert the item using the connector's method
            insert_result = self.connector.insert_item(self.collection_name, item_dict)
            if insert_result is None:
                 spider.logger.warning(f"Item insertion failed or skipped for: {item_dict.get('req_id')}")
                 # Optionally raise DropItem here if insertion failure is critical
                 # from scrapy.exceptions import DropItem
                 # raise DropItem(f"Failed to insert item {item_dict.get('req_id')}")
            else:
                 spider.logger.info(f"Item inserted/handled for req_id: {item_dict.get('req_id')}")
        else:
             spider.logger.error("MongoDB connector not available. Cannot process item.")
             # Optionally raise DropItem here
        return item # Always return item for other pipelines
