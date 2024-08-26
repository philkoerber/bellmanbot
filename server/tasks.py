from celery import Celery
import os
import pandas as pd
import tensorflow as tf
import json
from datetime import datetime
from celery_config import make_celery

celery = make_celery()

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(50, activation='relu', input_shape=(1, 4)),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    return model

@celery.task(bind=True)
def train_model(self, symbol):
    try:
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
            epochs=30,
            batch_size=32,
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

        return {"message": f"Training completed and model for symbol '{symbol}' saved!"}
    except Exception as e:
        raise self.retry(exc=e)