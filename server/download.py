from flask import Blueprint, jsonify
import os
import pandas as pd
import nasdaqdatalink as ndl

download_bp = Blueprint('download', __name__)

# Configuration
NASDAQ_API_KEY = os.getenv('NASDAQ_API_KEY') or 'QttARKYQYRXeP3setHbc'
SYMBOL = os.getenv('SYMBOL') or 'AAPL'  # Example: 'AAPL' for Apple stock
DATA_FILE = 'historical_nasdaq_data.csv'

# Function to download data and save to CSV
def download_nasdaq_data():
    try:
        # Set API key for nasdaq-data-link
        ndl.ApiConfig.api_key = NASDAQ_API_KEY

        # Retrieve historical data for the symbol
        data = ndl.get(f"WIKI/{SYMBOL}")

        # Save the data to a CSV file
        data.to_csv(DATA_FILE)
        
    except Exception as e:
        raise Exception(f"Failed to download data for symbol {SYMBOL}: {str(e)}")

@download_bp.route('/download', methods=['GET'])
def download_nasdaq_route():
    try:
        download_nasdaq_data()
        return jsonify({"message": "NASDAQ data downloaded and saved to CSV."})
    except Exception as e:
        return jsonify({"message": "Download failed!", "error": str(e)}), 500
