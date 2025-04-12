# In query.py
import csv
import os
import argparse # <-- Import argparse
from infra.mongodb_connector import MongoDBConnector
from datetime import datetime

def export_jobs_to_csv(args):
    """
    Connects to MongoDB, fetches job data based on command-line arguments,
    and exports it to a CSV file.
    """
    print("Connecting to MongoDB...")
    connector = None # Initialize connector to None
    try:
        connector = MongoDBConnector()
        collection_name = os.environ.get('MONGO_COLLECTION', 'raw_jobs')
        print(f"Fetching data from collection: {collection_name}")

        # --- Determine Query, Projection, Headers based on args ---
        mongo_query = {}
        mongo_projection = None
        output_filename = args.output if args.output else 'final_jobs.csv' # Use provided filename or default
        headers = [] # Initialize empty headers list

        print(f"\nExecuting query type: {args.query_type}")

        if args.query_type == 'all':
            print("Query: Fetching all documents, all fields.")
            jobs_data = connector.find_all(collection_name) # Query = {} implicitly
            # Define headers for 'all' - should match your Item fields
            headers = [
                '_id', 'req_id', 'title', 'description',
                'street_address', 'city', 'state', 'country_code', 'postal_code',
                'latitude', 'longitude', 'apply_url', 'update_date',
                'create_date', 'source_file' # Adjust as per your items.py
            ]
            if not args.output: # If no output filename specified, use a default for this query type
                 output_filename = 'final_all_jobs.csv'

        elif args.query_type == 'state':
            if not args.state:
                print("Error: --state argument is required for query type 'state'")
                return
            target_state = args.state
            print(f"Query: Fetching all fields for state: {target_state}")
            mongo_query = {'state': target_state}
            # Example using the specific reusable method:
            # jobs_data = connector.find_jobs_by_state(collection_name, target_state)
            # Or using the generic find_all:
            jobs_data = connector.find_all(collection_name, query=mongo_query)
            # Define headers for 'state' (same as 'all' in this case)
            headers = [
                '_id', 'req_id', 'title', 'description',
                'street_address', 'city', 'state', 'country_code', 'postal_code',
                'latitude', 'longitude', 'apply_url', 'update_date',
                'create_date', 'source_file' # Adjust as per your items.py
            ]
            if not args.output:
                 output_filename = f'final_{target_state.lower()}_jobs.csv'


        elif args.query_type == 'state_partial':
            if not args.state:
                print("Error: --state argument is required for query type 'state_partial'")
                return
            target_state = args.state
            print(f"Query: Fetching Title, City, State for state: {target_state}")
            mongo_query = {'state': target_state}
            mongo_projection = {'title': 1, 'city': 1, 'state': 1, '_id': 0}
            jobs_data = connector.find_all(
                collection_name,
                query=mongo_query,
                projection=mongo_projection
            )
            # Define headers explicitly matching the projection
            headers = ['title', 'city', 'state']
            if not args.output:
                 output_filename = f'final_{target_state.lower()}_jobs_partial.csv'

        else:
            print(f"Error: Unknown query type '{args.query_type}'")
            return

        # --- Proceed with CSV Export ---
        if not jobs_data:
            print("No data matched the query criteria.")
            return

        print(f"Fetched {len(jobs_data)} documents.")
        print(f"Exporting selected data to {output_filename}...")

        if not headers:
             print("Error: CSV headers were not defined for the selected query.")
             return

        try:
            with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
                # Use DictWriter - handles missing keys if 'ignore' is used
                writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore')
                writer.writeheader()
                for job in jobs_data:
                    # Ensure date fields are formatted nicely for CSV if they are datetime objects
                    # This assumes date parsing was done in the spider
                    if 'create_date' in job and isinstance(job['create_date'], datetime):
                         job['create_date'] = job['create_date'].isoformat()
                    if 'update_date' in job and isinstance(job['update_date'], datetime):
                         job['update_date'] = job['update_date'].isoformat()
                    writer.writerow(job)
            print(f"Successfully exported data to {output_filename}")
        except IOError as e:
             print(f"Error writing CSV file: {e}")
        except Exception as e:
             print(f"An unexpected error occurred during CSV export: {e}")

    except ConnectionError as e:
        print(f"Database connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure connection is closed if it was opened
        if connector:
            print("Closing MongoDB connection.")
            connector.close_connection()

if __name__ == "__main__":
    # --- Argument Parsing Setup ---
    parser = argparse.ArgumentParser(description="Query MongoDB job data and export to CSV.")

    parser.add_argument(
        '--query-type',
        type=str,
        default='all', # Default to fetching all if not specified
        choices=['all', 'state', 'state_partial'], # Allowed query types
        help="Type of query to execute ('all', 'state', 'state_partial'). Default: 'all'."
    )
    parser.add_argument(
        '--state',
        type=str,
        help="Specify the state to filter by (required for query types 'state' and 'state_partial')."
    )
    parser.add_argument(
        '--output',
        type=str,
        help="Optional: Specify the output CSV filename."
    )

    # Parse arguments
    args = parser.parse_args()

    # Run the export function with parsed arguments
    export_jobs_to_csv(args)