from flask import Blueprint

# Create blueprint instances
train_bp = Blueprint('train', __name__)
predict_bp = Blueprint('predict', __name__)
download_bp = Blueprint('download', __name__)
instrument_info_bp = Blueprint('intstrument_info', __name__)


# Import routes to register them with blueprints
from .train import train_bp
from .predict import predict_bp
from .download import download_bp
from .instrument_info import instrument_info_bp