# Job Scraping Pipeline Project

## Introduction

This project implements a data ingestion pipeline using Scrapy, MongoDB, and Docker Compose. The goal is to scrape job data from local JSON files, store it in a MongoDB database, and provide a script to query the stored data and export it to a CSV file. This project fulfills the requirements outlined in the Software Engineer Take Home Project description.

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
3.  **Environment Variables:** Configure the necessary environment variables for database connections. You can either:
    * **Create a `.env` file:** Create a file named `.env` in the `job-scraping` root directory with the following content:
        ```dotenv
        MONGO_URI=mongodb://mongo:27017/
        MONGO_DB_NAME=jobs_db
        MONGO_COLLECTION=raw_jobs
        # Add REDIS_URL=redis://redis:6379 if using Redis
        ```
    * **Modify `docker-compose.yaml`:** Alternatively, set these variables directly under the `environment:` section for the `app` service in the `docker-compose.yaml` file.

## Running the Project

All commands should be run from the root `job-scraping` directory in your terminal.

1.  **Build and Start Containers:**
    This command builds the Scrapy application image (if not already built or if `Dockerfile` changed) and starts the `app` and `mongo` (and optionally `redis`) services in detached mode.
    ```bash
    docker-compose up --build -d
    ```

2.  **Run the Scrapy Spider:**
    This executes the `job_spider` inside the running `app` container. The spider reads data from the JSON files, processes it through the pipeline(s), and stores it in MongoDB.
    ```bash
    docker-compose exec app bash -c "cd jobs_project && scrapy crawl job_spider"
    ```
    *(You can monitor the progress by checking the logs - see below)*

3.  **Run the Query Script:**
    This executes the `query.py` script inside the `app` container. It connects to MongoDB, fetches the stored job data, and exports it to a CSV file (`final_jobs.csv` or similar, depending on your script's implementation) in the `job-scraping` root directory.
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

5.  **Access MongoDB Shell (Optional):**
    You can directly interact with the MongoDB database running inside the container:
    ```bash
    docker-compose exec mongo mongosh
    ```
    Inside the shell, you can use commands like:
    * `use jobs_db;` (or your configured DB name)
    * `db.raw_jobs.find().pretty();` (or your configured collection name)
    * `exit`

6.  **Stop Containers:**
    When finished, stop and remove the containers, networks, and volumes defined in the `docker-compose.yaml`.
    ```bash
    docker-compose down
    ```
    **Caution:** To also remove the persistent MongoDB data volume (useful for a clean start), use:
    ```bash
    docker-compose down -v
    ```

## Output

* The primary output of the `query.py` script is a CSV file (e.g., `final_jobs.csv`) generated in the project's root directory, containing the job data fetched from MongoDB.

## Redis Implementation (Optional)

TBD

## Demo Video Requirement

TBD