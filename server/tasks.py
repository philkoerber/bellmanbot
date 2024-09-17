import os
import requests
import csv
import pandas as pd
import tensorflow as tf
import json
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from celery_config import make_celery

celery = make_celery()

# Configuration Constants
TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY') or '83a3ab2d88ff4292a6b446d30b5d27bc'
INTERVAL = os.getenv('INTERVAL') or '1min'
OUTPUTSIZE = 4000  # Maximum allowed by the API for one request
DATA_FOLDER = 'data'
TOTAL_RECORDS = 50000  # Number of records you want to retrieve for testing
MODELS_FOLDER = 'models'

# Ensure the data and models directories exist.
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(MODELS_FOLDER, exist_ok=True)

# Function to create the model
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(100, activation='relu', input_shape=(5, 4)),  # Adjust input shape based on sequences
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    return model

# Function to create sequences from data
def create_sequences(X, y, time_steps=5):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:i + time_steps])
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

# Task to download data using TwelveData API
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
                        record.get('volume', 0)  # Use 0 as default for volume
                    ])
                    total_data.append(record)

                if len(time_series) < OUTPUTSIZE:
                    break  # If fewer than the output size, we are at the end of the data

                end_date = time_series[-1]['datetime']

        print(f"Download complete for {symbol}. Total records: {len(total_data)}")
        return {"status": "success", "message": f"Download complete for {symbol}. Total records: {len(total_data)}"}

    except Exception as e:
        print(f"Error occurred: {e}")
        raise self.retry(exc=e)


# Task to train the model
@celery.task(bind=True)
def train_model(self, symbol):
    try:
        print(f"Starting training for symbol: {symbol}")

        safe_symbol = symbol.replace('/', '_')
        data_file = os.path.join(DATA_FOLDER, f'{safe_symbol}.csv')

        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file for symbol '{symbol}' not found.")

        # Load data
        df = pd.read_csv(data_file)
        X = df[['open', 'high', 'low', 'volume']].values
        y = df['close'].shift(-1).fillna(df['close']).values

        # Normalize data using MinMaxScaler
        scaler_X = MinMaxScaler()
        scaler_y = MinMaxScaler()

        X_scaled = scaler_X.fit_transform(X)
        y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

        # Create sequences (e.g., 5 time steps)
        time_steps = 5
        X_seq, y_seq = create_sequences(X_scaled, y_scaled, time_steps)

        # Split data into training and validation sets
        train_size = int(len(X_seq) * 0.8)
        X_train, X_val = X_seq[:train_size], X_seq[train_size:]
        y_train, y_val = y_seq[:train_size], y_seq[train_size:]

        model = create_model()

        # Train the model
        history = model.fit(
            X_train,
            y_train,
            epochs=100,
            batch_size=64,
            validation_data=(X_val, y_val),
            verbose=2
        )

        # Save the model and scalers
        model_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}.keras')
        model.save(model_path)

        # Save the scalers
        scaler_X_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}_scaler_X.pkl')
        scaler_y_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}_scaler_y.pkl')
        pd.to_pickle(scaler_X, scaler_X_path)
        pd.to_pickle(scaler_y, scaler_y_path)

        # Log results
        results = {
            "final_training_loss": history.history['loss'][-1],
            "final_validation_loss": history.history.get('val_loss', [None])[-1],
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        results_path = os.path.join(MODELS_FOLDER, 'results', f'{safe_symbol}_log.json')
        os.makedirs(os.path.join(MODELS_FOLDER, 'results'), exist_ok=True)
        with open(results_path, 'w') as f:
            json.dump(results, f)

        print(f"Training completed for symbol: {symbol}")
        return {"message": f"Training completed and model for symbol '{symbol}' saved!", "results": results}

    except Exception as e:
        print(f"Error occurred: {e}")
        raise self.retry(exc=e)

