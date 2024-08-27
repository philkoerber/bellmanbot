from celery import Celery
import os
import pandas as pd
import tensorflow as tf
import json
from datetime import datetime
from celery_config import make_celery
import time  # Import time module for sleep

celery = make_celery()

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(100, activation='relu', input_shape=(1, 4)),  # Increased neurons for longer training
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    return model

@celery.task(bind=True)
def train_model(self, symbol):
    try:
        print(f"Starting training for symbol: {symbol}")  # Debug log

        # Simulate delay at the start of the task
        time.sleep(30)  # Sleep for 30 seconds to ensure task is pending for a while

        sanitized_symbol = symbol.replace('/', '_')
        data_file = os.path.join('data', f'{sanitized_symbol}.csv')

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
            X_train, y_train,
            epochs=100,  # Increased epochs for longer training
            batch_size=64,  # Adjusted batch size
            validation_data=(X_val, y_val),
            verbose=2
        )

        model_path = os.path.join('models', f'{sanitized_symbol}.keras')
        model.save(model_path)

        results = {
            "final_training_loss": history.history['loss'][-1],
            "final_validation_loss": history.history.get('val_loss', [None])[-1],
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        results_path = os.path.join('models', 'results', f'{sanitized_symbol}_log.json')
        with open(results_path, 'w') as f:
            json.dump(results, f)

        print(f"Training completed for symbol: {symbol}")  # Debug log

        return {"message": f"Training completed and model for symbol '{symbol}' saved!", "results": results}
    except Exception as e:
        print(f"Error occurred: {e}")  # Debug log
        raise self.retry(exc=e)
