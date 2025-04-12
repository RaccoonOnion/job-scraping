import json
import os
import scrapy
from jobs_project.items import JobsProjectItem


class JobSpider(scrapy.Spider):
    name = 'job_spider'
    # custom_settings should point to your actual pipeline class name in pipelines.py
    # We'll define this properly later. For now, you can comment it out or leave as is.
    # custom_settings = {
    #    'ITEM_PIPELINES': {'jobs_project.pipelines.MongoPipeline': 300},
    # }


    start_urls = [
        f'file://{os.path.abspath(os.path.join("jobs_project", "data", "s01.json"))}',
        f'file://{os.path.abspath(os.path.join("jobs_project", "data", "s02.json"))}',
    ]

    # Scrapy uses start_urls class attribute in its default start_requests 
    # method to automatically generate the initial requests, 
    # calling the parse method for each response.

    def parse(self, response):
        # Extract the source filename from the URL for reference
        source_file = response.url.split('/')[-1]
        self.logger.info(f"Processing file: {source_file}")

        try:
            # Load the JSON data from the response body
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from {source_file}: {e}")
            return # Stop processing this file if JSON is invalid we could improve this?

        # Check if 'jobs' key exists and is a list
        if 'jobs' not in data or not isinstance(data.get('jobs'), list):
             self.logger.error(f"'jobs' key not found or not a list in {source_file}")
             return # Stop processing this file

        # Loop over each job entry in the 'jobs' array
        for job_entry in data.get('jobs', []):
             # Check if 'data' key exists within the job entry
             if 'data' in job_entry:
                job_data = job_entry['data']
                item = JobsProjectItem()

                # Populate the item fields from the job_data dictionary
                # Use .get(key, default_value) to avoid errors if a key is missing
                item['req_id'] = job_data.get('req_id')
                item['title'] = job_data.get('title')
                item['description'] = job_data.get('description')
                # item['location_name'] = job_data.get('location_name') not common
                item['street_address'] = job_data.get('street_address')
                item['city'] = job_data.get('city')
                item['state'] = job_data.get('state')
                item['country_code'] = job_data.get('country_code')
                item['postal_code'] = job_data.get('postal_code')
                item['latitude'] = job_data.get('latitude')
                item['longitude'] = job_data.get('longitude')
                item['apply_url'] = job_data.get('apply_url')
                item['update_date'] = job_data.get('update_date')
                item['create_date'] = job_data.get('create_date')
                item['source_file'] = source_file # Store which file it came from

                # Yield the populated item
                yield item
             else:
                self.logger.warning(f"Skipping job entry in {source_file} due to missing 'data' key: {job_entry}")