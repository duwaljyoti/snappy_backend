import os
from celery import Celery

# 1. Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snappy_backend.settings')

# 2. Create the Celery app instance.
app = Celery('snappy_backend')

# 3. Read config from Django settings using the 'CELERY' namespace.
# This means all celery-related settings in settings.py must start with CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. Automatically discover tasks from all registered Django apps.
# It looks for a 'tasks.py' file inside each app directory.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
