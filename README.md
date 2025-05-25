# lydia-data-engineer-ELT-pipeline
An ELT pipeline with Airbyte and DBT

This project implements an ELT (Extract, Load, Transform) pipeline to process cryptocurrency data, specifically focusing on Bitcoin prices from the CoinGecko API. It uses Apache Airflow for orchestration, DuckDB as the data warehouse, and dbt for transformations. The entire development and execution environment is managed using the Astronomer `astro` CLI.

## Objective

The primary goal is to extract hourly Bitcoin price data, load it into a DuckDB database, and transform it into a daily candlestick format (Open, High, Low, Close) suitable for analysis. This project demonstrates the ability to build and manage a modern data pipeline using industry-standard tools.

## Technology Stack

* **Orchestration:** Apache Airflow (Managed via Astronomer `astro` CLI)
* **Extraction:** Python (`pycoingecko` library)
* **Loading:** Python (`duckdb` library)
* **Database:** DuckDB
* **Transformation:** dbt (Data Build Tool)
* **Development Environment:** Docker, Astronomer `astro` CLI
* **Package Management:** UV (via `astro` and `requirements.txt`)

## Project Structure

* **lydia-data-engineer-ELT-pipeline/**
    * `.astro/`
        * `config.yaml`
    * `dags/`
        * `elt_pipeline_dag.py`
        * `exampledag.py`
    * `dbt_project/`
        * `models/`
            * `staging/`
            * `marts/`
        * `dbt_project.yml`
        * `profiles.yml`
    * `include/`
        * `extract.py`
        * `load.py`
        * `visualize.py`
        * `common_configs.py`
    * `data/`
    * `tests/`
    * `.gitignore`
    * `Dockerfile`
    * `Makefile`
    * `packages.txt`
    * `requirements.txt`
    * `README.md`

## Prerequisites

Before you begin, ensure you have the following installed on your system:

1.  **Git:** To clone the repository.
2.  **Docker Desktop:** Essential for running the `astro` CLI local environment.
3.  **Astro CLI:** Follow the [official installation instructions](https://www.astronomer.io/docs/astro/cli/install-cli). Make sure you can run `astro version`.

## Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone <REPOSITORY_URL>
    cd lydia-data-engineer-ELT-pipeline
    ```

2.  **Check `dbt_project/profiles.yml`:** Ensure the path to your DuckDB file is correct for the containerized environment. It should look like this, using a relative path from the `dbt_project` directory to the `data` directory:
    ```yaml
    crypto_pipeline:
      target: dev
      outputs:
        dev:
          type: duckdb
          path: ../data/crypto.duckdb # *Relative* path to the DB file
    ```

3.  **Check `requirements.txt`:** Ensure `pycoingecko`, `duckdb`, `dbt-duckdb`, `pandas`, `matplotlib`, `mplfinance` are listed. `make start` will install them.

4.  **Check DAG Paths:** Ensure paths in `elt_pipeline_dag.py` use *inside-container* paths (e.g., `/usr/local/airflow/include/extract.py`, `/usr/local/airflow/dbt_project`).

## Running the Pipeline with Astro CLI

1.  **Start the Airflow Environment:** Navigate to the project root and run:
    ```bash
    make start
    ```
    This command builds your project into a Docker image (installing dependencies from `requirements.txt` and `packages.txt`) and starts the Airflow containers (webserver, scheduler, triggerer, database).

2.  **Access Airflow UI:** Open `http://localhost:8080`. Log in with `admin` / `admin`.

3.  **Run the DAG:**
    * Find `simple_crypto_elt_pipeline`.
    * Unpause it.
    * Trigger it.

4.  **View Logs:** To see the combined logs from all Airflow components:
    ```bash
    astro dev logs -f
    ```

5.  **Check Output:** After a successful run, you should find:
    * The `crypto.duckdb` file in the `data/` directory.
    * The `bitcoin_candlestick_chart.png` graph in the `data/` directory.

6.  **Stop the Environment:** When you are finished:
    ```bash
    make stop
    ```

7.  **Clean Up (Optional):** To stop and remove all containers, networks, and volumes:
    ```bash
    make clean
    ```

## Design Decisions & Notes

* **Extraction (`pycoingecko` vs. `PyAirbyte`):** While the business case suggested `PyAirbyte`, `pycoingecko` was chosen for its simplicity and directness (other setup and dependecy problems were encountered with airbyte). This allows a direct connection to the CoinGecko API, which was sufficient to demonstrate the core ELT flow within the given time constraints. Integrating `PyAirbyte` could be a next step.
* **Orchestration (`Airflow` + `BashOperator`):** Airflow is used as required. `BashOperator` provides a clear, simple way to execute Python scripts and `dbt` commands.
* **Environment (`Astro` CLI):** Provides a standardized, reproducible local Airflow environment, simplifying setup.
* **Visualization:** A visualization step was added to generate a candlestick chart from the transformed data, as suggested in the bonus points.

## Potential Next Steps

* Implement more robust `dbt` tests.
* Integrate `PyAirbyte` for extraction, as initially suggested.
* Enhance error handling and add data quality checks.
* Implement incremental `dbt` models for optimization.
* Develop more interactive data visualizations.
* Optimize performance (partitioning, indexing).
* Ensure full DAG idempotency.
