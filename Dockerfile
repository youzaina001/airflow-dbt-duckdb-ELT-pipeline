FROM quay.io/astronomer/astro-runtime:7.6.0

USER root

# Ensure curl and unzip are present
RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*

# Switch to astro user to install dbt locally
USER astro
RUN curl -L https://install.duckdb.org | sh

# Switch back to root to create the link in a system path
USER root
RUN ln -s /home/astro/.duckdb/cli/latest/duckdb /usr/local/bin/duckdb

# Switch back to astro
USER astro