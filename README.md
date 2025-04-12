# Job Scraping Pipeline Project

## Introduction

This project implements a data ingestion pipeline using Scrapy, MongoDB, Redis, and Docker Compose. The goal is to scrape job data from local JSON files, deduplicate items using Redis, store the unique data in a MongoDB database, and provide a script to query the stored data and export it to a CSV file. This project fulfills the requirements outlined in the Software Engineer Take Home Project description 

## Project Structure
```
job-scraping
├─ .dockerignore
├─ Dockerfile
├─ LICENSE
├─ README.md
├─ docker-compose.yaml
├─ final_georgia_jobs_partial.csv
├─ find_common.py
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
├─ query.py
└─ requirements.txt

```

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1.  **Clone/Download:** Obtain the project files.
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
    * **Modify `docker-compose.yaml`:** Alternatively, set these variables directly under the `environment:` section for the `app` service in the `docker-compose.yaml` file. (Note: `REDIS_SET_KEY` is optional as a default is provided in `pipelines.py`).

## Running the Project

All commands should be run from the root `job-scraping` directory in your terminal.

1.  **Build and Start Containers:**
    This command builds the Scrapy application image (if not already built or if `Dockerfile`/`requirements.txt` changed) and starts the `app`, `mongo`, and `redis` services in detached mode.
    ```bash
    docker-compose up --build -d
    ```

2.  **Run the Scrapy Spider:**
    This executes the `job_spider` inside the running `app` container. The spider reads data, passes items through the Redis deduplication pipeline (dropping seen items), and then stores unique items in MongoDB via the MongoDB pipeline.
    ```bash
    docker-compose exec app bash -c "cd jobs_project && scrapy crawl job_spider"
    ```
    * **First Run:** Expect to see logs indicating items being added to Redis and then inserted into MongoDB.
    * **Subsequent Runs:** Expect to see logs indicating items are found in Redis and dropped, with few or no new insertions into MongoDB.

3.  **Run the Query Script:**
    This executes the `query.py` script inside the `app` container. It connects to MongoDB, fetches the stored unique job data, and exports it to a CSV file (e.g., `final_jobs.csv`) in the `job-scraping` root directory.
    ```bash
    docker-compose exec app python query.py
    ```
    *(Check the terminal output for confirmation messages and look for the generated CSV file in the project root.)*

4.  **Check Logs (Optional):**
    * View logs from the Scrapy application:
        ```bash
        docker-compose logs app
        ```
    * View logs from the MongoDB service:
        ```bash
        docker-compose logs mongo
        ```
    * View logs from the Redis service:
        ```bash
        docker-compose logs redis
        ```

5.  **Check Databases (Optional):**
    * **Access MongoDB Shell:**
        ```bash
        docker-compose exec mongo mongosh
        ```
        Inside the shell: `use jobs_db;`, `db.raw_jobs.countDocuments();`, `exit`
    * **Access Redis CLI:**
        ```bash
        docker-compose exec redis redis-cli
        ```
        Inside the shell: `SCARD processed_job_ids` (or your custom `REDIS_SET_KEY`), `exit`

6.  **Stop Containers:**
    When finished, stop and remove the containers, networks, and volumes.
    ```bash
    docker-compose down
    ```
    **Caution:** To also remove the persistent MongoDB and Redis data volumes (useful for a completely clean start), use:
    ```bash
    docker-compose down -v
    ```

## Output

* The primary output of the `query.py` script is a CSV file (e.g., `final_jobs.csv`) generated in the project's root directory, containing the unique job data fetched from MongoDB.
* Redis stores the set of processed `req_id`s for deduplication across runs (data persists in a volume unless removed with `docker-compose down -v`).

## Demo Video Requirement

TBD