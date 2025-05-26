# include/visualize.py
import duckdb
import pandas as pd
import mplfinance as mpf # For candlestick charts
import os
from datetime import datetime

# For simplicity, DB_FILE and plot output paths are defined here
DB_FILE = '/usr/local/airflow/data/crypto.duckdb'
PLOT_OUTPUT_DIR = '/usr/local/airflow/data' # Output directory inside the container
PLOT_FILENAME = 'bitcoin_candlestick_chart.png'
PLOT_FILE_PATH = os.path.join(PLOT_OUTPUT_DIR, PLOT_FILENAME)

# Let's use 'bitcoin' as per the project's focus.
COIN_TO_PLOT = 'bitcoin' 

def generate_candlestick_visualization():
    """
    Connects to DuckDB, queries the daily_candlestick data,
    and generates a candlestick chart for the specified coin.
    """
    print(f"--- Starting Candlestick Data Visualization ({datetime.now()}) ---")
    print(f"Connecting to database: {DB_FILE}")

    if not os.path.exists(DB_FILE):
        print(f"!! Error: Database file not found at {DB_FILE}. Cannot generate visualization.")
        print(f"--- Candlestick Data Visualization Finished ({datetime.now()}) ---")
        return

    conn = None
    try:
        conn = duckdb.connect(database=DB_FILE, read_only=True)
        print("Successfully connected to DuckDB.")

        query = f"""
        SELECT 
            trade_date,
            opening_price,
            maximum_price, -- dbt model output this as high
            minimum_price, -- dbt model output this as low
            closing_price
        FROM daily_candlestick
        WHERE coin_id = '{COIN_TO_PLOT}'
        ORDER BY trade_date ASC;
        """
        print(f"Executing query for {COIN_TO_PLOT}: {query}")
        df = conn.execute(query).fetchdf()
        print(f"Fetched {len(df)} rows for visualization.")

        if df.empty:
            print(f"No data found for '{COIN_TO_PLOT}' in daily_candlestick table.")
            print(f"--- Candlestick Data Visualization Finished ({datetime.now()}) ---")
            return

        # Preparing DataFrame for mplfinance:
        # 1. Convert 'trade_date' to Datetime objects and set as index
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df.set_index('trade_date', inplace=True)

        # 2. Rename columns to what mplfinance expects: Open, High, Low, Close (case-sensitive)
        df.rename(columns={
            'opening_price': 'Open',
            'maximum_price': 'High',
            'minimum_price': 'Low',
            'closing_price': 'Close'
        }, inplace=True)
        
        # Select only the required OHLC columns
        ohlc_df = df[['Open', 'High', 'Low', 'Close']]

        print("DataFrame prepared for plotting:")
        print(ohlc_df.head())

        # Generate the candlestick plot
        print(f"Generating candlestick chart and saving to {PLOT_FILE_PATH}...")
        os.makedirs(PLOT_OUTPUT_DIR, exist_ok=True) # Ensure output directory exists
        
        mpf.plot(ohlc_df, 
                type='candle', 
                style='yahoo',
                title=f'{COIN_TO_PLOT.capitalize()} Daily Candlestick Chart',
                ylabel='Price (USD)',
                savefig=dict(fname=PLOT_FILE_PATH, dpi=150, pad_inches=0.25),
                volume=False,
                )
        
        print(f"Plot saved successfully to {PLOT_FILE_PATH}")

    except Exception as e:
        print(f"!! An error occurred during visualization: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
    
    print(f"--- Candlestick Data Visualization Finished ({datetime.now()}) ---")

if __name__ == "__main__":
    generate_candlestick_visualization()