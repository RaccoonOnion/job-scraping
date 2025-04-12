# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    req_id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    # location_name = scrapy.Field() not common
    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    country_code = scrapy.Field()
    postal_code = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    apply_url = scrapy.Field()
    # Add any other fields you need from the 'data' object
    # Example: dates - you might need to parse these later in the pipeline
    update_date = scrapy.Field()
    create_date = scrapy.Field()
    # You can also store the source file if needed
    source_file = scrapy.Field()
