# In query.py
import csv
import os
from infra.mongodb_connector import MongoDBConnector
from datetime import datetime # Optional: If you want to timestamp the filename

def export_jobs_to_csv():
    """
    Connects to MongoDB, fetches job data, and exports it to a CSV file.
    """
    print("Connecting to MongoDB...")
    try:
        connector = MongoDBConnector()
        collection_name = os.environ.get('MONGO_COLLECTION', 'raw_jobs')
        print(f"Fetching data from collection: {collection_name}")

        # --- Example 1: Fetch ALL data (using the reusable find_all) ---
        print(f"Fetching ALL data from collection: {collection_name}")
        all_jobs_data = connector.find_all(collection_name)
        print(f"Fetched {len(all_jobs_data)} total documents.")
        # You could export this to 'all_jobs.csv' for demonstration


        # --- Example 2: Fetch only jobs from 'Georgia' (Filter) ---
        target_state = 'Georgia'
        print(f"\nFetching only jobs from {target_state}...")
        georgia_query = {'state': target_state}
        georgia_jobs_data = connector.find_all(collection_name, query=georgia_query)
        print(f"Fetched {len(georgia_jobs_data)} documents for {target_state}.")
        # You could export this to 'georgia_jobs.csv'


        # --- Example 3: Fetch only jobs from 'Georgia' (using specific reusable method) ---
        print(f"\nFetching only jobs from {target_state} using specific method...")
        georgia_jobs_data_reusable = connector.find_jobs_by_state(collection_name, target_state)
        print(f"Fetched {len(georgia_jobs_data_reusable)} documents for {target_state} via reusable method.")
        # This data should be the same as Example 2


        # --- Example 4: Fetch only Title, City, State for Georgia jobs (Filter + Projection) ---
        print(f"\nFetching specific fields (Title, City, State) for {target_state} jobs...")
        georgia_projection = {
            'title': 1,      # Include title field
            'city': 1,       # Include city field
            'state': 1,      # Include state field
            '_id': 0         # Exclude the default _id field
        }
        partial_georgia_jobs_data = connector.find_all(
            collection_name,
            query=georgia_query,
            projection=georgia_projection
        )
        print(f"Fetched {len(partial_georgia_jobs_data)} partial documents for {target_state}.")

        # --- CSV Export (Choose which data you want to export) ---
        # Decide which dataset you want to write to final_jobs.csv
        # Let's export the partial georgia data for this example
        jobs_to_export = partial_georgia_jobs_data
        output_filename = 'final_georgia_jobs_partial.csv' # Adjust filename maybe

        if not jobs_to_export:
            print("No data selected for export.")
            # Close connection and return if needed
            # connector.close_connection()
            # return
        else:
            print(f"\nExporting selected data ({len(jobs_to_export)} documents) to {output_filename}...")
            # Define headers EXPLICITLY based on your projection
            headers = ['title', 'city', 'state'] # Must match the keys included in the projection

            try:
                with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    # Use DictWriter - it handles missing keys if a doc is different
                    writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore')
                    writer.writeheader()
                    for job in jobs_to_export:
                        writer.writerow(job)
                print(f"Successfully exported data to {output_filename}")
            except IOError as e:
                 print(f"Error writing CSV file: {e}")
            except Exception as e:
                 print(f"An unexpected error occurred during CSV export: {e}")


        # Fetch all documents using the connector's method
        # Add projection={} if you only want specific fields
        # jobs_data = connector.find_all(collection_name)

        # if not jobs_data:
        #     print("No data found in MongoDB collection.")
        #     return

        # print(f"Fetched {len(jobs_data)} documents.")

        # --- CSV Export ---
        # output_filename = 'final_jobs.csv'
        # print(f"Exporting data to {output_filename}...")

        # Define CSV headers - Use keys from your JobsProjectItem or MongoDB docs
        # It's good practice to get headers dynamically or define them explicitly
        # Let's try getting them from the first document, assuming all docs have similar structure
        # if jobs_data:
        #     # Be careful: MongoDB documents might not have consistent fields!
        #     # It's safer to define headers explicitly based on your Item definition.
        #     # Example explicit headers (adjust based on your items.py):
        #     headers = [
        #         '_id', # MongoDB default ID
        #         'req_id',
        #         'title',
        #         'description',
        #         # 'location_name',
        #         'street_address',
        #         'city',
        #         'state',
        #         'country_code',
        #         'postal_code',
        #         'latitude',
        #         'longitude',
        #         'apply_url',
        #         'update_date',
        #         'create_date',
        #         'source_file'
        #         # Add all other fields from your JobsProjectItem
        #     ]
            # Fallback in case the first document is missing many keys:
            # headers = list(jobs_data[0].keys())


            # try:
            #     with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            #         writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore') # 'ignore' skips fields not in headers

            #         writer.writeheader()
            #         for job in jobs_data:
            #             writer.writerow(job)

            #     print(f"Successfully exported data to {output_filename}")

            # except IOError as e:
            #      print(f"Error writing CSV file: {e}")
            # except Exception as e:
            #      print(f"An unexpected error occurred during CSV export: {e}")

        # else:
        #      print("No data fetched, CSV file not created.")


    except ConnectionError as e:
        print(f"Database connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure connection is closed if it was opened
        if 'connector' in locals() and connector:
            print("Closing MongoDB connection.")
            connector.close_connection()

if __name__ == "__main__":
    export_jobs_to_csv()