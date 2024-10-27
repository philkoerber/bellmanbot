import os
import requests
import csv
import pandas as pd
import tensorflow as tf
from datetime import datetime
from celery_config import make_celery
from server import socketio


celery = make_celery()

# Configuration Constants
TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY') or '83a3ab2d88ff4292a6b446d30b5d27bc'
OUTPUTSIZE = 4000  # Maximum allowed by the API for one request
DATA_FOLDER = 'data'
TOTAL_RECORDS = OUTPUTSIZE * 50  # Number of records you want to retrieve for testing

# Ensure the data and models directories exist.
os.makedirs(DATA_FOLDER, exist_ok=True)

# Task to download data using TwelveData API
@celery.task(name='download_data', bind=True)
def download_data(self, symbol):
    
    try:
        total_data = []
        end_date = os.getenv('END_DATE') or datetime.now().strftime('%Y-%m-%d')
        safe_symbol = symbol.replace('/', '_')
        data_file = os.path.join(DATA_FOLDER, f'{safe_symbol}.csv')

        socketio.emit("download_progress", {'status': "pending", 'message': "starting download...", "symbol": symbol})

        with open(data_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['datetime', 'open', 'high', 'low', 'close', 'volume'])

            while len(total_data) < TOTAL_RECORDS:
                url = f'https://api.twelvedata.com/time_series'
                params = {
                    'symbol': symbol,
                    'interval': '1min',
                    'end_date': end_date,
                    'outputsize': OUTPUTSIZE,
                    'apikey': TWELVEDATA_API_KEY
                }

                response = requests.get(url, params=params)
                response.raise_for_status()

                data = response.json()
                if 'values' not in data:
                    error_message = f"Error fetching data for {safe_symbol}: {data.get('message', 'Unknown error')}"
                    socketio.emit("download_progress", {'status': "error", 'message': "Something went wrong...", "symbol": symbol})
                    print(f"Error: {error_message}")
                    return {"status": "error", "message": error_message}

                time_series = data['values']
                for record in time_series:
                    writer.writerow([
                        record['datetime'],
                        record['open'],
                        record['high'],
                        record['low'],
                        record['close'],
                        record.get('volume', 0)  # Use 0 as default for volume
                    ])
                    total_data.append(record)

                socketio.emit("download_progress", {'status': "pending", 'message': f"{len(total_data)}/{TOTAL_RECORDS}", "symbol": symbol})

                if len(time_series) < OUTPUTSIZE:
                    break  # If fewer than the output size, we are at the end of the data

                end_date = time_series[-1]['datetime']

        print(f"Download complete for {symbol}. Total records: {len(total_data)}")
        socketio.emit("download_progress", {'status': "success", 'message': "Download complete", "symbol": symbol})
        return {"status": "success", "message": f"Download complete for {symbol}. Total records: {len(total_data)}"}

    except Exception as e:
        print(f"Error occurred: {e}")
        raise self.retry(exc=e)
