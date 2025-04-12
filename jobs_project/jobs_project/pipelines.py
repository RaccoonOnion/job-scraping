# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import sys
from pymongo.errors import PyMongoError

# Add the root folder to the path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))) not necessary in docker
from infra.mongodb_connector import MongoDBConnector
from infra.redis_connector import RedisConnector
from scrapy.exceptions import DropItem

class RedisDeduplicationPipeline:
    """Pipeline for filtering out items seen in previous crawls using Redis."""

    redis_set_key = os.environ.get('REDIS_SET_KEY', 'processed_job_ids') # Redis set name

    def open_spider(self, spider):
        spider.logger.info("Opening Redis connection for deduplication pipeline.")
        try:
            self.connector = RedisConnector()
            if not self.connector.client: # Check if connection failed in __init__
                 spider.logger.warning("Redis client not available in deduplication pipeline. Deduplication disabled.")
                 self.connector = None # Ensure it's None to skip processing
        except ConnectionError as e:
             spider.logger.error(f"Failed to open Redis connection: {e}")
             self.connector = None

    def close_spider(self, spider):
         spider.logger.info("Closing Redis connection for deduplication pipeline.")
         if self.connector:
            self.connector.close_connection()

    def process_item(self, item, spider):
        if not self.connector:
            spider.logger.debug("Redis connector not available, skipping deduplication.")
            return item # Pass item through if Redis isn't working

        adapter = ItemAdapter(item)
        item_id = adapter.get('req_id') # Use 'req_id' or another unique field

        if not item_id:
            spider.logger.warning(f"Item missing unique ID ('req_id'): {item}. Cannot perform deduplication.")
            return item # Pass through items without an ID

        # Check if item ID exists in the Redis set
        already_processed = self.connector.check_if_exists(self.redis_set_key, item_id)

        if already_processed:
            spider.logger.info(f"Item already processed (found in Redis): {item_id}")
            raise DropItem(f"Duplicate item found: {item_id}")
        else:
            # Add item ID to Redis set and pass item to next pipeline
            self.connector.add_item(self.redis_set_key, item_id)
            spider.logger.debug(f"Added item to Redis set: {item_id}")
            return item


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
        if not self.connector:
            spider.logger.error("MongoDB connector not available. Dropping item.")
            raise DropItem("Item skipped: MongoDB connection unavailable") # Make failure explicit

        adapter = ItemAdapter(item)
        item_dict = adapter.asdict()

        # Optional: Add basic validation here
        if not adapter.get('title') or not adapter.get('req_id'):
             spider.logger.warning(f"Item missing required fields (title or req_id): {adapter.get('req_id')}")
             raise DropItem("Missing required fields for MongoDB storage")

        try:
            insert_result = self.connector.insert_item(self.collection_name, item_dict)
            # Connector would raise exception on failure now, so no need to check return value 'None' explicitly for errors
            spider.logger.info(f"Item inserted for req_id: {item_dict.get('req_id')}")

        except PyMongoError as e: # Catch specific DB errors
            spider.logger.error(f"MongoDB insertion failed for req_id {item_dict.get('req_id')}: {e}")
            raise DropItem(f"MongoDB insertion failed: {e}") # Drop item on DB error
        except Exception as e: # Catch unexpected errors
             spider.logger.critical(f"Unexpected error during MongoDB insertion for req_id {item_dict.get('req_id')}: {e}", exc_info=True)
             raise DropItem(f"Unexpected error during MongoDB insertion: {e}") # Or maybe CloseSpider

        return item
