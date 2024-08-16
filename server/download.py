from flask import Blueprint, jsonify
import os
import pandas as pd
import asyncio
from metaapi_cloud_sdk import MetaApi
from datetime import datetime

download_bp = Blueprint('download', __name__)

# Configuration
TOKEN = os.getenv('TOKEN') or '<put your token here>'
ACCOUNT_ID = os.getenv('ACCOUNT_ID') or '<put your account id here>'
SYMBOL = os.getenv('SYMBOL') or 'EURUSD'
DOMAIN = os.getenv('DOMAIN') or 'agiliumtrade.agiliumtrade.ai'
DATA_FILE = 'historical_data.csv'

# Function to download data and save to CSV
async def download_data():
    api = MetaApi(TOKEN, {'domain': DOMAIN})
    account = await api.metatrader_account_api.get_account(ACCOUNT_ID)

    # Ensure account is connected
    if account.state != 'DEPLOYED':
        await account.deploy()
    if account.connection_status != 'CONNECTED':
        await account.wait_connected()

    # Set up the parameters for data retrieval
    pages = 10
    start_time = datetime.fromtimestamp(datetime.now().timestamp() - 7 * 24 * 60 * 60)
    offset = 0
    all_ticks = []

    # Retrieve and collect data
    for i in range(pages):
        ticks = await account.get_historical_ticks(SYMBOL, start_time, offset)
        if ticks:
            all_ticks.extend(ticks)
            start_time = ticks[-1]['time']
            offset = 0
            while offset < len(ticks) and ticks[-1 - offset]['time'].timestamp() == start_time.timestamp():
                offset += 1

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame([{
        'time': tick['time'],
        'bid': tick['bid'],
        'ask': tick['ask']
    } for tick in all_ticks])
    
    df.to_csv(DATA_FILE, index=False)

@download_bp.route('/download_data', methods=['GET'])
def download_data_route():
    try:
        asyncio.run(download_data())
        return jsonify({"message": "Data downloaded and saved to CSV."})
    except Exception as e:
        return jsonify({"message": "Download failed!", "error": str(e)}), 500
