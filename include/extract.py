# scripts/extract.py
import json
from datetime import datetime
from pycoingecko import CoinGeckoAPI
from common_configs import COIN_ID, DAYS_RANGE, EXTRACTED_DATA_FILE

def fetch_and_save_crypto_data():
    """
    Fetches crypto data from CoinGecko and saves it to a JSON file.
    """
    print(f"--- Starting Data Extraction ({datetime.now()}) ---")
    print(f"Fetching data for '{COIN_ID}' for {DAYS_RANGE} days.")

    cg = CoinGeckoAPI()
    data_to_save = [] # Default to empty list

    try:
        # 1. Fetch data directly from the API
        market_chart = cg.get_coin_market_chart_by_id(
            id=COIN_ID,
            vs_currency='usd',
            days=DAYS_RANGE
        )
        prices = market_chart.get('prices', [])

        # 2. Prepare data for saving
        for point in prices:
            timestamp_ms, price = point
            timestamp_dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
            data_to_save.append({
                'timestamp': timestamp_dt.isoformat(),
                'price': price,
                'coin_id': COIN_ID
            })
        print(f"Fetched {len(data_to_save)} data points.")

    except Exception as e:
        print(f"!! Error fetching data from CoinGecko: {e}")
        print("!! Proceeding with an empty list.")

    # 3. Save data (or empty list on error) to JSON
    print(f"Saving data to {EXTRACTED_DATA_FILE}...")
    try:
        with open(EXTRACTED_DATA_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print("Data saved successfully.")
    except Exception as e:
        print(f"!! Error saving data to JSON: {e}")

    print(f"--- Data Extraction Finished ({datetime.now()}) ---")

# This makes the script runnable for testing
if __name__ == "__main__":
    fetch_and_save_crypto_data()