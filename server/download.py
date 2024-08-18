from flask import Blueprint, Response, stream_with_context, request
import os
import requests
import csv
from datetime import datetime

download_bp = Blueprint('download', __name__)

# Configuration
TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY') or '83a3ab2d88ff4292a6b446d30b5d27bc'
INTERVAL = os.getenv('INTERVAL') or '1min'
OUTPUTSIZE = 4000  # Set to the maximum allowed by the API for one request
DATA_FOLDER = 'data'
TOTAL_RECORDS = 16000  # Number of records you want to retrieve for testing

# Ensure the data directory exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def stream_twelvedata_large(symbol):
    try:
        total_data = []
        end_date = os.getenv('END_DATE') or datetime.now().strftime('%Y-%m-%d')
        data_file = os.path.join(DATA_FOLDER, f'twelvedata_{symbol}.csv')

        with open(data_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['datetime', 'open', 'high', 'low', 'close', 'volume'])

            while len(total_data) < TOTAL_RECORDS:
                url = f'https://api.twelvedata.com/time_series'
                params = {
                    'symbol': symbol,
                    'interval': INTERVAL,
                    'end_date': end_date,
                    'outputsize': OUTPUTSIZE,
                    'apikey': TWELVEDATA_API_KEY
                }

                response = requests.get(url, params=params)
                response.raise_for_status()

                data = response.json()
                if 'values' not in data:
                    raise Exception(f"Error fetching data: {data.get('message', 'Unknown error')}")

                time_series = data['values']
                for record in time_series:
                    writer.writerow([
                        record['datetime'],
                        record['open'],
                        record['high'],
                        record['low'],
                        record['close'],
                        record['volume']
                    ])
                    total_data.append(record)

                if len(time_series) < OUTPUTSIZE:
                    break

                end_date = time_series[-1]['datetime']

            yield f"data: Download complete for {symbol}. Total records: {len(total_data)}\n\n"

    except Exception as e:
        yield f"data: Error: {str(e)}\n\n"

@download_bp.route('/download', methods=['GET'])
def download_twelvedata_route():
    # Get the symbol from query parameters, default to 'AAPL' if not provided
    symbol = request.args.get('symbol', 'AAPL')
    return Response(stream_with_context(stream_twelvedata_large(symbol)), content_type='text/event-stream')
