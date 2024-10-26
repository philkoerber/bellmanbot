import os
import tensorflow as tf

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
def train_autoencoder(X_scaled, input_dim, save_path):
    autoencoder, encoder = build_autoencoder(input_dim)
    
    # Train the autoencoder
    autoencoder.fit(X_scaled, X_scaled, epochs=50, batch_size=64, validation_split=0.2, verbose=2)
    
    # Save the trained encoder
    encoder.save(save_path)
    
    return encoder

# Function to load a pre-trained encoder
def load_encoder(encoder_path):
    if os.path.exists(encoder_path):
        return tf.keras.models.load_model(encoder_path)
    else:
        raise FileNotFoundError(f"Encoder file not found at {encoder_path}")
