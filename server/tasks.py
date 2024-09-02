import os
import requests
import csv
import pandas as pd
import tensorflow as tf
import json
from datetime import datetime
from celery_config import make_celery

celery = make_celery()

# Configuration Constants
TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY') or '83a3ab2d88ff4292a6b446d30b5d27bc'
INTERVAL = os.getenv('INTERVAL') or '1min'
OUTPUTSIZE = 4000  # Maximum allowed by the API for one request
DATA_FOLDER = 'data'
TOTAL_RECORDS = 50000  # Number of records you want to retrieve for testing

# Ensure the data directory exists.
os.makedirs(DATA_FOLDER, exist_ok=True)

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(100, activation='relu', input_shape=(1, 4)),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    return model

@celery.task(bind=True)
def download_data(self, symbol):
    try:
        total_data = []
        end_date = os.getenv('END_DATE') or datetime.now().strftime('%Y-%m-%d')
        safe_symbol = symbol.replace('/', '_')
        data_file = os.path.join(DATA_FOLDER, f'{safe_symbol}.csv')

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
                    error_message = f"Error fetching data for {safe_symbol}: {data.get('message', 'Unknown error')}"
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
                        record.get('volume', 0)
                    ])
                    total_data.append(record)

                if len(time_series) < OUTPUTSIZE:
                    break

                end_date = time_series[-1]['datetime']

        print(f"Download complete for {symbol}. Total records: {len(total_data)}")

        return {"status": "success", "message": f"Download complete for {symbol}. Total records: {len(total_data)}"}
    
    except Exception as e:
        print(f"Error occurred: {e}")
        raise self.retry(exc=e)

@celery.task(bind=True)
def train_model(self, symbol):
    try:
        print(f"Starting training for symbol: {symbol}")

        safe_symbol = symbol.replace('/', '_')
        data_file = os.path.join(DATA_FOLDER, f'{safe_symbol}.csv')

        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file for symbol '{symbol}' not found.")

        df = pd.read_csv(data_file)
        X = df[['open', 'high', 'low', 'volume']].values
        y = df['close'].shift(-1).fillna(df['close']).values
        X = X.reshape((X.shape[0], 1, X.shape[1]))
        y = y.reshape((y.shape[0], 1))

        model = create_model()
        train_size = int(len(X) * 0.8)
        X_train, X_val = X[:train_size], X[train_size:]
        y_train, y_val = y[:train_size], y[train_size:]

        history = model.fit(
            X_train,
            y_train,
            epochs=100,
            batch_size=64,
            validation_data=(X_val, y_val),
            verbose=2
        )

        model_path = os.path.join('models', f'{safe_symbol}.keras')
        model.save(model_path)

        results = {
            "final_training_loss": history.history['loss'][-1],
            "final_validation_loss": history.history.get('val_loss', [None])[-1],
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        results_path = os.path.join('models', 'results', f'{safe_symbol}_log.json')
        with open(results_path, 'w') as f:
            json.dump(results, f)

        print(f"Training completed for symbol: {symbol}")

        return {"message": f"Training completed and model for symbol '{symbol}' saved!", "results": results}
    
    except Exception as e:
        print(f"Error occurred: {e}")
        raise self.retry(exc=e)