# scripts/load.py
import duckdb
import json
from datetime import datetime
from common_configs import DB_FILE, RAW_TABLE_NAME, EXTRACTED_DATA_FILE, COIN_ID

def load_data_to_db():
    """
    Loads data from the JSON file into the DuckDB database.
    """
    print(f"--- Starting Data Loading ({datetime.now()}) ---")
    print(f"Loading data from {EXTRACTED_DATA_FILE} into {DB_FILE}.")

    conn = None # Initialize connection variable

    try:
        # 1. Read data from JSON file
        with open(EXTRACTED_DATA_FILE, 'r') as f:
            data = json.load(f)

        if not data:
            print("No data in JSON file. Nothing to load.")
            print(f"--- Data Loading Finished ({datetime.now()}) ---")
            return

        # 2. Connect to the database
        conn = duckdb.connect(database=DB_FILE, read_only=False)

        # 3. Ensure the table exists
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {RAW_TABLE_NAME} (
                timestamp TIMESTAMP,
                price DOUBLE,
                coin_id VARCHAR,
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 4. Clear old data for this coin (to avoid duplicates on re-runs)
        print(f"Clearing old data for '{COIN_ID}'...")
        conn.execute(f"DELETE FROM {RAW_TABLE_NAME} WHERE coin_id = ?", (COIN_ID,))

        # 5. Insert new data
        print(f"Inserting {len(data)} new records...")
        for record in data:
            timestamp_dt = datetime.fromisoformat(record['timestamp'])
            conn.execute(
                f"INSERT INTO {RAW_TABLE_NAME} (timestamp, price, coin_id) VALUES (?, ?, ?)",
                (timestamp_dt, record['price'], record['coin_id'])
            )
        print("Data inserted successfully.")

    except FileNotFoundError:
        print(f"!! Error: Cannot find {EXTRACTED_DATA_FILE}. Did the extract step run?")
    except Exception as e:
        print(f"!! An error occurred during loading: {e}")
    finally:
        # 6. Close the connection
        if conn:
            conn.close()
            print("Database connection closed.")

    print(f"--- Data Loading Finished ({datetime.now()}) ---")

# This makes the script runnable for testing
if __name__ == "__main__":
    load_data_to_db()