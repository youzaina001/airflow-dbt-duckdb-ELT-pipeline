# Simplified Makefile for the Crypto ELT Pipeline

# --- Astro CLI Commands ---
.PHONY: start
start: ## Starts the local Airflow environment (astro dev start)
	@echo "Starting local Airflow environment..."
	astro dev start

.PHONY: stop
stop: ## Stops the local Airflow environment (astro dev stop)
	@echo "Stopping local Airflow environment..."
	astro dev stop

.PHONY: restart
restart: stop start ## Restarts the local Airflow environment

# --- dbt Commands ---
# Assumes you are in the project root and dbt_project is a subdirectory
.PHONY: dbt-run
dbt-run: ## Runs dbt models (dbt run)
	@echo "Running dbt models..."
	cd ./dbt_project && dbt run --profiles-dir .

.PHONY: dbt-test
dbt-test: ## Runs dbt tests (dbt test)
	@echo "Running dbt tests..."
	cd ./dbt_project && dbt test --profiles-dir .

# --- Cleanup ---
.PHONY: clean
clean: ## Cleans dbt target and Python pycache files
	@echo "Cleaning dbt target directory..."
	cd ./dbt_project && dbt clean
	@echo "Removing __pycache__ directories..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.py[co]" -delete
	@echo "Project cleaned."
	@echo "Terminating astro dev environment..."
	astro dev kill
	@echo "All clean up done."

# --- Help ---
.PHONY: help
help: ## Shows this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Set a default goal
.DEFAULT_GOAL := help