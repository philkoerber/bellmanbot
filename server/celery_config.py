from celery import Celery

def make_celery(app=None):
    celery = Celery(
        app.import_name if app else __name__,
        broker='redis://redis:6379/0',  # Redis service URL
        backend='redis://redis:6379/0'  # Redis service URL
    )
    if app is not None:
        celery.conf.update(app.config)
    return celery
