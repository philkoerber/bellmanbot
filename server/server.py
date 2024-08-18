from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Import the blueprints
from train import train_bp
from predict import predict_bp
from download import download_bp

# Register the blueprints
app.register_blueprint(train_bp, url_prefix='/api')
app.register_blueprint(predict_bp, url_prefix='/api')
app.register_blueprint(download_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask server!"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000) 