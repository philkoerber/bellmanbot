import os
import tensorflow as tf

# Constants for folder paths
MODELS_FOLDER = 'models'
# Model Config Constants
MAX_EPOCHS = 50
FUTURE_STEPS = 10
TIME_STEPS = 10
BATCH_SIZE = 64

# Function to create and train an autoencoder
def build_autoencoder(input_dim):
    input_layer = tf.keras.layers.Input(shape=(input_dim,))
    encoded = tf.keras.layers.Dense(64, activation='relu')(input_layer)
    encoded = tf.keras.layers.Dense(32, activation='relu')(encoded)
    bottleneck = tf.keras.layers.Dense(16, activation='relu')(encoded)  # Bottleneck layer

    decoded = tf.keras.layers.Dense(32, activation='relu')(bottleneck)
    decoded = tf.keras.layers.Dense(64, activation='relu')(decoded)
    output_layer = tf.keras.layers.Dense(input_dim, activation='sigmoid')(decoded)

    autoencoder = tf.keras.models.Model(inputs=input_layer, outputs=output_layer)
    encoder = tf.keras.models.Model(inputs=input_layer, outputs=bottleneck)

    autoencoder.compile(optimizer='adam', loss='mse')
    
    return autoencoder, encoder

# Function to train and save the autoencoder
def train_autoencoder(X_scaled, input_dim, symbol, callback):
    safe_symbol = symbol.replace('/', '_')
    # Define save path based on symbol
    encoder_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}_encoder.keras')
    
    # Build the autoencoder
    autoencoder, encoder = build_autoencoder(input_dim)

    # Train the autoencoder with the provided callback
    autoencoder.fit(
        X_scaled, X_scaled, 
        epochs=MAX_EPOCHS, 
        batch_size=64, 
        validation_split=0.2, 
        verbose=2,
        callbacks=[callback] #need to pass down from parent because of socketio instance is in parent
    )
    
    # Save the trained encoder
    encoder.save(encoder_path)
    
    return encoder

# Function to load a pre-trained encoder
def load_encoder(safe_symbol):
    # Define path based on symbol
    encoder_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}_encoder.keras')
    
    if os.path.exists(encoder_path):
        return tf.keras.models.load_model(encoder_path)
    else:
        raise FileNotFoundError(f"Encoder file not found for symbol '{safe_symbol}' at {encoder_path}")

# Custom Callback for Autoencoder Training Progress
class SocketIOAutoencoderCallback(tf.keras.callbacks.Callback):
    def __init__(self, socketio, symbol):
        super(SocketIOAutoencoderCallback, self).__init__()
        self.socketio = socketio
        self.symbol = symbol

    def on_epoch_end(self, epoch, logs=None):
        # Emit training progress for each epoch
        self.socketio.emit("training_progress", {
            'status': "pending",
            'message': f"Training autoencoder...",
            'result': {
                'epoch': epoch + 1,
                'loss': logs.get('loss'),
                'valLoss': logs.get('val_loss')
            },
            "symbol": self.symbol
        })
