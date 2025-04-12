# it's good practice to get the MongoDB URI from an environment variable (e.g., MONGO_URI=mongodb://mongo:27017/)

import pymongo
import os
from urllib.parse import quote_plus

class MongoDBConnector:
    def __init__(self):
        # It's better to get sensitive info like URI from environment variables
        # For docker-compose, you can define these in the compose file or an .env file
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://mongo:27017/') # Default if not set
        db_name = os.environ.get('MONGO_DB_NAME', 'jobs_db') # Choose a database name

        self.client = None
        self.db = None
        try:
            self.client = pymongo.MongoClient(mongo_uri)
            self.db = self.client[db_name]
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster') # As of MongoDB 4.2+, the 'ismaster' command is deprecated and replaced with 'hello', though many drivers (including PyMongo) still use 'ismaster' under the hood for backward compatibility
            print("MongoDB connection successful.")
        except pymongo.errors.ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            # Handle connection error appropriately - maybe raise an exception
            raise ConnectionError(f"Failed to connect to MongoDB at {mongo_uri}") from e
        except Exception as e:
             print(f"An error occurred during MongoDB connection: {e}")
             raise ConnectionError(f"An error occurred during MongoDB connection {mongo_uri}") from e


    def get_collection(self, collection_name):
        if self.db is not None:
             return self.db[collection_name]
        return None

    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

    # Add reusable query methods as needed per project doc
    def insert_item(self, collection_name, item_dict):
        collection = self.get_collection(collection_name)
        if collection is not None:
            try:
                # --- Remove the find_one check ---
                # if 'req_id' in item_dict and item_dict['req_id']:
                #    existing_item = collection.find_one({'req_id': item_dict['req_id']})
                #    if existing_item:
                #        print(f"Duplicate item skipped: {item_dict.get('req_id')}")
                #        return None # Indicate skipped duplicate
                #    else:
                #       result = collection.insert_one(item_dict) # Just insert
                #       print(f"Inserted item with ID: {result.inserted_id}")
                #       return result.inserted_id
                # else:
                #    print("Warning: Inserting item without a unique req_id for duplicate check.")
                #    result = collection.insert_one(item_dict) # Just insert
                #    print(f"Inserted item with ID: {result.inserted_id}")
                #    return result.inserted_id
                # --- End Remove ---

                # --- Simplified Logic: Just insert the dictionary ---
                result = collection.insert_one(item_dict)
                # Optional: Add logging back if desired, but no duplicate check needed here
                # print(f"Inserted item with ID: {result.inserted_id}")
                return result.inserted_id
                # --- End Simplified Logic ---

            except Exception as e:
                print(f"Error inserting item into {collection_name}: {e}")
                # Handle insertion error (log it, etc.)
                return None
        return None

    def find_all(self, collection_name, query={}, projection=None):
        """ Fetches documents matching the query, optionally projecting fields """
        collection = self.get_collection(collection_name)
        if collection is not None:
            try:
                # Apply projection if provided
                if projection is not None:
                    return list(collection.find(query, projection))
                else:
                    return list(collection.find(query)) # No projection
            except Exception as e:
                print(f"Error finding documents in {collection_name}: {e}")
                return []
        return []
    
    # Add a new specific reusable query method
    def find_jobs_by_state(self, collection_name, state):
        """ Reusable query to find jobs for a specific state """
        query = {'state': state}
        # Optionally add projection here if needed
        # projection = {'title': 1, 'city': 1, 'state': 1, '_id': 0}
        # return self.find_all(collection_name, query=query, projection=projection)
        return self.find_all(collection_name, query=query)