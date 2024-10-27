import os
import pandas as pd
import numpy as np
import tensorflow as tf
import json
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from celery_config import make_celery
from server import socketio
from tools.autoencoder import train_autoencoder, SocketIOAutoencoderCallback

# Initialize Celery
celery = make_celery()

# Configuration Constants
# Navigation
MODELS_FOLDER = 'models'
DATA_FOLDER = 'data'
# Model
MAX_EPOCHS = 50
FUTURE_STEPS = 10
TIME_STEPS = 10
BATCH_SIZE = 64


# Create folders if they don't exist
os.makedirs(MODELS_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# Function to create the RNN model
def create_model(input_shape=(10, 16), future_steps=10):  # Adjusted for autoencoder output
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(100, activation='tanh', input_shape=input_shape, return_sequences=True),
        tf.keras.layers.LSTM(50, activation='tanh'),
        tf.keras.layers.Dense(future_steps)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

# Function to create sequences from data
def create_sequences(X, y, time_steps=TIME_STEPS, future_steps=FUTURE_STEPS):
    Xs, ys = [], []
    for i in range(len(X) - time_steps - future_steps + 1):
        Xs.append(X[i:i + time_steps])
        ys.append(y[i + time_steps:i + time_steps + future_steps])
    return np.array(Xs), np.array(ys)

# Custom Callback to Emit SocketIO Events
class SocketIOCallback(tf.keras.callbacks.Callback):
    def __init__(self, socketio, symbol):
        super(SocketIOCallback, self).__init__()
        self.socketio = socketio
        self.symbol = symbol

    def on_epoch_end(self, epoch, logs=None):
        # Emit training progress for each epoch
        self.socketio.emit("training_progress", {
            'status': "pending",
            'message': "Currently training...",
            'result': {
                'epoch': epoch + 1,
                'loss': logs.get('loss'),
                'valLoss': logs.get('val_loss')
            },
            "symbol": self.symbol
        })

# Task to train the model
@celery.task(name="train_model", bind=True)
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
        X = df[['open', 'high', 'low', 'close', 'volume']].values
        y = df['close'].shift(-1).fillna(df['close']).values

        # Normalize data using StandardScaler
        scaler_X = StandardScaler()
        scaler_y = StandardScaler()

        X_scaled = scaler_X.fit_transform(X)  # Fit and transform X
        y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

        # Emit a starting message before training the autoencoder
        socketio.emit("training_progress", {
            'status': "pending",
            'message': "Starting autoencoder training...",
            "symbol": symbol
        })

        # Create the SocketIO callback for the autoencoder
        autoencoder_callback = SocketIOAutoencoderCallback(socketio, symbol)
        
        # Train Autoencoder using tools and transform the data
        encoder = train_autoencoder(X_scaled, X_scaled.shape[1], safe_symbol, autoencoder_callback)

        # Use the trained encoder to transform X_scaled data
        X_transformed = encoder.predict(X_scaled)

        # Emit a completion message after the autoencoder training
        socketio.emit("training_progress", {
            'status': "pending",
            'message': "Autoencoder training completed.",
            "symbol": symbol
        })

        # Create sequences using transformed data
        X_seq, y_seq = create_sequences(X_transformed, y_scaled, TIME_STEPS, FUTURE_STEPS)

        # Split data into training and validation sets
        train_size = int(len(X_seq) * 0.8)
        X_train, X_val = X_seq[:train_size], X_seq[train_size:]
        y_train, y_val = y_seq[:train_size], y_seq[train_size:]

        model = create_model(input_shape=(TIME_STEPS, X_transformed.shape[1]), future_steps=FUTURE_STEPS)

        # Create and pass the SocketIO callback for RNN model training
        socketio_callback = SocketIOCallback(socketio, symbol)

        # Train the model with the callback
        history = model.fit(
            X_train,
            y_train,
            epochs=MAX_EPOCHS,
            batch_size=BATCH_SIZE,
            validation_data=(X_val, y_val),
            verbose=2,
            callbacks=[socketio_callback]
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

    except Exception as e:
        print(f"Error occurred: {e}")
        socketio.emit("training_progress", {'status': "error", 'message': str(e), "symbol": symbol})
        raise self.retry(exc=e)
