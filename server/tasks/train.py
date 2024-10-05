import os
import pandas as pd
import numpy as np
import tensorflow as tf
import json
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from celery_config import make_celery
from server import socketio


celery = make_celery()

# Configuration Constants
MODELS_FOLDER = 'models'
DATA_FOLDER = 'data'

os.makedirs(MODELS_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

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

# Task to train the model
@celery.task(name="train_model",bind=True)
def train_model(self, symbol):
    try:
        print(f"Starting training for symbol: {symbol}")
        socketio.emit("training_progress", {'status': "pending", 'message': "starting training...", "symbol": symbol})

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
        socketio.emit("training_progress", {'status': "success", 'message': "Training finished", "symbol": symbol})
        return {"message": f"Training completed and model for symbol '{symbol}' saved!", "results": results}

    except Exception as e:
        print(f"Error occurred: {e}")
        raise self.retry(exc=e)

