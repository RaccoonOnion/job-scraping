import json
import scrapy
import os
from jobs_project.items import JobsProjectItem
from datetime import datetime

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    start_urls = [
        f'file://{os.path.abspath(os.path.join("jobs_project", "data", "s01.json"))}',
        f'file://{os.path.abspath(os.path.join("jobs_project", "data", "s02.json"))}',
    ]

    def parse(self, response):
        source_file = response.url.split('/')[-1]
        self.logger.info(f"Processing file: {source_file}")
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from {source_file}: {e}")
            return

        if 'jobs' not in data or not isinstance(data.get('jobs'), list):
             self.logger.error(f"'jobs' key not found or not a list in {source_file}")
             return

        for job_entry in data.get('jobs', []):
             if 'data' in job_entry:
                job_data = job_entry['data']
                item = JobsProjectItem()

                # --- Populate standard fields ---
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
                item['source_file'] = source_file # Store which file it came from

                # --- Parse and assign date fields ---
                create_date_str = job_data.get('create_date')
                update_date_str = job_data.get('update_date')

                # Define the expected format string including timezone
                # %z handles formats like +0000 or -0500
                date_format = "%Y-%m-%dT%H:%M:%S%z"

                try:
                    if create_date_str:
                        # Use strptime with the defined format
                        item['create_date'] = datetime.strptime(create_date_str, date_format)
                    else:
                        item['create_date'] = None # Handle missing dates
                except (ValueError, TypeError) as e:
                    # Log the specific string and error
                    self.logger.warning(f"Could not parse create_date '{create_date_str}' with format '{date_format}': {e}")
                    item['create_date'] = None # Assign None if parsing fails

                try:
                    if update_date_str:
                        # Use strptime with the defined format
                        item['update_date'] = datetime.strptime(update_date_str, date_format)
                    else:
                        item['update_date'] = None
                except (ValueError, TypeError) as e:
                    # Log the specific string and error
                    self.logger.warning(f"Could not parse update_date '{update_date_str}' with format '{date_format}': {e}")
                    item['update_date'] = None

                # --- Yield the item ---
                yield item
             else:
                self.logger.warning(f"Skipping job entry in {source_file} due to missing 'data' key: {job_entry}")