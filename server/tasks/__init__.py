from celery_config import make_celery  # Import your Celery app creation function
from .download import download_data  # Import your tasks
from .train import train_model

celery = make_celery()  # Initialize Celery