from flask import Blueprint

# Create blueprint instances
train_bp = Blueprint('train', __name__)
predict_bp = Blueprint('predict', __name__)
download_bp = Blueprint('download', __name__)
metadata_bp = Blueprint('metadata', __name__)
job_status_bp = Blueprint('job_status', __name__)
health_bp = Blueprint('health', __name__)

# Import routes to register them with blueprints
from .train import train_bp
from .predict import predict_bp
from .download import download_bp
from .metadata import metadata_bp
from .job_status import job_status_bp
from .health import health_bp