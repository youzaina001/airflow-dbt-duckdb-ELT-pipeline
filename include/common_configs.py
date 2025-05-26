# scripts/common_configs.py
import os

print("--- Loading Project Configurations ---")

# --- Define Project Paths ---
# We assume this file is in 'include/' and the main project folder is one level up.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Project Root (assumed): {PROJECT_ROOT}")

# --- API Configuration ---
COIN_ID = 'bitcoin'
VS_CURRENCY = 'usd'
DAYS_RANGE = 30 # Fetch data for the last 30 days

# --- Database and File Path Configuration ---
# We'll build paths based on the PROJECT_ROOT.
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
TEMP_DATA_DIR = os.path.join(PROJECT_ROOT, 'scripts', 'temp_data')

RAW_TABLE_NAME = 'raw_crypto_prices'
DB_FILE = os.path.join(DATA_DIR, 'crypto.duckdb')
EXTRACTED_DATA_FILE = os.path.join(TEMP_DATA_DIR, 'extracted_crypto_data.json')

# --- Ensure directories exist ---
if not os.path.exists(DATA_DIR):
    print(f"Creating data directory: {DATA_DIR}")
    os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(TEMP_DATA_DIR):
    print(f"Creating temp data directory: {TEMP_DATA_DIR}")
    os.makedirs(TEMP_DATA_DIR, exist_ok=True)


# --- Log effective configurations ---
print("--- Effective Configurations ---")
print(f"CoinGecko Coin ID: {COIN_ID}")
print(f"CoinGecko VS Currency: {VS_CURRENCY}")
print(f"CoinGecko Days Range: {DAYS_RANGE}")
print(f"Raw Table Name: {RAW_TABLE_NAME}")
print(f"DB File Path: {DB_FILE}")
print(f"Extracted Data File Path: {EXTRACTED_DATA_FILE}")
print("---------------------------------")