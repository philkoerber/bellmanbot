from celery import Celery

def make_celery(app=None):
    celery = Celery(
        app.import_name if app else __name__,
        broker='redis://redis:6379/0',  # Redis as broker
        backend='redis://redis:6379/0'  # Redis as backend
    )
    if app is not None:
        celery.conf.update(app.config)
    
    # Explicitly ensure that Redis backend settings are correctly configured
    celery.conf.update(
        result_backend='redis://redis:6379/0',
        accept_content=['json'],
        result_serializer='json',
        task_serializer='json',
    )

    return celery