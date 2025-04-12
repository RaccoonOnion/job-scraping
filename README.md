# Job Scraping Pipeline Project

## Demo Video

* **Link:** [YouTube Video Demo: Check it out!](https://youtu.be/kXQI1XvLFTc)

*(Please replace the placeholder above with the actual link to your ~2 minute demo video as required by the project description*

## Introduction

This project implements a data ingestion pipeline using Scrapy, MongoDB, Redis, and Docker Compose. The goal is to scrape job data from local JSON files, deduplicate items using Redis, store the unique data in a MongoDB database, and provide a script to query the stored data and export it to a CSV file.

## Project Structure

```
job-scraping
├─ .dockerignore
├─ Dockerfile
├─ LICENSE
├─ README.md
├─ docker compose.yaml
├─ docker-logs
│  └─ app
│     ├─ scrapy.log
├─ infra
│  ├─ mongodb_connector.py
│  └─ redis_connector.py
├─ jobs_project
│  ├─ jobs_project
│  │  ├─ __init__.py
│  │  ├─ data
│  │  │  ├─ s01.json
│  │  │  └─ s02.json
│  │  ├─ items.py
│  │  ├─ middlewares.py
│  │  ├─ pipelines.py
│  │  ├─ settings.py
│  │  └─ spiders
│  │     ├─ __init__.py
│  │     └─ json_spider.py
│  └─ scrapy.cfg
├─ logs
├─ query.py
└─ requirements.txt

```

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1.  **Clone/Download:** Obtain the project files.     
    ```bash
    git clone https://github.com/RaccoonOnion/job-scraping.git
    ```
2.  **Place Data Files:** Ensure the input JSON files (`s01.json`, `s02.json`) are located within the `job-scraping/jobs_project/jobs_project/data/` directory.
3.  **Environment Variables:** Configure the necessary environment variables for database and cache connections. You can either:
    * **Create a `.env` file:** Create a file named `.env` in the `job-scraping` root directory with the following content:
        ```dotenv
        MONGO_URI=mongodb://mongo:27017/
        MONGO_DB_NAME=jobs_db
        MONGO_COLLECTION=raw_jobs
        REDIS_URL=redis://redis:6379/0
        # Optional: Define a custom Redis key for deduplication
        # REDIS_SET_KEY=my_custom_job_ids
        ```
    * **Modify `docker compose.yaml`:** Alternatively, set these variables directly under the `environment:` section for the `app` service in the `docker compose.yaml` file. (`REDIS_SET_KEY` is optional as a default is provided in `pipelines.py`).

## Infrastructure Overview

This project utilizes Docker Compose to orchestrate three main services:

1.  **`app` (Scrapy Service):**
    * Builds from the `Dockerfile`.
    * Contains the Scrapy project (`jobs_project`) including spiders, items, and pipelines.
    * Responsible for running the `job_spider` to read local JSON data.
    * Connects to Redis for deduplication and MongoDB for storage via the pipelines.
    * Also runs the `query.py` script for data export.

2.  **`mongo` (MongoDB Service):**
    * Uses the official `mongo:latest` image.
    * Acts as the primary data store.
    * Receives unique job items from the `app` service's `MongoPipeline`.
    * Persists data using a named volume (`mongo_data`).

3.  **`redis` (Redis Service):**
    * Uses the official `redis:latest` image.
    * Acts as an in-memory cache/data structure store.
    * Used by the `RedisDeduplicationPipeline` in the `app` service to store unique item IDs (`req_id`) in a Set, preventing duplicate items from being processed and stored in MongoDB across multiple spider runs.
    * Persists data using a named volume (`redis_data`) (Optional, depending on `docker compose.yaml` configuration).


## Error Handling Overview

Error handling is implemented at various stages:

* **Spider (`json_spider.py`):**
    * Handles `FileNotFoundError` (via Scrapy) and `json.JSONDecodeError` during file loading.
    * Validates basic data structure (presence of `jobs` list, `data` object within jobs).
    * Safely parses date strings using `try...except`, logging warnings on failure and setting fields to `None`.
* **Connectors (`infra/`):**
    * Catch specific connection errors (`pymongo.errors.ConnectionFailure`, `redis.exceptions.ConnectionError`) during initialization and report failure (raising `ConnectionError` or setting client to `None`).
    * Catch general exceptions during database/cache operations (e.g., insert, find, check), log them, and typically return default values (could be improved by raising specific exceptions).
* **Pipelines (`pipelines.py`):**
    * Handle connector initialization failures in `open_spider` by setting connector instances to `None` and logging errors.
    * Check if connectors are available in `process_item` before attempting operations. If Redis is unavailable, deduplication is skipped (item passes through). If MongoDB is unavailable, storage fails, and an error is logged (item might be dropped depending on latest implementation).
    * Uses Scrapy's `DropItem` exception in the Redis pipeline to stop processing duplicate items.
    * Handles potential `None` return from `mongodb_connector.insert_item` (if insertion failed internally in the connector).
* **Query Script (`query.py`):**
    * Uses a main `try...except` block to catch `ConnectionError` and general `Exception`.
    * Specifically handles `IOError` during CSV file writing.
    * Validates required command-line arguments (e.g., `--state`).
    * Uses a `finally` block to ensure the MongoDB connection is closed.

## Running the Project

All commands should be run from the root `job-scraping` directory in your terminal.

1.  **Build and Start Containers:**
    ```bash
    docker compose up --build -d
    ```

2.  **Run the Scrapy Spider:**
    ```bash
    docker compose exec app bash -c "cd jobs_project && scrapy crawl job_spider"
    ```
    *(Check logs/screen output for processing and deduplication messages.)*

3.  **Run the Query Script (with Arguments):**
    Use command-line arguments to control the query and output.
    * **Default (Fetch all data, full fields):** Outputs to `final_all_jobs.csv`.
        ```bash
        docker compose exec app python query.py
        ```
        *(Or explicitly: `docker compose exec app python query.py --query-type all`)*
    * **Fetch only jobs from a specific state (e.g., Georgia):** Outputs to `final_georgia_jobs.csv`.
        ```bash
        docker compose exec app python query.py --query-type state --state Georgia
        ```
    * **Fetch partial data (Title, City, State) for a specific state (e.g., Alabama):** Outputs to `final_alabama_jobs_partial.csv`.
        ```bash
        docker compose exec app python query.py --query-type state_partial --state Alabama
        ```
    * **Specify Output Filename:**
        ```bash
        docker compose exec app python query.py --query-type state --state Alabama --output custom_alabama_export.csv
        ```
    *(Check the terminal output for confirmation and look for the generated CSV file in the project root.)*

4.  **Check Logs (Optional):**
    * `docker compose logs app`
    * `docker compose logs mongo`
    * `docker compose logs redis`

5.  **Check Databases (Optional):**
    * **MongoDB:**
        ```bash
        docker compose exec mongo mongosh
        ```
        Inside the shell:
        ```mongodb
        use jobs_db; // Or your configured DB name
        db.raw_jobs.countDocuments(); // Or your configured collection name
        db.raw_jobs.findOne();
        exit
        ```
    * **Redis:**
        ```bash
        docker compose exec redis redis-cli
        ```
        Inside the shell: `SCARD processed_job_ids` (or your custom `REDIS_SET_KEY`), `exit`

6.  **Stop Containers:**
    ```bash
    docker compose down
    ```
    *(Use `docker compose down -v` to also remove data volumes for a clean start.)*

## Output

* The primary output of the `query.py` script is a CSV file (e.g., `final_all_jobs.csv`, `final_georgia_jobs.csv`, etc.) generated in the project's root directory, containing the job data fetched from MongoDB based on the query arguments.
* Redis stores the set of processed `req_id`s for deduplication across runs.