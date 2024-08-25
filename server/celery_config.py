from celery import Celery

def make_celery(app):
    # Configure Celery to use Redis as the message broker and backend
    celery = Celery(
        app.import_name,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0'
    )
    celery.conf.update(app.config)
    return celery